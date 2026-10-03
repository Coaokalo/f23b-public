The F-23B Black Widow II aircraft for DCS World with custom flight dynamics and F/A-18C Hornet avionics.
Includes internal weapon bays, AIM-424 MALICE, and project AIM-9X Block II.

## [Download the Windows installer](https://github.com/Coaokalo/f23b-public/releases/download/release-2026-10-03/F23B-2026-10-03-Setup.exe)

**Aircraft and weapons included · No separate Python installation**

| Requirement | Supported configuration |
| --- | --- |
| Operating system | Windows 64-bit |
| DCS World | **2.9.30.28536** |
| Required module | **DCS: F/A-18C Hornet**, installed and activated |
| Play mode | Single-player |

![F-23B Black Widow II above the clouds in DCS World](https://raw.githubusercontent.com/Coaokalo/f23b-public/a25e04b/docs/images/f23b-exterior.jpg)

*Development capture. Some visual details can differ from this release.*

## New in this release

- **MALICE long-range loft control.** Extra loft pauses when the estimated coasting
  apex reaches 98,400 feet. A single-player flight confirmed an A-50 kill from
  336.4 statute miles with continuing target updates, plus a Tu-95MS kill from 76.2 miles.
  Exact 350-mile shots and the full engagement envelope remain unverified.
- **Updated MALICE launch-zone indications.** The displayed launch envelope now
  uses the revised long-range anchors. Second pulse timing is unchanged: seeker search after boost burnout.
- **Installer upgrades.** Install / Repair accepts an installed October 1 release and preserves the DCS game files.

The coasting estimate is not a hard altitude cap. The successful long shot reached about 158,000 feet.
Launch conditions and continued target support affect the result.

Carried over from the October 1 release:

- **DCS World 2.9.30.28536 support.** MALICE, Block II, the 640 NM SA scale and the friendly-track filter remain connected.
  On DCS 2.9.29.27468, use the [September 29 release](https://github.com/Coaokalo/f23b-public/releases/tag/release-2026-09-29).

Carried over from the September 29 release:

- **No DCS game-file changes.** Setup installs only into your Saved Games profile.
  Upgrading removes the cockpit connection that the September 18 release added.
- **Weapons:** MALICE uses the native Hornet radar and missile support, with a
  lofted profile and a second motor pulse. AI F-23Bs now fire MALICE and Block II.
- **Radar:** The SA page scale now goes to 640 NM.
- **Airframe:** The aircraft now crashes on ground and water impact.
- **Ground handling:** Nosewheel steering turns on a Hornet-like radius. Steering
  authority reduces with speed to prevent ground loops. A stiffer nose strut
  prevents bottoming and gear damage in hard braking.
- **Smaller download:** unused textures and development files are removed.

## Included

- **Aircraft:** Custom F-23 flight dynamics with the F/A-18C cockpit, avionics, and controls.
- **Weapons:** AIM-424 MALICE and project AIM-9X Block II. Stock missiles remain unchanged.
- **Systems:** Trigger-operated weapon bays, exterior lights, and afterburner effects.
- **Missions:** Caucasus Cold Start, Hot Start, and Free Flight.

## Installation

1. Close DCS, its updater, and ModelViewer.
2. Run the Windows installer.
3. Confirm your DCS game folder and Saved Games profile.
4. Select **Install / Repair**.

Start DCS after installation. Select an **F-23B Quick Start** mission.
Upgrading from an earlier F-23B release uses the same steps.

Keep the installer for repair and removal. Your existing Hornet controls apply.

[Full installation and removal guide](https://github.com/Coaokalo/f23b-public/blob/main/INSTALL.md)

## Known limitations

- MALICE's coasting-apex threshold is not a hard altitude cap. Exact 350-mile shots are unverified.
- Full flight and weapon envelopes are not verified.
- AIM-9X Block II helmet cueing and post-launch datalink/lock-on after launch are not implemented.
- AI F-23Bs use the MALICE energy profile only when the player also flies an F-23B.
- VR and multiplayer compatibility are unverified.
- The installer is unsigned. DCS updates require a compatible F-23B release.

[Known issues](https://github.com/Coaokalo/f23b-public/blob/main/KNOWN_ISSUES.md) · [Report a problem](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)

## Licensing and credits

Different parts of this release have different licenses.

| Content | License |
| --- | --- |
| Combined software | **GPL-3.0-or-later**. Individual source files with MIT notices retain their MIT grant. See the [software license](https://github.com/Coaokalo/f23b-public/blob/main/LICENSE). |
| Original documentation and eligible original creative content | **CC BY-SA 4.0**, with attribution to F-23B project contributors. See the [content terms](https://github.com/Coaokalo/f23b-public/blob/main/LICENSE-ASSETS.md). |
| Purchased models, derived textures, and third-party content | Separate license terms apply. The software license grants no additional rights to extract or redistribute these assets. |

The flight-model adaptation uses source from **Grinnelli Designs F-22A**, including work by **Branden Hooper**.
The licensed YF-23 visual model is by **SytaPastel** on CGTrader.
F-23B project contributors provide the adaptation and original project content.

The release includes a corresponding software source ZIP.
DCS and the Hornet remain separate required products. Their proprietary files are not included in this download.

[Third-party notices and source credits](https://github.com/Coaokalo/f23b-public/blob/main/THIRD_PARTY_NOTICES.md) · [Asset license details](https://github.com/Coaokalo/f23b-public/blob/main/LICENSE-ASSETS.md)

<details>
<summary>Other downloads</summary>

The Windows installer is the normal player download.

| File | Purpose |
| --- | --- |
| [Aircraft ZIP](https://github.com/Coaokalo/f23b-public/releases/download/release-2026-10-03/F23B-2026-10-03.zip) | Installer payload. The EXE already includes this file. |
| [Source ZIP](https://github.com/Coaokalo/f23b-public/releases/download/release-2026-10-03/F23B-2026-10-03-source.zip) | Software source for this release. |
| [SHA256 checksums](https://github.com/Coaokalo/f23b-public/releases/download/release-2026-10-03/SHA256SUMS.txt) | File checksums for download verification. |

GitHub's automatic **Source code** archives are repository snapshots. They are not aircraft installation packages.

</details>

---

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
