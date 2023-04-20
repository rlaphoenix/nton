# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2023-04-20

### Added

- Added an error message when a required binary was not found.
- Added check to ensure the Title and Publisher have at least one alphanumerical character to stop using
  vague details like `-` or `...` e.t.c.
- Added error messages when a value from NACP was empty/unavailable and one was not manually specified.

### Changed

- NTON now checks if the NRO path you provide is on your Switch microSD card by looking for `Nintendo` & `switch`
  folders, or `atmosphere` & `bootloader` folders. This is much more reliable than simply assuming any drive that
  isn't the C drive to be your microSD card.

### Fixed

- Fix loading of `prod.keys` from the `~/.switch` folder due to incorrect file-exists checks.
- Exiting from the Homebrew via the B button or an Exit option no longer crashes. The ExeFS ROM was updated by
  @Skywalker25 to support this feature properly.
- Fixed crashes when launching forwarders if the ROM path had any spaces.
- Fixed edge-case of incorrect sdmc path calculation on some Windows machines where the drive letter being replaced
  with `sdmc:/` failed causing forwarders to crash on launch.

## [1.2.0] - 2022-11-13

### Added

- User and Device Save Data Allocation is now disabled from all NSP forwarders. This frees up 63 MB of installed file
  space for most NROs, possibly more! The NRO may need Save Data Allocation, which it will keep, but the NSP forwarder
  itself will never ever store any data nor will it need to so such allocation is completely wasteful.
- The NRO path on the Switch's microSD card (sdmc path) can now be manually specified with `--sdmc`. Using `--sdmc`
  allows you to use an NRO path that is NOT on your Switch's microSD card, but you have to be certain that the sdmc
  path you set is correct.
- The NSP filename now contains the NRO version and the version can now be manually specified.
- If the NRO does not have a NACP partition, a new one will be made. If this happens, usage of `--name`, `--publisher`,
  and so on will be required. No Icon will be available, but setting an icon is still optional.
- A warning will now be logged if there's no Icon to use for the NSP.
- The CI/CD workflows have been immensely improved. CI now tests by building a "Hello World!" NSP, and CD now
  automatically builds NSP forwarders for the Homebrew Menu and AIO-Switch-Updater and adds them to the release's
  assets for anyone to download. Every release will make forwarders for whatever NRO is the newest available from the
  [Switch Appstore](https://apps.fortheusers.org/switch).

### Changed

- The forwarder ROM ExeFS has been updated with a new build based on the latest nx-hbloader code. The forwarder ROM is
  now also Open-Source by the original person who made it on GBATemp. It is available here:
  https://github.com/Skywalker25/Forwarder-Mod
- The ROM (`--rom`) path no longer needs to exist and is no longer checked to exist. Unlike the NRO path, we never need
  to read anything from it therefore we don't need to check it.

### Fixed

- Runtime Errors on almost all Subprocess calls under Python 3.7 is now fixed.
- Process Return Codes for errors (non-0 return codes) are now working.
- The output file checks in `nstool.py` for `get_nacp()` and `get_icon()` now check the output file rather than the
  input file.

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

[1.2.1]: https://github.com/rlaphoenix/nton/releases/tag/v1.2.1
[1.2.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.2.0
[1.1.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.1.0
[1.0.1]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.1
[1.0.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.0
