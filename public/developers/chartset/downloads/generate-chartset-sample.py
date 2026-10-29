#!/usr/bin/env python3
"""Generate the minimal DingHai chart set sample (minimal-chartset.zip on dinghai.app).

A reference producer for the DingHai chart set integration manual
(https://dinghai.app/developers/chartset/), using only the Python
standard library: it projects a few hand-written objects (depth areas,
depth contours, soundings, a land area and its coastline, an anchorage, a
lateral buoy with its light, and a wreck) to Web Mercator, clips them per
tile, encodes MVT 2.1, gzips each tile, and writes a plain MBTiles 1.3 file
(`tiles` is a table) plus `manifest.json`.

The output is deterministic: running it again with the same Python rewrites
the same bytes. Across Python versions, the gzip header of a tile may
differ in one byte (the OS field) and the SQLite file header records the
SQLite library version; the decompressed MVT of every tile and the
manifest are the same. To compare with the published sample, compare
manifest.json and the decoded tiles, not the files' bytes.
Always pass --output: the default output directory,
docs/samples/minimal-chartset/ next to the script's parent directory, is
the layout this script was written in, not something you need to create.

    python3 generate-chartset-sample.py --output <dir>
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import os
import sqlite3
import struct
import tempfile
from pathlib import Path

EXTENT = 4096
BUFFER = 80
MIN_ZOOM = 10
MAX_ZOOM = 16
PROFILE = 1

# A made-up island in open water west of the Golden Gate. Offsets below are
# metres east/north of this point.
CENTER_LON = -122.62
CENTER_LAT = 37.80

MANIFEST = {
    "format": "dinghai-chartset",
    "formatVersion": "1.0",
    "tileProfile": PROFILE,
    "id": "example.org:minimal-sample",
    "name": "最小样例海图集",
    "source": {"type": "external", "producer": "scripts/generate-chartset-sample.py 1"},
    "minimumZoom": MIN_ZOOM,
    "maximumZoom": MAX_ZOOM,
    "createdAt": "2026-10-01T00:00:00Z",
}


# --- Geometry in metres around the centre -----------------------------------

def to_lonlat(east: float, north: float) -> tuple[float, float]:
    metres_per_degree = 111_320.0
    lat = CENTER_LAT + north / metres_per_degree
    lon = CENTER_LON + east / (metres_per_degree * math.cos(math.radians(CENTER_LAT)))
    return (lon, lat)


def ellipse(rx: float, ry: float, steps: int = 24) -> list[tuple[float, float]]:
    """A closed ring (first point not repeated), counter-clockwise on the map."""
    return [
        to_lonlat(rx * math.cos(2 * math.pi * i / steps), ry * math.sin(2 * math.pi * i / steps))
        for i in range(steps)
    ]


def rectangle(west: float, south: float, east: float, north: float) -> list[tuple[float, float]]:
    return [to_lonlat(west, south), to_lonlat(east, south), to_lonlat(east, north), to_lonlat(west, north)]


ISLAND = ellipse(350, 220)
SHALLOW = ellipse(650, 450)   # 0–5 m ring around the island
MEDIUM = ellipse(1000, 750)   # 5–10 m ring
OUTER = rectangle(-1800, -1300, 1800, 1300)  # 10–20 m out to the edge
ANCHORAGE = rectangle(1150, -1150, 1650, -750)

# Each feature: (layer, kind, geometry, attributes). kind is "polygon"
# (list of rings, first outer), "line" (list of points; closed when the
# first point is repeated) or "point" (one lon/lat).
FEATURES: list[tuple[str, str, object, dict]] = [
    ("DEPARE", "polygon", [OUTER, MEDIUM], {"DRVAL1": 10.0, "DRVAL2": 20.0}),
    ("DEPARE", "polygon", [MEDIUM, SHALLOW], {"DRVAL1": 5.0, "DRVAL2": 10.0}),
    ("DEPARE", "polygon", [SHALLOW, ISLAND], {"DRVAL1": 0.0, "DRVAL2": 5.0}),
    ("DEPCNT", "line", SHALLOW + SHALLOW[:1], {"VALDCO": 5.0}),
    ("DEPCNT", "line", MEDIUM + MEDIUM[:1], {"VALDCO": 10.0}),
    ("LNDARE", "polygon", [ISLAND], {}),
    ("COALNE", "line", ISLAND + ISLAND[:1], {}),
    ("SOUNDG", "point", to_lonlat(-500, 0), {"DEPTH": 3.4}),
    ("SOUNDG", "point", to_lonlat(0, 600), {"DEPTH": 7.2}),
    ("SOUNDG", "point", to_lonlat(-1200, -900), {"DEPTH": 14.8}),
    ("SOUNDG", "point", to_lonlat(1400, 700), {"DEPTH": 18.5}),
    # The anchorage: its polygon (filled by nothing, read by a tap) and its
    # visible outline as a line with dh_boundary = 1 and the same attributes.
    ("ACHARE", "polygon", [ANCHORAGE], {"CATACH": "1", "OBJNAM": "Sample Anchorage"}),
    ("ACHARE", "line", ANCHORAGE + ANCHORAGE[:1],
     {"CATACH": "1", "OBJNAM": "Sample Anchorage", "dh_boundary": 1}),
    # A port-hand lateral buoy, IALA B (green, can), with a light on it.
    ("BOYLAT", "point", to_lonlat(700, -500),
     {"BOYSHP": 2, "CATLAM": 1, "COLOUR": "4", "MARSYS": 2, "OBJNAM": "Sample 1"}),
    ("LIGHTS", "point", to_lonlat(700, -500),
     {"COLOUR": "4", "LITCHR": 2, "SIGGRP": "(1)", "SIGPER": 4.0, "OBJNAM": "Sample 1"}),
    # A dangerous wreck with a known depth.
    ("WRECKS", "point", to_lonlat(-750, 350),
     {"CATWRK": 2, "WATLEV": 3, "VALSOU": 6.5, "OBJNAM": "Sample Wreck",
      "INFORM": "Generated sample object."}),
]


# --- Web Mercator ------------------------------------------------------------

def world(lon: float, lat: float, zoom: int) -> tuple[float, float]:
    """Global tile-extent units at `zoom`, y down."""
    scale = EXTENT * (1 << zoom)
    x = (lon + 180.0) / 360.0 * scale
    s = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * scale
    return (x, y)


# --- Clipping ----------------------------------------------------------------

def clip_ring(ring, x0, y0, x1, y1):
    """Sutherland–Hodgman against an axis-aligned box."""
    def clip(points, inside, intersect):
        out = []
        for i, current in enumerate(points):
            previous = points[i - 1]
            if inside(current):
                if not inside(previous):
                    out.append(intersect(previous, current))
                out.append(current)
            elif inside(previous):
                out.append(intersect(previous, current))
        return out

    def at_x(x):
        return lambda p, q: (x, p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0]))

    def at_y(y):
        return lambda p, q: (p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1]), y)

    points = list(ring)
    for inside, intersect in (
        (lambda p: p[0] >= x0, at_x(x0)),
        (lambda p: p[0] <= x1, at_x(x1)),
        (lambda p: p[1] >= y0, at_y(y0)),
        (lambda p: p[1] <= y1, at_y(y1)),
    ):
        if not points:
            break
        points = clip(points, inside, intersect)
    return points


def clip_line(points, x0, y0, x1, y1):
    """Liang–Barsky per segment, joined into runs."""
    runs, run = [], []
    for p, q in zip(points, points[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        t0, t1, keep = 0.0, 1.0, True
        for edge_p, edge_q in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
            if edge_p == 0:
                if edge_q < 0:
                    keep = False
                    break
            else:
                t = edge_q / edge_p
                if edge_p < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
        if not keep or t0 > t1:
            if run:
                runs.append(run)
                run = []
            continue
        a = (p[0] + t0 * dx, p[1] + t0 * dy)
        b = (p[0] + t1 * dx, p[1] + t1 * dy)
        if not run:
            run = [a]
        run.append(b)
        if t1 < 1.0:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    return runs


def to_local(points, origin_x, origin_y):
    out = []
    for x, y in points:
        p = (round(x - origin_x), round(y - origin_y))
        if not out or out[-1] != p:
            out.append(p)
    return out


def signed_area(ring):
    """Shoelace in tile coordinates (y down); MVT outer rings are positive."""
    return sum(ring[i - 1][0] * ring[i][1] - ring[i][0] * ring[i - 1][1] for i in range(len(ring))) / 2


# --- MVT encoding -------------------------------------------------------------

def varint(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def zigzag(value: int) -> int:
    return (value << 1) ^ (value >> 63)


def field(number: int, wire: int, payload: bytes) -> bytes:
    return varint((number << 3) | wire) + payload


def length_delimited(number: int, payload: bytes) -> bytes:
    return field(number, 2, varint(len(payload)) + payload)


def encode_value(value) -> bytes:
    if isinstance(value, str):
        return length_delimited(1, value.encode("utf-8"))
    if isinstance(value, bool):
        return field(7, 0, varint(int(value)))
    if isinstance(value, int):
        return field(6, 0, varint(zigzag(value)))  # sint_value
    return field(3, 1, struct.pack("<d", value))  # double_value


def command(cid: int, count: int) -> int:
    return (count << 3) | cid


def encode_geometry(kind: str, parts) -> list[int]:
    words, cx, cy = [], 0, 0
    for part in parts:
        x, y = part[0]
        words += [command(1, 1), zigzag(x - cx), zigzag(y - cy)]
        cx, cy = x, y
        if kind == "point":
            continue
        rest = part[1:]
        words.append(command(2, len(rest)))
        for x, y in rest:
            words += [zigzag(x - cx), zigzag(y - cy)]
            cx, cy = x, y
        if kind == "polygon":
            words.append(command(7, 1))
    return words


GEOMETRY_TYPE = {"point": 1, "line": 2, "polygon": 3}


def encode_layer(name: str, features) -> bytes:
    keys, values, body = [], [], b""
    for identifier, kind, parts, attributes in features:
        tags = []
        for key in sorted(attributes):
            if key not in keys:
                keys.append(key)
            value = attributes[key]
            typed = (type(value), value)
            if typed not in values:
                values.append(typed)
            tags += [keys.index(key), values.index(typed)]
        packed_tags = b"".join(varint(t) for t in tags)
        packed_geometry = b"".join(varint(w) for w in encode_geometry(kind, parts))
        feature = (
            field(1, 0, varint(identifier))
            + length_delimited(2, packed_tags)
            + field(3, 0, varint(GEOMETRY_TYPE[kind]))
            + length_delimited(4, packed_geometry)
        )
        body += length_delimited(2, feature)
    layer = field(15, 0, varint(2)) + length_delimited(1, name.encode("utf-8")) + body
    layer += b"".join(length_delimited(3, k.encode("utf-8")) for k in keys)
    layer += b"".join(length_delimited(4, encode_value(v)) for _, v in values)
    layer += field(5, 0, varint(EXTENT))
    return layer


# --- Tiling --------------------------------------------------------------------

def tile_features(zoom: int, column: int, row: int):
    """Clipped features of one tile, grouped by layer, in input order."""
    ox, oy = column * EXTENT, row * EXTENT
    x0, y0, x1, y1 = ox - BUFFER, oy - BUFFER, ox + EXTENT + BUFFER, oy + EXTENT + BUFFER
    layers: dict[str, list] = {}
    for identifier, (layer, kind, geometry, attributes) in enumerate(FEATURES, start=1):
        parts = []
        if kind == "point":
            x, y = world(*geometry, zoom)
            if x0 <= x <= x1 and y0 <= y <= y1:
                parts = [to_local([(x, y)], ox, oy)]
        elif kind == "line":
            projected = [world(lon, lat, zoom) for lon, lat in geometry]
            for run in clip_line(projected, x0, y0, x1, y1):
                local = to_local(run, ox, oy)
                if len(local) >= 2:
                    parts.append(local)
        else:
            for index, ring in enumerate(geometry):
                projected = [world(lon, lat, zoom) for lon, lat in ring]
                local = to_local(clip_ring(projected, x0, y0, x1, y1), ox, oy)
                if len(local) > 1 and local[0] == local[-1]:
                    local.pop()
                if len(local) < 3 or signed_area(local) == 0:
                    if index == 0:
                        break  # outer ring gone: so is the polygon
                    continue
                outer = index == 0
                if (signed_area(local) > 0) != outer:
                    local.reverse()
                parts.append(local)
        if parts:
            layers.setdefault(layer, []).append((identifier, kind, parts, attributes))
    return layers


def bounds():
    lons, lats = [], []
    for _, kind, geometry, _ in FEATURES:
        points = [geometry] if kind == "point" else (
            [p for ring in geometry for p in ring] if kind == "polygon" else geometry
        )
        lons += [p[0] for p in points]
        lats += [p[1] for p in points]
    return (min(lons), min(lats), max(lons), max(lats))


def build_tiles():
    west, south, east, north = bounds()
    tiles = []
    for zoom in range(MIN_ZOOM, MAX_ZOOM + 1):
        (left, top), (right, bottom) = world(west, north, zoom), world(east, south, zoom)
        for column in range(int((left - BUFFER) // EXTENT), int((right + BUFFER) // EXTENT) + 1):
            for row in range(int((top - BUFFER) // EXTENT), int((bottom + BUFFER) // EXTENT) + 1):
                layers = tile_features(zoom, column, row)
                if not layers:
                    continue
                payload = b"".join(length_delimited(3, encode_layer(name, features))
                                   for name, features in layers.items())
                tms_row = (1 << zoom) - 1 - row
                tiles.append((zoom, column, tms_row, gzip.compress(payload, mtime=0)))
    return tiles


# --- Output ----------------------------------------------------------------------

def vector_layers():
    fields: dict[str, dict[str, str]] = {}
    for layer, _, _, attributes in FEATURES:
        layer_fields = fields.setdefault(layer, {})
        for key, value in attributes.items():
            layer_fields[key] = "String" if isinstance(value, str) else "Number"
    return [
        {"id": layer, "minzoom": MIN_ZOOM, "maxzoom": MAX_ZOOM, "fields": dict(sorted(fields[layer].items()))}
        for layer in sorted(fields)
    ]


def write(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    west, south, east, north = (round(v, 6) for v in bounds())
    metadata = {
        "name": MANIFEST["name"],
        "format": "pbf",
        "type": "overlay",
        "version": "1",
        "scheme": "tms",
        "minzoom": str(MIN_ZOOM),
        "maxzoom": str(MAX_ZOOM),
        "bounds": f"{west},{south},{east},{north}",
        "center": f"{round((west + east) / 2, 6)},{round((south + north) / 2, 6)},{MIN_ZOOM}",
        "json": json.dumps({"vector_layers": vector_layers()}, separators=(",", ":"), sort_keys=True),
        "dh_profile": str(PROFILE),
    }

    descriptor, temporary = tempfile.mkstemp(dir=output, suffix=".mbtiles")
    os.close(descriptor)
    try:
        database = sqlite3.connect(temporary)
        database.executescript(
            "CREATE TABLE metadata (name TEXT PRIMARY KEY, value TEXT);"
            "CREATE TABLE tiles (zoom_level INTEGER, tile_column INTEGER, tile_row INTEGER, tile_data BLOB,"
            " PRIMARY KEY (zoom_level, tile_column, tile_row));"
        )
        database.executemany("INSERT INTO metadata VALUES (?, ?)", sorted(metadata.items()))
        database.executemany("INSERT INTO tiles VALUES (?, ?, ?, ?)", build_tiles())
        database.commit()
        database.execute("VACUUM")
        database.close()
        os.replace(temporary, output / "chart.mbtiles")
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)

    manifest = dict(MANIFEST)
    manifest["bounds"] = {"west": west, "south": south, "east": east, "north": north}
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    default = Path(__file__).resolve().parent.parent / "docs" / "samples" / "minimal-chartset"
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=default)
    write(parser.parse_args().output)


if __name__ == "__main__":
    main()
