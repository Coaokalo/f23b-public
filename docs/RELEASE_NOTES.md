# F-23B v1.4

Native Hornet radar, datalink and SA in a stealth airframe, with sequenced internal bays, MALICE and project AIM-9X Block II.
Current installs change no DCS game files.

![F-23B v1.4 in DCS](https://raw.githubusercontent.com/Coaokalo/f23b-public/v1.4/docs/images/f23b-exterior.jpg)

## Two equal install options

| Method | Download |
| --- | --- |
| Copy and paste | [F-23B-v1.4.zip](https://github.com/Coaokalo/f23b-public/releases/latest/download/F-23B-v1.4.zip) |
| Installer | [F-23B-v1.4-Setup.exe](https://github.com/Coaokalo/f23b-public/releases/latest/download/F-23B-v1.4-Setup.exe), which does the same thing for you |

Both contain identical aircraft, weapons, ten liveries and documentation. No separate Python installation is needed.
Requires Windows and an installed, activated **DCS: F/A-18C Hornet**.
Weapon and radar connection: **DCS 2.9.30.28738**. Single-player; VR and multiplayer not yet tested.

**Manual install**

- Close DCS.
- Extract the ZIP and drag its contents into `Saved Games\DCS`.

**Manual upgrade**

- Close DCS and delete `Mods\aircraft\F-23B` and `Mods\aircraft\F-23B-Player` first.
- Copy the extracted contents into the same profile.

**Manual removal**

- Close DCS and delete those two aircraft folders.
- Delete the supplied `F23B-...` folders in `Liveries\F-23B` and, optionally, `F-23B-docs`.

**September 17/18 users:** run DCS Repair with **Check all files (slow)** once before your first manual upgrade.
Copying the ZIP cannot undo their game-file changes. Setup can remove verified old changes automatically.
[Full instructions, mod managers and switching methods](https://github.com/Coaokalo/f23b-public/blob/main/INSTALL.md).

For setup, close DCS, run the EXE, confirm both folders, then select **Install / Repair**.
Windows warns about the unsigned installer? Use the ZIP.

## New in v1.4

- Current DCS support, with the existing flight and weapon tuning retained.
- New afterburner visuals and ten liveries. Quick Start missions use the Langley scheme.
- Equal ZIP and setup options. Setup adopts unchanged, known manual installations.
- Installation on other DCS builds, with a clear in-game **connection OFF** message when the native connection cannot start.
- Administrator permission only for removal of earlier F-23B game-file changes.
- A [one-page illustrated pilot guide](https://github.com/Coaokalo/f23b-public/blob/main/docs/PILOT_GUIDE.md) and [Discussions for feedback](https://github.com/Coaokalo/f23b-public/discussions).

## Since the September 18 release

The in-memory connection replaced the old DCS game-file edits.
MALICE gained loft, a second motor pulse, and long-range loft control. An owner flight recorded a **336-mile A-50 kill** with continuing support.
AI F-23Bs fire both custom weapons. Friendly aircraft are excluded from automatic target ranking, and SA extends to **640 NM**.
Ground and water collision, Hornet-radius speed-limited steering, a stiffer nose strut, and a single pilot-view canopy frame are retained.

The 336-mile result is one supported flight, not a guaranteed range. Exact 350-mile shots remain unverified.
The coasting-apex estimate is not a hard altitude cap; the recorded long shot reached about 158,000 feet.

## Limits and help

![Ten included liveries](https://raw.githubusercontent.com/Coaokalo/f23b-public/v1.4/docs/images/f23b-liveries.jpg)

![Afterburner at dusk](https://raw.githubusercontent.com/Coaokalo/f23b-public/v1.4/docs/images/f23b-afterburner.jpg)

[Bay doors and MALICE launch — short DCS clip](https://github.com/Coaokalo/f23b-public/releases/latest/download/F-23B-v1.4-Bay-Launch.mp4)

Block II helmet cueing and post-launch datalink/lock-on after launch are not implemented.
AI uses the extended MALICE energy profile when the player also flies an F-23B.
On a mismatched DCS build, custom weapons, radar upgrades and SA 640 are unavailable.
Flight, the native cockpit and radar, bays, lights and liveries remain available.

[Known limits](https://github.com/Coaokalo/f23b-public/blob/main/KNOWN_ISSUES.md) ·
[Feedback](https://github.com/Coaokalo/f23b-public/discussions) ·
[Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)

For DCS 2.9.29.27468, keep the [September 29 / v1.1 release](https://github.com/Coaokalo/f23b-public/releases/tag/release-2026-09-29).

## Source and licences

[Corresponding software source](https://github.com/Coaokalo/f23b-public/releases/download/v1.4/F-23B-v1.4-source.zip) ·
[SHA-256 checksums](https://github.com/Coaokalo/f23b-public/releases/download/v1.4/SHA256SUMS.txt)

Software: GPL-3.0-or-later, with retained file-level MIT grants. Eligible original documentation/content: CC BY-SA 4.0.
Purchased models and derived textures retain separate terms. Editable vendor sources are not included.
Credits include Grinnelli Designs and Branden Hooper for flight-model source, and SytaPastel for the licensed YF-23 visuals.
[Full notices](https://github.com/Coaokalo/f23b-public/blob/main/THIRD_PARTY_NOTICES.md) ·
[Asset terms](https://github.com/Coaokalo/f23b-public/blob/main/LICENSE-ASSETS.md)

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
