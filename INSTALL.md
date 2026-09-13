# F-23B Black Widow II — experimental preview

Requires Windows, **DCS World 2.9.29.27468**, an installed and activated
**DCS: F/A-18C Hornet**, and **Python 3.11 or later** for the missile installer.
Other DCS versions are not qualified. The installer checks the actual native
weapon files and refuses unknown versions.

This preview uses the Hornet cockpit and avionics with experimental F-23 flight
forces, internal bays, MALICE and project AIM-9X Block II. It is intended for
single-player testing. Full-envelope flight, VR and multiplayer are unqualified.
Block II post-launch datalink/LOAL is not implemented.

## Install

1. Download the **F23B-preview-…zip** release asset and extract it completely.
   GitHub's automatic “Source code” archives are not the aircraft download.
2. Close DCS, its updater and ModelViewer. Move any existing `F-23B` and
   `F-23B-Player` folders to a backup location outside `Mods/aircraft`.
   Copy both new folders into `%USERPROFILE%\Saved Games\DCS\Mods\aircraft`.
   Use your actual Saved Games profile if it is named `DCS.openbeta` or differs.
   Do not merge old files into the new folders. Keep your `Config/Input` mappings.
3. In the extracted download, open a terminal and run the following, replacing
   the DCS path with your installation directory:

   ```powershell
   python native_patch.py install --dcs-root "D:\Eagle Dynamics\DCS World"
   python native_patch.py verify --dcs-root "D:\Eagle Dynamics\DCS World"
   ```

   Both commands must report PASS. If Windows denies access to the DCS folder,
   run the terminal as administrator and repeat. Keep this extracted release
   for verification and rollback.
4. Start DCS normally. Select the F-23B and an included Quick Start mission,
   or use an F-23B mission with the MALICE/Block II payload. Existing Hornet
   controls apply. Selecting a missile leaves the bay closed; one trigger press
   opens the bay, sends the native release command and closes the bay.

The two missile patches are required. They replace **AIM-120B and AIM-9X globally**,
including their use on other aircraft. AIM-120C remains unchanged. This changes
DCS installation files and can fail multiplayer integrity checks. DCS repair or
updates may remove the patches; verify again afterward. Do not force installation
on an unsupported version or replace a missing patch with an old downloaded ED file.
No ED native source or binary is included: the installer uses your own installation.

## Remove or roll back

Close DCS and run this from the original extracted release:

```powershell
python native_patch.py restore --dcs-root "D:\Eagle Dynamics\DCS World"
```

Then remove the two F-23B module folders from Saved Games, or restore your prior
module backup and its matching native patch. Original native files and checksums
are retained in `F23B-native-backup` inside the DCS installation. The script
refuses to overwrite files changed by an update or another mod. If DCS already
restored the stock files, restore is harmless. Keep backups until rollback is
complete; a different F-23B weapon revision requires restoring the old release first.

## Troubleshooting

- Aircraft absent: check that both folders sit directly inside `Mods/aircraft`,
  with `entry.lua` immediately inside each; check Hornet installation/activation.
- Aircraft present but missiles wrong: run native patch verification and choose
  a matching F-23B payload. Installing Saved Games folders alone is insufficient.
- Unsupported native file: restore other missile modifications or use DCS repair,
  then check whether your DCS version is supported. Do not bypass the checksum.
- Bug reports: include the build ID from `release.json`, DCS version, mission,
  steps to reproduce and the relevant `Saved Games/DCS/Logs/dcs.log` excerpt.
  Remove personal paths or account details before posting.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
