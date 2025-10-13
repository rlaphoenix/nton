# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-10-13

### Added

- Support for Switch Firmware 19.0.0 and newer.

## [2.1.1] - 2024-01-20

### Added

- Support for Python 3.12.

### Changed

- Release builds now use the same bundled third-party binaries in this project's repository at the time of release.
- nstool has been updated to v1.8.1.

### Fixed

- Fixed crash when saving the Built NSP to a drive other than the `C:` drive.

## [2.1.0] - 2023-10-03

### Changed

- Dropped support for Python 3.7.
- Portable and Installer GUI builds are now built on PyInstaller 6.
- HacBrewPack no longer sets/deals with the Name/Publisher language data.

### Fixed

- Name and Publisher was Padded with 0x00 on the wrong side. However, it ultimately was not an issue as HacBrewPack
  effectively overrode all Name/Publisher changes anyway, but still.
- Special characters like "é" etc. are no longer garbled in the built NSP. This was a bug when HacBrewPack set the
  name and publisher, yet that was never intended anyway. Now NTON itself fully manages setting the Name and Publisher.
- Multiple language data being included but with missing data is now fixed. Only AmericanEnglish is enabled, and only
  AmericanEnglish has language data. Similarly to the previous issue, this was caused by HacBrewPack in the same way. 

## [2.0.1] - 2023-08-26

### Changed

- Moved the Binary dependency and prod.keys checks from `constants.py` to `main.py` so it only runs if you actually
  run the CLI.
- Moved the Game Title ID registry checks from `title_ids.py` to `main.py`, again so it only runs if you actually
  run the CLI.

### Fixed

- Fixed silent crash when running the GUI if the Binary dependencies are missing.
- Fixed silent crash when running the GUI if the Game Title ID registry is missing.
- Fixed silent crash when running the GUI if the `prod.keys` file is missing.

## [2.0.0] - 2023-08-12

### Added

- Added a fully featured Windows GUI built using Qt for Python. The Installer and Portable EXEs are built using
  PyInstaller and Inno Setup.

## [1.4.0] - 2023-08-12

### Added

- Force Disabled the "Select User" launch requirement on Control NACPs. This removes the menu asking you to choose
  a User Profile when launching the Forwarder when you have two or more User Profiles. Choosing a User Profile is
  unnecessary as we do not use any kind of storage, let alone per-profile storage.
- Disabled more types of Storage allocation, in some cases freeing up even more post-install storage usage.

### Changed

- Now only keeping one Language Name/Publisher on both NRO-derived Control NACPs and new Control NACPs. This is so NSP
  tools and the Switch only reads one Icon file, and one Language, since only one of these can be defined by the CLI.
  Non-English language Switch's will still support the NSP.

### Fixed

- Manually set Display Version used incorrect byte for padding.

## [1.3.0] - 2023-08-06

### Added

- All leftover external dependencies are now redistributed and bundled with the project. NTON is now truly
  Plug-and-play! Just install NTON and it's ready to go!
- Licenses for the dependencies are now bundled alongside the redistributed binaries.
- Stating of these dependencies' source code/link, license, and any changes has been added to the README.

### Fixed

- Corrected the invalid use "Operating System :: OS Independent" when NTON currently only supports Windows 7+.
- Updated severely outdated `__version__` variable affecting the version number displayed with `nton --version`.

## [1.2.3] - 2023-08-06

### Added

- Added `update-game-ids` command to manually update the Game Title ID registry.
- Added warning when Game Title ID registry is older than 30 days.

### Changed

- Game Title ID cache no longer expires, therefore is no longer considered cache and is now known as the Game Title ID
  registry.
- Game Title ID registry is now part of the project/package files and will be updated on each release.
- Replaced usage of ImageMagick with Pillow; ImageMagick is no longer a dependency.

### Fixed

- Fixed API call within `get_game_title_ids()`, though it still sometimes errors with HTTP 500. 

## [1.2.2] - 2023-04-20

## Added

- Added full support for Python 3.11.

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
- The NRO path is no longer forced to be within `/retroarch/cores` when `--rom` is used. This is to allow use of
  `--rom` with other Homebrew, e.g., MGBA. 

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

[2.2.0]: https://github.com/rlaphoenix/nton/releases/tag/v2.2.0
[2.1.1]: https://github.com/rlaphoenix/nton/releases/tag/v2.1.1
[2.1.0]: https://github.com/rlaphoenix/nton/releases/tag/v2.1.0
[2.0.1]: https://github.com/rlaphoenix/nton/releases/tag/v2.0.1
[2.0.0]: https://github.com/rlaphoenix/nton/releases/tag/v2.0.0
[1.4.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.4.0
[1.3.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.3.0
[1.2.3]: https://github.com/rlaphoenix/nton/releases/tag/v1.2.3
[1.2.2]: https://github.com/rlaphoenix/nton/releases/tag/v1.2.2
[1.2.1]: https://github.com/rlaphoenix/nton/releases/tag/v1.2.1
[1.2.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.2.0
[1.1.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.1.0
[1.0.1]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.1
[1.0.0]: https://github.com/rlaphoenix/nton/releases/tag/v1.0.0
