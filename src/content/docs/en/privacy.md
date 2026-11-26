---
title: Privacy Policy
description: DingHai Privacy Policy covering what data the app handles, what it is used for, where it is stored, who can see it, and what you control.
---

DingHai does not use advertising or third-party analytics services. You may choose to use a DingHai account with Sign in with Apple; local anchor watch requires no account and does not depend on DingHai servers.

<p class="meta">Effective date: November 21, 2026</p>

## 1. Scope

This policy applies to the DingHai app for iOS and iPadOS and to the privacy and support pages on this website.

## 2. What data DingHai handles and why

- <strong>Location:</strong> During anchor watch, while you use the map in the foreground, and while you record a track, DingHai obtains the device's location (including precise location) according to the location permission you have granted, or uses the vessel position from the onboard data source you select. The position is used to place the anchor, calculate the distance to it, determine whether the boat is outside the alarm radius, draw tracks, and continue anchor watch on the Lock Screen or in the background and alert you to a potential anchor drag. Ending an anchor watch does not stop location still in use by the map or a track.
- <strong>Anchor-watch records:</strong> Each anchor watch is saved as one record, including the anchor point, alarm radius, start and end times, the position fixes of the anchor-watch track and the watch status derived from them, your alarm acknowledgements, the identifier and name of the device that started the watch (which may be a vessel name in older records), and the record name and any photo you explicitly add. Records are used to view an anchor watch in progress and your anchor-watch history.
- <strong>Tracks:</strong> Voyage tracks you explicitly record or import from a GPX file, used to show your tracks and track history.
- <strong>Map marks:</strong> Marks you save or import from a GPX file, including their position, name, kind, and any note, used to show them on the map.
- <strong>Search:</strong> Coordinates and map links you type or explicitly paste are parsed on the device; results you select are saved as recent searches.
- <strong>Onboard data sources:</strong> After you add a Signal K or NMEA 0183 data source, DingHai receives onboard data from it, such as vessel position, heading, speed over ground, wind, and depth, for marine features including anchor watch. DingHai saves the data source's address, the name you set, and any Signal K username and password you enter; a vessel name reported by a Signal K data source is used on this device.
- <strong>Account information:</strong> Sign in with Apple is optional. After you sign in, DingHai processes the user identifier Apple provides to DingHai and a DingHai account identifier derived from it, a device identifier, platform, and system-provided device name, sign-in session information, and an encrypted Apple authorization credential (used only to ask Apple to revoke authorization when you delete the account); when sync is on, this also includes the push token used to send alerts to this device. DingHai does not request your name or email address from Apple when you sign in, and never asks for or stores your Apple ID password.
- <strong>Diagnostic reports:</strong> System-generated crash and performance reports used for troubleshooting; see Section 7.

## 3. Where data is stored

### Your device

Location processing, distance decisions, and alarms for local anchor watch run on the device. Local anchor watch can continue when the account, network, or DingHai servers are unavailable.

Anchor-watch records, photos, tracks, map marks, recent searches, data source settings, and display preferences are stored in the app's local data; Signal K usernames and passwords and DingHai sign-in credentials are stored in the device Keychain. DingHai does not sync anchor-watch records through iCloud or CloudKit. DingHai does not upload tracks, recent searches, or data source settings to DingHai servers or sync them through the DingHai account.

### DingHai servers

DingHai servers run on Cloudflare. After you sign in, the servers store the account information listed in Section 2.

When you're signed in and "Sync Anchor-Watch Records" is on (the default), anchor-watch records on this device that are assigned to the current account are uploaded to DingHai servers, including an anchor watch in progress and the position fixes of its track; record names, photos, and deletions are uploaded as well. These records are synchronized to other devices on the same account that have sync on. Anchor-watch records on this device that are not yet assigned to any account are assigned to the current account and uploaded. Anything that can't be uploaded yet stays on this device and is retried later. DingHai does not automatically remove anchor-watch records from its servers after a set period; you can remove them by deleting a record or deleting the account (see Section 6).

Diagnostic reports are also sent to DingHai servers (see Section 7). For troubleshooting, DingHai servers have Cloudflare's request logging turned on, which can record the time and URL of a request; the URL can contain a record or account identifier.

