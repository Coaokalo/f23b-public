# Install or remove the F-23B

Requires Windows, **DCS World 2.9.29.27468**, and an installed and activated
**DCS: F/A-18C Hornet**. No separate Python installation is needed.

## Install

1. Download **F23B-2026-09-29-Setup.exe** from
   [the release page](https://github.com/Coaokalo/f23b-public/releases/tag/release-2026-09-29).
2. Close DCS, its updater and ModelViewer. Run setup and allow its administrator prompt.
3. Confirm your **DCS game folder** and **Saved Games DCS profile**.
4. Click **Install / Repair**, then start an F-23B Quick Start mission.

Setup puts the `F-23B` and `F-23B-Player` folders in `Saved Games/DCS/Mods/aircraft`.
**It does not add or change files in the DCS game folder.** Stock missiles stay unchanged.
The F-23B connects its weapons and radar functions in memory only while you fly it.
No Eagle Dynamics scripts or binaries are included in the download.

## Fly

Your Hornet controls apply. Put MASTER ARM to ARM. Select AMRAAM for MALICE or
Sidewinder for Block II, then use the normal trigger. The bay opens before release.
MALICE requires a designated radar target. Block II requires IR cooling and seeker lock.
The SA page SCL button now also selects 640 NM.

Loadouts: 3x AIM-424 MALICE + 2x AIM-9X Block II, or 3x AIM-120C + 2x Block II.
The Quick Start missions carry MALICE and Block II.

## Upgrade, repair, or remove

**Upgrading from an earlier F-23B release:** run **Install / Repair**. Setup
removes the cockpit connection that the September 18 release added to the Hornet
cockpit script. It also restores missile files that the September 17 release changed.
Your DCS game folder then has no F-23B changes.

After DCS repair, run **Install / Repair** again. A newer DCS version needs a
compatible F-23B build: setup and the F-23B native functions reject unknown binaries.
Use one managed Saved Games profile per DCS installation with this release.

To remove, close DCS and use **Remove** in the same installer. It removes both
aircraft folders and keeps your controls and missions.
Setup refuses unmanaged aircraft folders and development links.
Move added liveries or edited module files to a backup before removal.

Keep the installer for repair and removal. The aircraft ZIP is the installer's
payload, not an extra installation step. The source ZIP is for developers.

## Help

Confirm the selected profile is the one DCS uses and the Hornet is activated.
For an unsupported or modified game file, restore conflicting mods or repair DCS,
then check that your DCS version is supported. Build details are kept in
`.f23b-install` within your profile.

[Known limitations](KNOWN_ISSUES.md) |
[Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml).
Include the release name, DCS version, mission, and reproduction steps. Remove account
information and personal paths from logs before sharing them.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
