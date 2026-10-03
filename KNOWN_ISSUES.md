# Known limitations

- Windows and DCS 2.9.30.28536 with an installed, activated F/A-18C Hornet are required.
  The F-23B native functions check the exact DCS binaries. Setup rejects unsupported
  versions, and the functions turn off with a logged error if the game changes.
- Intended for single-player. VR and multiplayer compatibility are not established.
- AI F-23Bs use the MALICE energy profile only when the player also flies an F-23B.
- MALICE's 98,400-foot coasting-apex threshold is not a hard altitude cap.
  A supported A-50 intercept was observed from 336.4 statute miles, with an apex near 158,000 feet.
  Exact 350-mile shots and the full engagement envelope remain unverified.
- The Hornet's remaining SMS pages keep donor labels. MALICE uses the AMRAAM
  selection and Block II uses the Sidewinder selection.
- Block II helmet cueing and post-launch datalink/lock-on after launch are not implemented.
- Full flight-envelope accuracy is not established.
  Reference tables derive from a community F-22 model rather than measured YF-23 data.
- Nosewheel steering authority reduces with ground speed to prevent ground loops.
  Use rudder and differential braking at higher taxi and landing speeds.
- The installer is unsigned.

[Report a bug](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml)
with the release name, DCS version, mission, and reproduction steps.
