# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.1]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.1
[1.0.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.0
