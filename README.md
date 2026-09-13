# F-23B Black Widow II

An experimental community aircraft for DCS World, combining an F-23 exterior
and flight model with the installed F/A-18C Hornet cockpit and avionics.

This repository contains the software source for the preview. Aircraft downloads
will be provided through [Releases](https://github.com/Coaokalo/f23b-public/releases).
The repository is currently private and its preview release is a draft.

## Installation

The preview targets Windows and DCS **2.9.29.27468**. It requires an installed,
activated **DCS: F/A-18C Hornet** and **Python 3.11+**.

Read [INSTALL.md](INSTALL.md) before installing. Download the aircraft ZIP from
the release assets; GitHub's automatic source archives cannot be installed as an
aircraft. Both Saved Games module folders and the included missile installer are
required. The installer changes AIM-120B and AIM-9X definitions globally and can
affect other aircraft and multiplayer integrity checks. It includes verification
and restoration commands.

## Preview status

The preview includes experimental flight forces, internal weapon bays, MALICE,
project AIM-9X Block II definitions, and exterior lighting and burner effects.
It is intended for single-player testing. Full-envelope flight, VR, multiplayer,
and a fresh-user install/fly/remove cycle remain unqualified. Post-launch
datalink/LOAL for Block II is not implemented.

See [known limitations](KNOWN_ISSUES.md) and the
[release status](docs/RELEASE_STATUS.md) for the remaining download checks.

## Source and development

- [Build and test](BUILDING.md)
- [Source layout](docs/SOURCE_LAYOUT.md)
- [Contributing](CONTRIBUTING.md)
- [Software license](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md)
- [Asset licensing](LICENSE-ASSETS.md)

The source tree includes the flight bridge, flight-model library, generators,
tests, installer, and the Lua shipped with the preview. Visual assets are
distributed separately under their own terms and are absent from this source
tree. [SOURCE_ORIGIN.json](SOURCE_ORIGIN.json) identifies the inherited source
snapshot and hashes. The development repository's Git history is not imported.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
