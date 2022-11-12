# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2022-11-12

### Added

- Direct RetroArch Game forwarding is now supported. Supply a RetroArch core as the NRO, and a ROM with `--rom`.
- Video Capture and Screenshots capability is now Enabled if it isn't already.
- A list of system title IDs are now used to ensure safe NSPs are made; See Security.
- A mapping of game title IDs and Names are also obtained from an external location and cached for 12 hours.
  This title ID is to warn if you manually specify a Title ID and prevent random title ID generation to match a game.
- Logs are now pretty to look at and have colors.
- A list of pre-defined title IDs are now set and used for some NRO filenames as an alternative to a random Title ID.
  The pre-defined title ID will not be used if you manually set one with `--id`.

### Fixed

- A crash will no longer occur when the NSP is being renamed to the final filename format. It will now warn you that it
  happened, and it will overwrite the pre-existing NSP with the new one.

### Security

- You can no longer create an NSP with the Title ID that matches that of a System title. This prevents you from
  accidentally making or sharing an NSP that would overwrite an important system title which would very likely brick
  your system.
- You can still manually make an NSP with the Title ID of a normal Game title, but a warning will be shown.
- Like above, the randomized Title ID generator will re-roll if it somehow matched an existing System title.
  It also re-rolls if it matches a Game title.

## [1.0.1] - 2022-11-11

Initial release (as a Python script).

### Added

- NRO files are now validated/verified with `nstool` before building.
- The Title Name and Publisher is now automatically retrieved from the NRO.
- You can now override the extracted Icon from the NRO with any image file of any format or size.
  You need to make it square yourself though!
- Paths to files are now checked and validated across the codebase in various ways to help reduce user error.

### Changed

- The Nintendo Switch `prod.keys` are now loaded from `C:/Users/<Username>/.switch/prod.keys` if it's not found in the
  current working directory. This is a common keys file location used by a lot of different homebrew.
- The output folder has been removed. NSPs are now saved to a folder named `NTON` on your Desktop.
  You can change the directories used for everything in the `constants.py` file.

### Fixed

- You can no longer insert random files in `exefs` or `romfs` by mistake (or not!) as the directories are ensured to
  be clean due to the temp directory process and how the directories are made, cleaned, and removed.

### Known Issues

- Logs of binary calls like `nstool` are not getting logged or printed to stdout.

## [1.0.0] - 2022-11-11

Initial release (as CMD script).

[1.1.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.1.0
[1.0.1]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.1
[1.0.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.0
