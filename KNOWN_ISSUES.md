# Known limitations

- Windows and DCS 2.9.29.27468 with an installed, activated F/A-18C Hornet are required.
  The independent weapon connection uses a version-specific cockpit interface;
  both setup and the connection reject unsupported binaries.
- Intended for single-player. VR and multiplayer compatibility are not established.
  The F-23B-only cockpit connection may fail multiplayer integrity checks.
- The Hornet's remaining SMS pages and launch-zone calculations retain donor logic.
  Use the project weapon names and counts on the HUD and radar page. Weapon-specific
  launch envelopes and the full long-range engagement envelope are not qualified.
- Independent Block II radar cueing is implemented. HMD cueing is not connected to
  the independent seeker. Post-launch datalink/LOAL is not implemented.
- Full flight-envelope accuracy is not established.
  Reference tables derive from a community F-22 model rather than measured YF-23 data.
- DCS repair can remove the cockpit connection. Rerun setup on a supported version;
  after a game update, wait for a compatible build. See [installation](INSTALL.md).
- The installer is unsigned.

[Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)
with the build ID, DCS version, mission, and reproduction steps.
