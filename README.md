# F-23B Black Widow II

An experimental community aircraft for DCS World: an F-23 airframe and custom
flight model paired with the F/A-18C Hornet cockpit and avionics.

**[Download the aircraft](https://github.com/Coaokalo/f23b-public/releases)** ·
[Installation & removal](INSTALL.md) ·
[Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)

**Requires Windows, DCS World 2.9.29.27468, an installed and activated
DCS: F/A-18C Hornet, and Python 3.11+.**

![F-23B above the clouds at sunset](docs/images/f23b-exterior.jpg)

## Included in the preview

- Custom F-23 flight forces with the Hornet pilot cockpit, avionics, and controls.
- Trigger-operated internal weapon bays, MALICE, and project AIM-9X Block II.
- Exterior lighting, combat-mode light blackout, and afterburner effects.
- Three Caucasus Quick Start missions: Cold Start, Hot Start, and Free Flight.

## Get flying

1. Open [Releases](https://github.com/Coaokalo/f23b-public/releases) and download
   **F23B-preview-2026-09-13.zip**. The source ZIP is for development.
2. Extract it and copy **both** `F-23B` and `F-23B-Player` into your
   `Saved Games/DCS/Mods/aircraft` folder.
3. Run the included missile installer and verification commands in
   [INSTALL.md](INSTALL.md), then select an F-23B Quick Start mission in DCS.

**The required missile installer changes AIM-120B and AIM-9X globally**, including
their use on other aircraft, and may affect multiplayer integrity checks.
[Installation and undo instructions](INSTALL.md) cover both parts of the mod.

![Hornet pilot cockpit used by the F-23B above sunset clouds](docs/images/f23b-cockpit.jpg)

*DCS development captures. Small visual details may differ from this preview.*

## Experimental preview

This release is intended for single-player use. Flight behavior is experimental;
full-envelope accuracy, VR, and multiplayer compatibility are not established.
Block II post-launch datalink/LOAL is not implemented.
See [known limitations](KNOWN_ISSUES.md).

Found a problem? [Open a bug report](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)
with your preview build, DCS version, and steps to reproduce it.

## Source and credits

[Build and test](BUILDING.md) · [Source layout](docs/SOURCE_LAYOUT.md) ·
[Contributing](CONTRIBUTING.md) · [Software license](LICENSE) ·
[Third-party notices](THIRD_PARTY_NOTICES.md) · [Asset licensing](LICENSE-ASSETS.md)

This repository includes the flight-model source, Lua, installer, tests, and
documentation. Runtime models and textures are in the aircraft download under
their respective terms. The corresponding source ZIP accompanies each preview.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
