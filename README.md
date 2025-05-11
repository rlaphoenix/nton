# NTON

[![Build status](https://github.com/rlaphoenix/nton/actions/workflows/ci.yml/badge.svg)](https://github.com/rlaphoenix/nton/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/nton)](https://pypi.python.org/pypi/nton)
[![Python versions](https://img.shields.io/pypi/pyversions/nton)](https://pypi.python.org/pypi/nton)
<a href="https://github.com/rlaphoenix/nton/blob/master/LICENSE">
  <img align="right" src="https://img.shields.io/badge/license-GPLv3-blue" alt="License (GPLv3)"/>
</a>

<img src="https://github.com/rlaphoenix/nton/assets/17136956/c6306192-9a57-41f2-8840-cc8db03fef93" style="width:300px" align="right" />

NTON is a Nintendo Switch NRO to NSP Forwarder for firmware 12.0.0 and newer.

A forwarder lets you open Homebrew files from your SD card through the Nintendo Switch Home Screen instead
of the Homebrew Launcher.

> [!TIP]
> Want to generate NSP forwarders directly on your Switch via Homebrew? Check out [TooTallNate's switch-nsp-forwarder](https://github.com/TooTallNate/switch-nsp-forwarder)!

<img src="https://user-images.githubusercontent.com/17136956/206882948-4f05cace-16a3-4300-9047-8cba33106a64.jpg" style="width:505px" />

> [!CAUTION]
> Installing NSP files, like NRO to NSP forwarders, can result in your console getting banned as they do not contain valid signatures verified by Nintendo.
> This applies to all forms of NRO to NSP forwarders, including homebrew and web versions. We do not possess Nintendo's private key to generate valid signatures.
> NSP forwarders are only safe if used on an emuMMC with all Nintendo servers blocked with [DNS.mitm](https://github.com/Atmosphere-NX/Atmosphere/blob/master/docs/features/dns_mitm.md).
> Do not install them on sysMMC (system eMMC/NAND). Do not use 90DNS or any manual DNS server approach. DNS.mitm is a much safer and faster approach.
> To run NSP forwarders you need to make further modifications to the boot process and your system. I do not support Piracy on any Nintendo device therefore support on that is not provided.

## Features

- ⚙ Firmware 12.0.0+ Support
- 🛡️ Title ID Conflict Checks
- 🤖 Automatically Extracts Title Information and Icon from NRO
- 🕹️ Direct Game Forwarding
- 🎥 Enable or Disable Video Capture and Screenshots
- 💾 1MB NSP Install Size
- 🖼️ Custom Icons
- 🧩 Plug-and-play
- ✨ GUI and CLI Interfaces
- ❤️ Forever FOSS!

## Installation

*Windows Installers for the GUI version is available on the [Releases] page.*

Alternatively you can download and install NTON from PIP/PyPI:

```shell
$ pip install nton[gui]
```

*(Exclude `[gui]` if you do not plan on using the GUI)*

> [!NOTE]
If pip gives you a warning about a path not being in your PATH environment variable then promptly add that path then
close all open command prompt Windows, or running `nton` won't work as it will not be recognized as a program.

You now have the `nton` package installed - Voilà 🎉!  
Launch the GUI by running `nton` without another subcommand in your Terminal or Windows Run.  
Otherwise, use the CLI by checking out `nton --help`.

  [Releases]: <https://github.com/rlaphoenix/nton/releases>

### Keys

Proprietary Keys known as `prod.keys` are required. You can obtain them from your own personal Switch using
[Lockpick_RCM](https://gbatemp.net/download/lockpick_rcm-1-9-15-fw-20-zoria.39129).

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

> [!NOTE]
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

> [!NOTE]
> - You must use a path to a RetroArch Game Core NRO, not the path to the RetroArch NRO itself.
> - Do not move, delete, or rename the ROM or the Core NRO files that are on your microSD card, or it will break.

## Storage Sizes

On Installation an NSP can allocate storage for specific purposes. There's three primary types of Storage:

- User Account Save Data: Storage allocated to each User profile. Most titles use this to save game progress.
- Device Save Data: Storage allocated to the Device itself. Typically used for data or information that should be set 
  to and used by all User profiles. For example, Animal Crossing: New Horizons uses this to store the Island data for
  all profiles to use.
- Cache Storage: Storage allocated for temporary data. Data stored here will be wiped without warning.

The NSP can specify how much data to allocate initially, as well as the maximum amount of storage that data can occupy
over time. Furthermore, the initial and maximimum size allocated for Journaling (a form of recovery and data integrity)
can also be specified.

A Forwarder like the ROM NTON uses does not need any form of storage or save data. Therefore, NTON automatically sets
all storage sizes to `0` to reduce storage usage.

## Troubleshooting

Before continuing try running the homebrew from the Homebrew Launcher and see if it works through there.
If it does not work through the Homebrew launcher either, then it was never the forwarder's fault, and you should
check on your NRO or application installation.

Please note that using Forwarders others have created has a good chance of not working on your system.
The location of the NRO on their system may differ from the location on your system, hence the NSP won't be able
to load the homebrew. I will not provide support if you are having an issue with a Forwarder you did not build
yourself.

### The forwarder does not launch, "The software was closed because an error occurred."

As the NSP forwarder's signature is not valid as we do not possess Nintendo's private signing keys, you cannot boot
any NSP forwarder with CFW alone. Nintendo has DMCA'd the options that allow you to run these kinds of NSP files due
to it allowing piracy. Support on this matter cannot be provided as I do not support piracy on any Nintendo system.

If you do not agree with enabling piracy, do not want to enable piracy, or do not know how to proceed from here, then
I do not recommend using NRO to NSP forwarders at all and stick with the Homebrew launcher through the Album icon, or
by opening any Game or Software while holding (R).

However, it's also possible the `prod.keys` you used with NTON is outdated for your firmware. Re-download the latest
Lockpick_RCM and re-obtain this `prod.keys` file from your own Switch. Make sure you choose to get keys from the SysMMC
or EmuMMC that you will be installing the forwarder on (or whichever has a newer firmware version).

### The forwarder starts loading but then crashes

The NRO path set when building the forwarder is incorrect or the NRO file is currently missing (or your microSD card is
not inserted). Make sure the path you choose starts with `/` and is an absolute path to an existing NRO file on your
Switch's microSD card (not your PC).

### The forwarder's icon is a '?'

This happens when the `icon_AmericanEnglish.dat` within the built forwarder is not to the spec that Nintendo likes, in
some way. This is usually caused by the format of the image not being JPEG, or it has EXIF data or other unnecessary
extra metadata.

> [!NOTE]
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

There are numerous reasons why this could be, see the following main reasons:

1. Make sure you haven't deleted or moved the NRO on your Switch's microSD card. It cannot be moved as the built
forwarder has a hardcoded file path that it loads the NRO from when launched.
2. You may have since updated Atmosphere or your Firmware which broke the changes you made to the bootloader that enabled
the use of custom NSP files. As this project does not support piracy on any Nintendo system, support is not provided.
4. It's possible a firmware update has broken the [forwarder ROM][ROM] that is used and needs
to be updated. Both Firmware 9.0.0 and 12.0.0 have previously broken different forwarder ROMs requiring updates. If
you believe this to be the case then please make an Issue.

If after reading all of these troubleshooting steps, you still cannot get the NSP forwarder to work, then I do not
recommend the use of them and instead recommend using the Homebrew launcher from the album or from title takeover
(holding R while booting any Game or Software).

## Development

The following steps are basic instructions on downloading and working on the code under a [Poetry] environment.

1. Follow Poetry's Docs to [Install Poetry].
2. Download NTON's latest code, `git clone https://github.com/rlaphoenix/nton`
3. Navigate to the downloaded code repository, `cd nton`
4. _Optionally_ have Poetry install the virtual-env in the project, `poetry config virtualenvs.in-project true` 
5. Install NTON's dependencies and development tools, `poetry install -E gui`
6. Run NTON from within the Poetry venv, `poetry run nton --help`

> [!NOTE]
> If you plan to work on or use the GUI during development, then add `-E gui` during Step 5.

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

## Licensing

This software is licensed under the terms of [GNU General Public License, Version 3.0](LICENSE).
You can find a copy of the license in the LICENSE file in the root folder

This project uses the following software:

- hacBrewPack licensed under GPL-v2 for packing the NSP: https://github.com/The-4n/hacBrewPack
- nstool licensed under MIT for NRO extraction and verification: https://github.com/jakcron/nstool
- hptnacp from hacPack licensed under GPL-v2 for creating new NACP partitions if the NRO did not have one:
  https://github.com/The-4n/hacPack/tree/master/hacPack-Tools/hacPackTools-NACP

No changes were made to any of the aforementioned software and copies of their licenses can be found next to their
binaries within the bin folder.

- [Open folder icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/open-folder)
- [Close icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/close)
- [Delete icons created by Pixel perfect - Flaticon](https://www.flaticon.com/free-icons/delete)

* * *

© rlaphoenix 2022-2024
