---
title: Privacy Policy
description: DingHai Privacy Policy covering location data, anchor-watch records and tracks, accounts and anchor-watch record sync, cross-device viewing and alert notifications, retention, and deletion.
---

DingHai does not use advertising or third-party analytics services. You may choose to use a DingHai account with Sign in with Apple; local anchor watch requires no account and does not depend on DingHai servers.

<p class="meta">Effective date: October 15, 2026</p>

## 1. Scope

This policy applies to the DingHai app for iOS and iPadOS and to the privacy and support pages on this website.

## 2. On-device location processing and anchor-watch records

While anchor watch is active, DingHai processes your precise vessel position on your device to:

- place an anchor on the map and calculate the distance between the vessel and anchor;
- determine whether the vessel has moved beyond your alarm radius;
- draw the movement track for the current anchor watch; and
- continue monitoring on the Lock Screen or in the background and alert you to a potential anchor drag.

Anchor positions, anchor-watch tracks, alarm radii, times, display preferences, and anchor-watch photos you explicitly select are stored first in the app's local data container. DingHai does not synchronize these records through iCloud or CloudKit.

After you sign in to a DingHai account with "Sync Anchor-Watch Records" turned on, anchor-watch records are uploaded to DingHai servers and synchronized to devices signed in to the same DingHai account, as described in Section 4.

Local location processing, distance decisions, and alarms always run on the device. Local anchor watch continues when the account, network, or DingHai servers are unavailable.

Only after you explicitly start track recording does DingHai save the positions, times, position sources, and position accuracy along your route on the device, to show the track and your track history. Tracks currently remain on the device only; they are not uploaded to DingHai servers and are not included in account sync.

If you enter the address of a Signal K service on your boat in the app, DingHai connects to that service to receive onboard data such as vessel position, heading, speed over ground, wind, and depth for marine features including anchor watch. Connecting to a service on your boat's local network requires the iOS Local Network permission. When Signal K is the position source, anchor-watch tracks and tracks record that position source. DingHai does not send your anchor-watch records, tracks, or account information to the Signal K service. After you sign in to a DingHai account, the vessel name and Signal K connection address are synchronized as a vessel profile to DingHai servers and to devices on the same account; vessel-profile sync is not controlled by the "Sync Anchor-Watch Records" switch. The current vessel name is also written into each anchor-watch record and is synchronized with it.

## 3. DingHai accounts and authentication

Sign in with Apple is optional. After you sign in, DingHai servers process:

- the user identifier Apple provides to DingHai, and an internal DingHai account identifier derived from it;
- a device identifier, platform, and system-provided device display name;
- hashes, expiry times, and revocation status for DingHai access and refresh sessions; and
- an encrypted Apple refresh token used only to revoke Apple authorization when you delete the account.

DingHai does not request your name or email address from Apple when you sign in, and never asks for or stores your Apple ID password. DingHai session tokens on the device are stored in the Keychain.

## 4. Anchor-watch record sync, cross-device viewing, and alert notifications

After you sign in, the "Sync Anchor-Watch Records" switch is on by default. While it is on, each anchor-watch record is an append-only log of facts: start, position, alarm acknowledgement, alarm-radius change, monitoring interruption, end, and similar facts are uploaded to DingHai servers after they are written on the device. An anchor watch in progress is uploaded continuously; uploading does not wait for the watch to end. Anchor-watch records that were saved only on the device before you signed in, or while sync was off, are also uploaded once you are signed in with sync on.

Uploaded content includes: the start time, anchor coordinates, alarm radius, and vessel name; for each position point, its coordinates, time, position source, position accuracy, distance from the anchor, and the alarm radius at that time; the times of alarm acknowledgements, alarm-radius changes, monitoring interruptions, and the end; the record name (an automatically generated place name or a name you enter); photos you explicitly add to the record; and the identifier of the device that wrote each fact.

Positions, alarm acknowledgements, alarm-radius changes, monitoring interruptions, and the end can be written only by the device that started the anchor watch; an anchor watch cannot be remotely controlled by, or handed off to, another device. After an anchor watch ends, devices on the same account can change the record name and photo or delete the record.

Other devices on the same account with sync on receive these facts over a live connection while the app is in the foreground, to view an anchor watch in progress and keep a copy of the record. That connection closes when the app goes to the background, sync is turned off, or the device signs out.

While an anchor watch is in progress, if the first position reported by the device that started it is already outside the alarm radius, or a new position moves from inside to outside the alarm radius, or DingHai servers have received no new position for about 5 minutes, the server sends an alert through the Apple Push Notification service (APNs) to the account's other devices that are signed in, have sync on, and have completed push registration; the alert is never sent to the device that started the anchor watch. Only positions that are still current when DingHai servers receive them count toward these checks; an older position that arrives late is kept only as part of the record and neither triggers an out-of-range alert nor restarts the 5-minute timer. When a record name is available, the alert title contains the vessel name and record name; otherwise, it contains only the vessel name. For this purpose the server stores those devices' APNs push tokens and push environment. When you turn sync off or sign out, the app asks the server to delete that device's push token; the server also deletes the token when the account is deleted or APNs reports the token as no longer valid. Notifications are a supplementary feature and may be delayed or lost; DingHai does not guarantee delivery, and they must not replace the local alarm on the device aboard.

