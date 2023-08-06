# NTON

[![Build status](https://github.com/rlaphoenix/nton/actions/workflows/ci.yml/badge.svg)](https://github.com/rlaphoenix/nton/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/nton)](https://pypi.python.org/pypi/nton)
[![Python versions](https://img.shields.io/pypi/pyversions/nton)](https://pypi.python.org/pypi/nton)
<a href="https://github.com/rlaphoenix/nton/blob/master/LICENSE">
  <img align="right" src="https://img.shields.io/badge/license-GPLv3-blue" alt="License (GPLv3)"/>
</a>

NTON is a Nintendo Switch NRO to NSP Forwarder for firmware 12.0.0 and newer.

A forwarder lets you open a Homebrew NRO file from your SD card through the Nintendo Switch Home Screen instead
of the Homebrew Launcher.

![Preview](https://user-images.githubusercontent.com/17136956/206882948-4f05cace-16a3-4300-9047-8cba33106a64.jpg)
*Forwarders made with NTON.*

## Features

- 🛡️ Safety-first approach; System/Game Title IDs cannot be used and NRO files are validated
- 🕹️ Boot right into an Emulated Game with Direct RetroArch Game Forwarding
- 🎥 Video Capture and Screenshots
- 🖼️ Custom Forwarder Icon of any resolution or format
- 🤖 The Title Name, Publisher, Icon, and more are automatically extracted from the NRO
- ⚙ Currently Supports Firmware 12.0.0 and up
- 🧩 Plug-and-play installation via PIP/PyPI
- ❤️ Forever FOSS!

## Installation

> **Note** *Requires [Python] 3.7.0 or newer with PIP installed.*

```shell
$ pip install nton
```

You now have the `nton` package installed and a `nton` executable is now available.
Check it out with `nton --help` - Voilà 🎉!

> **Warning**<br>
If pip gives you a warning about a path not being in your PATH environment variable then promptly add that path then
close all open command prompt Windows, or running `nton` won't work as it will not be recognized as a program.

  [Python]: <https://python.org>

### 1. Dependencies

The following is a list of programs required to be installed manually.

- [hacBrewPack] for packing the NSP.
- [nstool] for NRO extraction and verification.
- [hptnacp] for creating new NACP partitions if the NRO did not have one.

Make sure you put them in your current working directory, in NTON's installation directory, or put the dependency's
installation folder in your `PATH` environment variable. If you do not do this then NTON will not be able to find said
dependency and will not be able to continue.

  [hacBrewPack]: <https://github.com/The-4n/hacBrewPack>
  [nstool]: <https://github.com/jakcron/nstool>
  [hptnacp]: <https://github.com/The-4n/hacPack/tree/master/hacPack-Tools/hacPackTools-NACP>

### 2. Keys

Proprietary Keys known as `prod.keys` are required. You can obtain them from your own personal Switch using
Lockpick_RCM.

It must be placed at `C:\Users\<User>\.switch\prod.keys`, in your current working directory, or in
NTON's installation directory for NTON to be able to find and use the keys.

## Usage

NTON is quite simple, just give it the path to the NRO on your microSD card!

*For example, to create a forwarder for the Daybreak Homebrew included with Atmosphere, it's as simple as:*

```shell
nton build "D:/switch/daybreak.nro"
```

This will build a forwarder with the Title Name, Publisher, Version, and Icon automatically extracted from the NRO.
The Title ID will be a randomly assigned value within generally conformed bounds. You may manually set a value with
`--name`, `--publisher`, `--version`, `--icon`, and `--id` respectively.

The Title ID is automatically checked against a periodically updated list of pre-existing System and Software Title IDs
to ensure a collision does not occur. However, you should still be cautious and verify the Title ID is not already used
by other Software before using. 

> **Note**<br>
> While NTON can be used on NRO files stored on your PC, it was designed to be used directly from your Switch's
> microSD card. If you prefer to create forwarders with NRO files on your PC, or for batch purposes, you can specify
> the path that the NRO file will reside on your microSD card during generation with `--sdmc`.

For example, to make a forwarder for an NRO that is on your PC:

```shell
nton build "C:/Users/rlaphoenix/Downloads/haze.nro" --sdmc "/switch/haze.nro"
```

### Direct RetroArch Game forwarding

Use a RetroArch Game Core as the NRO path and provide the path to the ROM on your Switch's microSD card with `--rom`.  
This will then load the Core directly under RetroArch and provide the path to the ROM as a startup argument to the
RetroArch Core.

> **Note**
> - You must use a path to a RetroArch Game Core NRO, not the path to the RetroArch NRO itself.
> - Do not move, delete, or rename the ROM or the Core NRO files that are on your microSD card, or it will break.

## Troubleshooting

Before continuing try running the homebrew from the Homebrew Launcher and see if it works through there.
If it does not work through the Homebrew launcher either, then it was never the forwarder's fault, and you should
check on your NRO or application installation.

Please note that using Forwarders others have created has a good chance of not working on your system.
The location of the NRO on their system may differ from the location on your system, hence the NSP won't be able
to load the homebrew. I will not provide support if you are having an issue with a Forwarder you did not build
yourself.

### The forwarder does not launch, "The software was closed because an error occurred."

Your "sigpatches" (signature patches) that allow unsigned titles to launch is likely outdated or not set up correctly.
Sigpatches can go outdated from Horizon OS firmware updates, Atmosphere updates (as well as silent updates). It is
recommended to use the [sys-patch](https://github.com/ITotalJustice/sys-patch) sys-module to automatically patch your
system from signature checks as well as other useful patches. The default configuration is fine for the majority of
systems and is a simple copy & paste to your microSD card to install.

It's also possible the `prod.keys` you used with NTON is outdated for your firmware. Get new ones with Lockpick_RCM
and make sure you choose to get keys from the SysMMC or EmuMMC that you will be installing the forwarder on (or
whichever has a newer firmware version).

### The forwarder starts loading but then crashes

The NRO path set when building the forwarder is incorrect or the NRO file is currently missing (or your microSD card is
not inserted). Make sure the path you choose starts with `/` and is an absolute path to an existing NRO file on your
Switch's microSD card (not your PC).

### The forwarder's icon is a '?'

This happens when the `icon_AmericanEnglish.dat` within the built forwarder is not to the spec that Nintendo likes, in
some way. This is usually caused by the format of the image not being JPEG, or it has EXIF data or other unnecessary
extra metadata.

> **Note**<br>
This is considered a bug if it happens to you after using NTON as it should automatically sanitize the
images when building the forwarder. If this happens to you, please report what image you chose to use, or give
information on what exact NRO you were making a forwarder from.

### The forwarder's icon is a loading circle, opening fails

The installation of the Forwarder NSP failed in some way and the result is a corrupt title under that Title ID.
This may have happened when trying to install data to the Title ID you chose or had randomly assigned to your forwarder
NSP on an unsupported firmware version. This also happens when trying to install DLC to a Title without having the
minimum required Game Update for that DLC (i.e. Installing the DLC Courses while on Mario Kart 8 Deluxe v1.0). However,
since this happened on your Forwarder NSP you can likely rule that out.

When this happens deleting and reinstalling the same NSP likely won't fix it or do anything. You may need to reinstall
the NSP via Goldleaf and hit "Proceed" when it warns yo uthat the title is already installed. Goldleaf will deal with
the pre-existing files properly unlike Tinfoil (where you likely had the corruption in the first place). DBI may also
help you resolve this issue as it has tools to remove partial installs and leftover files.

### The forwarder randomly stopped working, I've read everything so far

You most likely updated Atmosphere or Horizon OS's Firmware and need to update your Sigpatches. If that hasn't fixed
it, make sure you haven't deleted or moved the NRO on your Switch's microSD card. It cannot be moved as the built
forwarder has a hardcoded file path that it loads the NRO from when launched.

If it still does not work, it's possible a firmware update has broken the [forwarder ROM][ROM] that is used and needs
to be updated. Both Firmware 9.0.0 and 12.0.0 have previously broken different forwarder ROMs requiring updates. If
you believe this to be the case then please make an Issue.

## Development

The following steps are basic instructions on downloading and working on the code under a [Poetry] environment.

1. Follow Poetry's Docs to [Install Poetry].
2. Download NTON's latest code, `git clone https://github.com/rlaphoenix/nton`
3. Navigate to the downloaded code repository, `cd nton`
4. _Optionally_ have Poetry install the virtual-env in the project, `poetry config virtualenvs.in-project true` 
5. Install NTON's dependencies and development tools, `poetry install`
6. Run NTON from within the Poetry venv, `poetry run nton --help`

As shown, running the `nton` executable is somewhat different to a normal installation. This is because Poetry installs
all dependencies and the `nton` shim itself within a virtual-environment, which is like a clone of your Python install
stripped clean, with only NTON's dependencies installed. That way you don't mess around with any dependencies from any
other installed Python applications, nor the other way around. A secluded environment.

I recommend taking a look at [Poetry's Docs] for further information, why not get started by reading Poetry's guide on
[Using Your Virtual Environment].

  [Poetry]: <https://python-poetry.org>
  [Install Poetry]: <https://python-poetry.org/docs/#installation>
  [Poetry's Docs]: <https://python-poetry.org/docs>
  [Using Your Virtual Environment]: <https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment>

## Credit

- [meliodas2255] for their [Open-Source forwarder ROM][ROM] supporting v12.0.0+ with both direct RetroArch Forwarding
  and general forwarding both supported.
- [vgmoose] for the [sdl-hello-world] NRO that is used in CI/CD testing.

  [meliodas2255]: <https://gbatemp.net/members/meliodas2255.410353>
  [vgmoose]: <https://github.com/vgmoose>
  [ROM]: <https://github.com/Skywalker25/Forwarder-Mod>
  [sdl-hello-world]: <https://github.com/vgmoose/sdl-hello-world>

## License

[GNU General Public License, Version 3.0](LICENSE)
