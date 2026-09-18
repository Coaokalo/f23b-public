# Install or remove the F-23B preview

Requires Windows, **DCS World 2.9.29.27468**, and an installed and activated
**DCS: F/A-18C Hornet**. No separate Python installation is needed.

## Install

1. Download **F23B-preview-2026-09-18-Setup.exe** from
   [Releases](https://github.com/Coaokalo/f23b-public/releases).
2. Close DCS, its updater and ModelViewer. Run setup and allow its administrator prompt.
3. Confirm your **DCS game folder** and **Saved Games DCS profile**.
4. Click **Install / Repair**, then start an F-23B Quick Start mission.

MALICE and AIM-9X Block II are independent weapons. **Stock AIM-120B and AIM-9X
remain unchanged.** Setup adds an F-23B-only connection to the installed Hornet
cockpit. No Eagle Dynamics scripts or binaries are included in the download.
This connection can affect multiplayer integrity checks; the preview targets single-player.

Your Hornet controls apply. Select AMRAAM for MALICE or Sidewinder for Block II;
use the normal trigger with master arm on. The bay opens before release. MALICE
requires a designated radar target; Block II requires IR cooling and seeker lock.
The HUD and radar page show the project weapon name and actual remaining count.

Keep the installer for repair and removal. The aircraft ZIP is the installer's
payload, not an extra installation step. The source ZIP is for developers.

## Upgrade, repair, or remove

The corrected installer upgrades the September 17 setup directly. It restores
verified original missile files from the old setup's backup before enabling the
independent weapons. Existing backups remain available for recovery.

After DCS repair, run **Install / Repair** again. A newer DCS version needs a
compatible F-23B build: setup and the weapon connection reject unknown binaries.
Use one managed Saved Games profile per DCS installation in this preview.

To remove, close DCS and use **Remove** in the same installer. It removes its
aircraft folders and cockpit connection, preserving profile controls and missions.
For another release, remove the previous release first unless its upgrade is
explicitly supported. Setup refuses unmanaged aircraft folders and development links.
Move added liveries or edited module files to a backup before removal.

## Help

Confirm the selected profile is the one DCS uses and the Hornet is activated.
For an unsupported or modified game file, restore conflicting mods or repair DCS,
then check that your DCS version is supported. Build details are retained in
`.f23b-install` within your profile.

[Known limitations](KNOWN_ISSUES.md) |
[Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml).
Include the build ID, DCS version, mission, and reproduction steps. Remove account
information and personal paths from logs before sharing them.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