You can turn off "Sync Anchor-Watch Records" on the app's account screen. When it is off, the app stops uploading this device's anchor-watch facts, stops receiving facts from other devices, and asks the server to delete this device's push token. No records are deleted on the device or on the server as a result; facts not yet uploaded stay on the device and resume uploading when sync is turned back on. While sync is off, copies on other devices are not updated. If this device is running an anchor watch when sync is turned off, after about 5 minutes the server sends a "no position received" alert to the account's other devices with sync on. Local anchor watch is unaffected.

Anchor-watch data is not used for advertising, profiling, or cross-app tracking. Tracks are not part of this sync.

## 5. Apple and infrastructure services

Apple map styles use MapKit; the GSHHG coastline basemap, vector charts, and raster charts are rendered on the device from local data using the MapLibre library.
GSHHG basemap downloads and update checks fetch a manifest from resources.dinghai.app; during installation, the app downloads the package specified by that manifest.
Device location, notifications, and Live Activities use Apple system services, including Core Location, UserNotifications, and ActivityKit.
After an anchor watch starts, DingHai uses MapKit to look up a nearby place name for the anchor coordinates as the record's automatic name. Cross-device alerts are sent through APNs. Apple's own privacy policy applies to its processing through those services.

DingHai uses Cloudflare Workers, D1, R2, and Durable Objects to provide accounts, anchor-watch record sync, and alert notifications: D1 stores accounts, identity links, devices, sessions, push tokens, and vessel profiles; one Durable Object per account stores that account's anchor-watch fact log; and R2 stores anchor-watch photos. DingHai includes no advertising SDKs or third-party analytics SDKs.

## 6. Permissions

- <strong>Location while using the app:</strong> shows the vessel position, places the anchor, calculates distance, or records a track you explicitly start. Track recording needs only this permission; once started, it continues while locked or in another app and does not require Always.
- <strong>Always and precise location:</strong> continues anchor watch while locked, in another app, or when iOS wakes the app for a location condition.
- <strong>Notifications:</strong> alerts you when an anchor-drag risk is detected on this device; after you sign in with sync on, also shows alerts about anchor watches on the account's other devices that leave the alarm radius or have sent no new position for about 5 minutes (see Section 4).
- <strong>Local Network:</strong> connects to the Signal K service on your boat that you enter and receives onboard data.

DingHai does not request microphone, camera, or contacts access and does not record audio. Only photos you explicitly choose through the system photo picker are added to anchor-watch records.

## 7. Retention, deletion, and control

Ended anchor-watch records remain until you delete them individually in the app. On other devices, an anchor watch with no end can be shown as "unfinished" after more than 7 days without a new position (counted from the start if no position has been received).
The device that started the watch still restores its newest local watch with no end, regardless of age, and excludes it from the logbook. The app currently offers no option to delete an anchor-watch record without an end.
When you delete a synchronized record, the server deletes all of that record's facts and photos and keeps only a deletion marker with no anchor-watch content, so that the account's other devices delete their copies. A record deleted while sync is off is deleted from the server after sync is turned back on.

Deleting the app removes the anchor-watch records, photos, and tracks in the app's data on that device, including records not yet uploaded; anchor-watch records already uploaded to your DingHai account remain on DingHai servers and synchronize to the device again after reinstallation once you sign in to the same account with sync on.

You can delete tracks individually in the app. Signing out or deleting your DingHai account does not delete tracks on the device.

You can sign out or delete the DingHai account from the account screen. When you sign out, the server revokes this device's DingHai session, closes its live connection, and deletes its push token; the app then removes the anchor-watch records and photos belonging to that account from the current device, including records whose upload had started but not finished, except an anchor watch in progress on this device. The records on DingHai servers are unaffected and synchronize again when you sign back in.

When you delete the account, DingHai servers empty the account's anchor-watch fact log and close all of its live connections, delete the account's anchor-watch photos, revoke Apple authorization, and delete the account, Apple identity link, devices, DingHai sessions, push tokens, and vessel profiles. The app then removes the anchor-watch records and photos belonging to that account from the current device (except an anchor watch in progress on this device) and clears the DingHai session from the Keychain.

Once you are signed in with sync on, the app assigns anchor-watch records that were created on the device before you signed in, or while sync was off, and not yet uploaded, to the current account and uploads them. If you later sign out or delete the account, those records are handled together with the account's other records: account deletion deletes them from DingHai servers and the current device, and signing out removes them from the current device. Only anchor-watch records that have never been synchronized while signed in with sync on since they were created, and so belong to no account, are unaffected by signing out or deleting the account. Synchronized local copies on other devices are not automatically removed by account deletion.

You can revoke location or notification access at any time in Settings. Revoking a permission required for anchor watch will stop the corresponding protection.

## 8. Use and sharing

DingHai processes the data described above only to provide accounts, anchor-watch record sync, cross-device viewing and alert notifications, security, and support. DingHai does not sell personal data or share it with advertising, analytics, or data-broker services. Apart from Apple and Cloudflare processing required to provide system and infrastructure services, DingHai does not provide this data to other third parties.

This website uses no cookies, analytics, tracking pixels, or third-party fonts.

## 9. Intended use

DingHai is an anchor-watch aid. It does not provide emergency rescue or vessel control and cannot replace
safe anchoring procedures, a human watch, or compliant marine equipment. Always maintain independent safety measures.

## 10. Updates and contact

If our data practices materially change, we will update this policy, this effective date, and the App Store Privacy Nutrition Label together, and provide an in-app notice when appropriate.

For privacy questions, contact the development team through
[GitHub Issues](https://github.com/jkqq147-team/dinghai-legal/issues).
Do not include vessel positions, tracks, or other sensitive information in a public issue.