### Apple services

- Device location, notifications, and Live Activities use Apple system services, including Core Location, UserNotifications, and ActivityKit.
- The chart coverage map and the NOAA Charts map use MapKit: when you view a chart coverage map or the NOAA Charts map in “Offline Charts”, DingHai requests the map of the area shown from Apple Maps services. When an anchor watch starts, DingHai sends the anchor coordinates to Apple Maps services to look up a nearby place name as the anchor-watch record's automatic name.
- Account sign-in uses Sign in with Apple; cross-device alerts are sent through the Apple Push Notification service (APNs).

Apple's own privacy policy applies to its processing through those services.

### Data downloads and onboard data sources

The DingHai Basemap, satellite imagery, vector charts, and raster charts are read and rendered on the device by MapLibre. To obtain this data and tidal data, DingHai connects to:

- <strong>resources.dinghai.app:</strong> when you select sea areas, download the DingHai Basemap, satellite imagery, or the recommended tidal data, or check for their updates. When the introduction ends, if you allow location access and the DingHai Basemap for your sea area has not been downloaded, DingHai also asks it for the download size of that sea area.
- <strong>charts.noaa.gov or [www.charts.noaa.gov](https://www.charts.noaa.gov):</strong> when you download NOAA charts.
- <strong>The URL you enter and its redirect destinations:</strong> when you choose "Download from Address" for charts or tidal data.

Checking or updating downloaded data also accesses the corresponding sources. Services receiving these requests can see network information such as your connection's public IP address, the resources requested, and request times, and the sea area you selected or are roughly in may be inferred from the resources requested; DingHai does not add your coordinates to these requests and does not attach DingHai account sign-in credentials or anchor-watch records.

After you add an onboard data source, DingHai connects to the Signal K or NMEA 0183 address you enter, or receives gateway broadcasts on this device; when you open "Data Sources", DingHai also looks for data sources on the local network that you can add. When connecting, DingHai uses the Signal K username and password you enter to authenticate with the Signal K service you configured; they are not routed through DingHai servers. DingHai does not send your anchor-watch records, tracks, or DingHai account information to onboard data sources.

## 4. Who can see this data

- <strong>Your other devices:</strong> Other devices on the same account with sync on receive anchor-watch records while the app is in the foreground, to view an anchor watch in progress and keep a copy of the record; after an anchor watch ends, those devices can also change the record name and photo or delete the record.
- <strong>The developer:</strong> Anchor-watch records and their photos are stored on Cloudflare services used by DingHai. When troubleshooting, the developer can view an account's anchor-watch records, position fixes, and photos.
- <strong>Apple and Cloudflare:</strong> provide the system services and infrastructure services described in Section 3, respectively.
- <strong>Data sources and onboard data sources:</strong> Data sources and the services to which they redirect receive the network request information described in Section 3; Signal K servers you add receive connection requests and any login credentials you enter for those servers.

DingHai processes the data described above only to provide local anchor watch, track recording, maps and charts, tidal data, onboard data connections, accounts, anchor-watch record sync, cross-device viewing and alert notifications, security, and support. DingHai does not sell personal data or share it with advertising, analytics, or data-broker services; it includes no advertising SDKs or third-party analytics SDKs; and anchor-watch data is not used for advertising, profiling, or cross-app tracking.

This website uses no cookies, analytics, tracking pixels, or third-party fonts.

## 5. Cross-device alerts

When you're signed in with sync on, DingHai servers use the uploaded positions and, on finding that an anchor watch in progress has gone outside the alarm radius or that no position has been received for some time, may send alerts through APNs to other devices on the same account that are registered for push. The alert title contains the name of the device that started the watch, and the record name when there is one. For this purpose the servers store those devices' push tokens.

Notifications are a supplementary feature and may be delayed or lost; DingHai does not guarantee delivery, and they must not replace the local alarm on the device aboard.

## 6. What you control

### Permissions

- <strong>Location while using the app:</strong> shows the vessel position, places the anchor, calculates distance, or records a track you explicitly start. Once started, track recording continues while locked or in another app.
- <strong>Always and precise location:</strong> continues anchor watch while locked, in another app, or when iOS wakes the app for a location condition.
- <strong>Notifications:</strong> alerts you when an anchor-drag risk is detected on this device; after you sign in with sync on, also shows alerts about anchor watches on the account's other devices (see Section 5).
- <strong>Local Network:</strong> finds Signal K data sources and gateways broadcasting NMEA 0183, and receives onboard data from the Signal K, NMEA 0183 TCP or UDP sources you add.

DingHai does not request microphone, camera, or contacts access and does not record audio. Only photos you explicitly choose through the system photo picker are added to anchor-watch records; photos are saved again as JPEG within a size limit, without copying location or other metadata from the originals.

You can revoke location or notification access in Settings. Revoking a permission required for anchor watch will stop the corresponding protection.

### The sync switch

You can turn off "Sync Anchor-Watch Records" on the app's account screen. When it is off, this device stops uploading and downloading anchor-watch records and asks the server to delete its push token. No records are deleted; anything not yet uploaded stays on this device and is uploaded after you turn sync back on, and anchor watch on this device continues as usual. Records already on the servers and sync among the account's other devices are unaffected. After it is off, this device may still receive alerts already sent or sent before its push token is deleted; if it is running an anchor watch, other devices on the same account may receive a position-lost alert about it.

### Deleting records

Only ended anchor-watch records can be deleted individually in the app. When you delete a synchronized record, the server deletes that record's contents, position fixes, and photos and keeps only a deletion marker with no anchor-watch content, so that the account's other devices delete their copies. A deletion made while sync is off is submitted to the server only once this device resumes sync for the same account; if you sign out before it is submitted, the deletion does not reach the server.

You can delete tracks individually in the app, and delete individual recent searches or clear them all on the search screen.

### Signing out

You can sign out from the app's account screen. When you sign out, the server revokes this device's sign-in and deletes its push token; the app then removes the anchor-watch records and photos belonging to that account from this device, including records not yet fully uploaded, except an anchor watch in progress on this device. The records on DingHai servers are unaffected and synchronize again when you sign back in.

### Deleting the account

You can delete the DingHai account from the app's account screen. When you delete the account, DingHai servers delete the account's anchor-watch records (including any anchor watch in progress), position fixes, and photos, delete the account, Apple identity link, devices, sign-in sessions, and push tokens, and ask Apple to revoke authorization. The app then removes the anchor-watch records and photos belonging to that account from this device (except an anchor watch in progress on this device) and clears the DingHai sign-in credentials from the Keychain. Synchronized local copies on other devices are not automatically removed by account deletion.

Once you are signed in with sync on, anchor-watch records on this device that are not yet assigned to any account are assigned to the current account; anchor-watch records on this device that are not assigned to any account are unaffected by signing out or deleting the account. Signing out or deleting the account does not delete tracks on the device.

### Deleting the app

Deleting the app removes data stored within the app, including anchor-watch records not yet uploaded; it does not delete records already uploaded to DingHai servers, and after reinstallation, they synchronize to the device again once you sign in to the same account with sync on. To remove them from the servers, delete the records or delete the account.

## 7. Diagnostic reports

To investigate crashes, hangs, and overheating, DingHai first saves system-generated diagnostic reports (crash causes, where hangs occur, power usage and performance statistics, and the system version and device model) on this device, then attempts to send them automatically to DingHai's servers, along with the app version number, build number, and app identifier. DingHai does not attach account information, boat positions, or device identifiers to the reports, does not link them to your identity, and does not use them for tracking. Each time the server receives a new report, it deletes reports stored for more than 90 days.

## 8. Intended use

DingHai is an anchor-watch aid. It does not provide emergency rescue or vessel control and cannot replace
safe anchoring procedures, a human watch, or compliant marine equipment. Always maintain independent safety measures.

## 9. Updates and contact

If our data practices materially change, we will update this policy, this effective date, and the App Store Privacy Nutrition Label together, and provide an in-app notice when appropriate.

For privacy questions, contact the development team through
[GitHub Issues](https://github.com/jkqq147-team/dinghai-legal/issues).
Do not include vessel positions, tracks, or other sensitive information in a public issue.
