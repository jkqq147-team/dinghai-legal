---
title: Connect Data Sources
description: Add Signal K or NMEA 0183 TCP data sources in DingHai.
---

DingHai supports Signal K and NMEA 0183 TCP data sources. Gateways that only broadcast over UDP are not currently supported.

## Signal K

1. Connect the device running DingHai to the same Wi-Fi network as the Signal K server, then open "Data Sources." Discovered Signal K services appear under "在这个网络上找到" (services found on this network). Tap the "+" on the right to add one.
2. If the server is not found, open "手动输入地址" (manual address entry), select "Signal K" as the type, and enter the server's `IP:port`.
3. If the server has security enabled, enter your username and password, then tap "Add."

## NMEA 0183 TCP

Open "手动输入地址" (manual address entry), select "NMEA 0183" as the type, enter the gateway or server's `IP:port`, then tap "Add." Check the device manual for the port.

The NMEA 0183 TCP output in signalk-server uses port `10110` by default ([official source](https://github.com/SignalK/signalk-server/blob/master/src/interfaces/nmea-tcp.ts)). If the server uses a different port, enter that port instead.

## Choose which data to use

DingHai can receive position and speed, heading, wind, and depth. Open each of these four items at the top of "Data Sources" to choose which device supplies that data. Adding a data source does not automatically select any of its devices.

## Local Network permission

Discovering and connecting to data sources on your boat's local network requires Local Network permission. If you previously denied it, allow DingHai to access the local network in system Settings.
