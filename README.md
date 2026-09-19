# F-23B Black Widow II

A community aircraft for DCS World with custom F-23 flight dynamics and the
F/A-18C Hornet cockpit and avionics.

Includes independent AIM-424 MALICE and AIM-9X Block II weapons. Stock missiles
retain their original behavior.

**[Download and release details](https://github.com/Coaokalo/f23b-public/releases/tag/test-2026-09-18)** ·
[Installation & removal](INSTALL.md) ·
[Known limitations](KNOWN_ISSUES.md) ·
[Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)

| Requirement | Supported configuration |
| --- | --- |
| Operating system | Windows 64-bit |
| DCS World | **2.9.29.27468** |
| Required module | **DCS: F/A-18C Hornet**, installed and activated |
| Play mode | Single-player; multiplayer and VR remain unverified |

The Windows installer includes the aircraft and custom weapons. No separate Python installation is needed.

![F-23B above the clouds at sunset](docs/images/f23b-exterior.jpg)

## Features

- Custom F-23 flight forces with the Hornet pilot cockpit, avionics, and controls.
- Trigger-operated internal weapon bays, MALICE, and project AIM-9X Block II.
- Exterior lighting, combat-mode light blackout, and afterburner effects.
- Three Caucasus Quick Start missions: Cold Start, Hot Start, and Free Flight.

## Get flying

1. Download **F23B-preview-2026-09-18-Setup.exe** from
   [the release page](https://github.com/Coaokalo/f23b-public/releases/tag/test-2026-09-18).
2. Close DCS, its updater, and ModelViewer.
3. Run the installer and confirm your DCS game folder and Saved Games profile.
4. Select **Install / Repair**.
5. Start DCS and select an F-23B Quick Start mission.

Setup installs an F-23B-only cockpit connection and may affect multiplayer
integrity checks. Keep the installer for repair and removal.
See [installation and removal](INSTALL.md).

![Hornet pilot cockpit used by the F-23B above sunset clouds](docs/images/f23b-cockpit.jpg)

*DCS development captures. Some visual details can differ from this release.*

## Known limitations

Full flight and weapon envelopes, VR, and multiplayer compatibility are not verified.
Block II helmet cueing and post-launch datalink/LOAL are not implemented.
The installer is unsigned. DCS updates require a compatible F-23B release.
See [known limitations](KNOWN_ISSUES.md).

Found a problem? [Open a bug report](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)
with your release version, DCS version, and steps to reproduce it.

## Licensing and credits

The combined software uses **GPL-3.0-or-later**. Individual files with MIT notices retain their MIT grant.
Original documentation and eligible original creative content use **CC BY-SA 4.0**.
Purchased models, derived textures, and third-party content have separate terms.

Credits include **Grinnelli Designs and Branden Hooper** for the F-22A flight-model source,
and **SytaPastel** for the licensed YF-23 visual model.

[Software license](LICENSE) · [Content and asset licenses](LICENSE-ASSETS.md) ·
[Full credits and third-party notices](THIRD_PARTY_NOTICES.md)

## Development

[Build and test](BUILDING.md) · [Source layout](docs/SOURCE_LAYOUT.md) ·
[Contributing](CONTRIBUTING.md)

This repository includes the flight-model source, Lua, installer, tests, and
documentation. Runtime models and textures are in the aircraft download under
their respective terms. The corresponding software source ZIP is on the release page.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
