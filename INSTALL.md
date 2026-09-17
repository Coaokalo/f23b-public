# Install or remove the F-23B preview

Requires Windows, **DCS World 2.9.29.27468**, and an installed and activated
**DCS: F/A-18C Hornet**. No separate Python installation or patch command is needed.
Other DCS versions are not qualified; setup refuses unknown native weapon files.

## Install

1. Download **F23B-preview-2026-09-17-Setup.exe** from
   [Releases](https://github.com/Coaokalo/f23b-public/releases).
2. Close DCS, its updater and ModelViewer. Run setup and allow its Windows
   administrator prompt.
3. Confirm your **DCS game folder** and **Saved Games DCS profile**. The profile
   is normally `%USERPROFILE%\Saved Games\DCS` and contains `Config` or `Logs`.
   Use Browse for Steam, a custom location or a different profile.
4. Click **Install / Repair**. Wait for the installed message, then start DCS
   and select an F-23B Quick Start mission. Your existing Hornet controls apply.

Setup installs both aircraft folders and the required custom weapon changes.
**These changes affect AIM-120B and AIM-9X globally, including other aircraft,
and can affect multiplayer integrity checks.** AIM-120C is unchanged.
Original native files are retained in `F23B-native-backup` inside the DCS folder.
No Eagle Dynamics native source or binaries are distributed with setup.

Keep this installer for repair and removal. The source ZIP is for developers;
the aircraft ZIP is a packaging input, not an additional installation step.
This preview is intended for single-player use; see [known limitations](KNOWN_ISSUES.md).

## Repair or change versions

After a DCS update or repair, close DCS and run **Install / Repair** again.
Setup reapplies the weapon changes only when the DCS files are supported.
If an update introduces unknown files, wait for a compatible F-23B release.

For a different F-23B release, use the original installer to **Remove** the old
release first. For an earlier manual installation, preserve its aircraft folders
outside `Mods/aircraft` and follow its original missile-restoration instructions
before installing. Setup refuses unmanaged folders and development junctions.

Use one Saved Games profile per patched DCS installation. The missile changes
are shared by all profiles using that game folder.

## Remove

Close DCS, run the same installer, select the same folders, and click **Remove**.
Setup restores the original missile files and removes its two aircraft folders.
Your profile's controls and missions remain. Native rollback backups are retained.

If you added liveries or changed module files, move those files somewhere safe
before removal. Setup refuses to delete added or changed files, or overwrite
native files modified by an update or another mod. Do not bypass these checks.

## Troubleshooting

- Aircraft absent: confirm you selected the profile DCS actually uses and have
  installed and activated the Hornet.
- Folder not detected: use Browse; the DCS game folder and Saved Games profile
  are two different folders.
- Unsupported missile file: restore conflicting weapon mods or use DCS repair,
  then check whether your DCS version is supported.
- Build details and instructions are retained in `.f23b-install` inside your
  selected profile. Include its `release.json` build ID when reporting a bug.
- [Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)
  with the build ID, DCS version, mission, reproduction steps and relevant
  `Logs/dcs.log` excerpt. Remove account details and personal paths first.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
