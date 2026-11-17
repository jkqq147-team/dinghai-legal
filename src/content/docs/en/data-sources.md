---
title: Connect Data Sources
description: Add Signal K, NMEA 0183 TCP, or NMEA 0183 UDP data sources in DingHai.
---

DingHai supports Signal K, NMEA 0183 TCP, and NMEA 0183 UDP data sources.

## Signal K

1. Connect the device running DingHai to the same Wi-Fi network as the Signal K server, then open "Data Sources." Discovered Signal K services appear under "在这个网络上找到" (services found on this network). Tap the "+" on the right to add one.
2. If the server is not found, open "手动输入地址" (manual address entry), select "Signal K" as the type, and enter the server's `IP:port`.
3. If the server has security enabled, enter your username and password, then tap "Add."

## NMEA 0183 TCP

Open "手动输入地址" (manual address entry), select "NMEA 0183 TCP" as the type, enter the gateway or server's `IP:port`, then tap "Add." Check the device manual for the port.

The NMEA 0183 TCP output in signalk-server uses port `10110` by default ([official source](https://github.com/SignalK/signalk-server/blob/master/src/interfaces/nmea-tcp.ts)). If the server uses a different port, enter that port instead.

## NMEA 0183 UDP

Open "手动输入地址" (manual address entry), select "NMEA 0183 UDP" as the type, enter the address in one of the forms below, then tap "Add." DingHai receives data on that port of this device, and the gateway must be on the same network as this device. Check the device manual for the port.

- `gateway IPv4:port`: receives only data sent from that address;
- `0.0.0.0:port`: accepts data from any sender;
- `multicast address:port`: joins that multicast group.

While "Data Sources" is open, DingHai listens for broadcasts on ports `10110` and `2000`: `10110` is the [port IANA registered for NMEA 0183](https://www.iana.org/assignments/service-names-port-numbers/), and `2000` is the [port Digital Yacht gateways send UDP on](https://digitalyacht.support/tutorials/how-to-configure-apps-software/). Gateways sending NMEA 0183 sentences on these ports appear under "在这个网络上找到" (found on this network); tap the "+" on the right to add one. DingHai does not automatically add or select discovered gateways.

## Choose which data to use

DingHai can receive position and speed, heading, wind, and depth. Open each of these four items at the top of "Data Sources" to choose which device supplies that data. Adding a data source does not automatically select any of its devices.

## Local Network permission

Discovering data sources on your boat's local network, and connecting to them or receiving their data, requires Local Network permission. If you previously denied it, allow DingHai to access the local network in system Settings.
