from __future__ import annotations

import base64
import logging
import os
import shutil
import string
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import click as click
import coloredlogs
import jsonpickle
from PIL import Image
from bs4 import BeautifulSoup

from nton import __version__, nstool, title_ids
from nton.constants import Directories, Binaries, Files
from nton.title_ids import get_game_title_ids


@click.group(invoke_without_command=True)
@click.option("-v", "--version", is_flag=True, default=False, help="Print version information.")
@click.option("-d", "--debug", is_flag=True, default=False, help="Enable DEBUG level logs.")
def main(version: bool, debug: bool) -> None:
    """nton—Nintendo Switch NRO to NSP Forwarder."""
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    log = logging.getLogger(__name__)
    coloredlogs.install(level=log.parent.level, logger=log, fmt="{asctime} [{levelname[0]}] {name} : {message}", style="{")

    copyright_years = 2022
    current_year = datetime.now().year
    if copyright_years != current_year:
        copyright_years = f"{copyright_years}-{current_year}"

    log.info("nton version %s Copyright (c) %s rlaphoenix", __version__, copyright_years)
    log.info("https://github.com/rlaphoenix/nton")
    if version:
        return


@main.command()
@click.argument("path", type=Path)
@click.option("-n", "--name", type=str, default=None, help="Title Name.")
@click.option("-p", "--publisher", type=str, default=None, help="Title Publisher.")
@click.option("-v", "--version", type=str, default=None, help="Title Version.")
@click.option("-i", "--icon", type=Path, default=None, help="Title Icon (256x256px recommended, supports any image).")
@click.option("--id", "id_", type=str, default=None, help="Title ID.")
@click.option("--rom", type=str, default=None, help="ROM path for Direct Game Forwarding.")
@click.option("--sdmc", type=str, default=None, help="NRO path relative to the root of the Switch's microSD card.")
def build(
    path: Path,
    name: str | None,
    publisher: str | None,
    version: str | None,
    icon: Path | None,
    id_: str | None,
    rom: str | None,
    sdmc: str | None
):
    """
    Build an NSP that loads an NRO on the Switch's microSD card.

    \b
    Parameters:
        path: Path to the NRO file. You MUST provide the path on the Switch's microSD card, NOT a file on your PCs
            HDD! This is so we can automatically get the sdmc:/ path in a foolproof way.
        name: Override the Title name that is automatically retrieved from the NRO.
        publisher: Override the Publisher name that is automatically retrieved from the NRO.
        icon: Override the Icon that is automatically retrieved from the NRO. This can be any image of any format or
            resolution. A 256x256px image is recommended.
        id_: Set a specific Title ID, otherwise a Random Title ID is used. There's a miniscule chance it could get the
            same Title ID as another installed Title, but it's so miniscule you shouldn't realistically worry about it.
        rom: Path to a ROM file on the Switch's microSD card to create a forwarder that boots directly into the game.
            The path to the ROM must be an absolute path. The NRO used must be a homebrew that supports specifying a
            ROM by args (e.g., a RetroArch Core, MGBA, possibly others).
        sdmc: Path to the NRO path relative to the root of the Switch's microSD card. This should only be used if the
            NRO path you provided is NOT on the microSD card, as it is implicitly inferred.
    """
    log = logging.getLogger("build")
    log.info("Building!")

    if not path.is_file():
        log.error(f"The NRO path \"{path}\" does not exist, or is not a file.")
        sys.exit(1)

    if path.suffix.lower() != ".nro":
        log.error(f"The NRO path \"{path}\" is not to an NRO file.")
        sys.exit(1)

    if sdmc:
        if not sdmc.startswith("sdmc:/"):
            if not sdmc.startswith("/"):
                sdmc = f"/{sdmc}"
            sdmc = f"sdmc:{sdmc}"
    else:
        path_root = Path(path.anchor)
        if not (
            ((path_root / "Nintendo").exists() and (path_root / "switch").exists()) or
            ((path_root / "atmosphere").exists() and ((path_root / "bootloader").exists()))
        ):
            log.error("The NRO path must be a path on your Switch's microSD card to implicitly infer the sdmc path.")
            log.error("You can use --sdmc to manually specify the path relative to the Switch's microSD card.")
            sys.exit(1)
        sdmc = path.resolve().absolute().as_posix().replace(path.anchor.replace("\\", "/"), "sdmc:/")

    verification = nstool.verify(path, "nro")
    if verification:
        log.critical(f"The NRO \"%s\" is invalid, %s", path, verification)
        sys.exit(2)

    log.info("NRO checked and verified")

    if id_:
        if any(c not in string.hexdigits for c in id_):
            log.error(f"The Title ID \"{id_}\" is an invalid hex string. It must be a-fA-f0-9.")
            sys.exit(1)
        id_ = id_.lower()
        if id_ in title_ids.ALL_SYSTEM:
            log.critical(f"The Title ID \"{id_}\" is a reserved System Title! Using it is unsafe!")
            sys.exit(2)
        if id_ in title_ids.game_title_ids:
            log.warning(f"The Title ID \"{id_}\" is already used by \"{title_ids.game_title_ids[id_]}\".")
    elif path.stem.lower() in title_ids.unofficial:
        id_ = title_ids.unofficial[path.stem.lower()]
    elif sdmc and Path(sdmc).stem.lower() in title_ids.unofficial:
        id_ = title_ids.unofficial[Path(sdmc).stem.lower()]
    else:
        id_ = "0100000000000000"
        while id_ in title_ids.ALL:
            id_ = "01%s000" % os.urandom(6).hex()[:-1]

    if rom and not rom.startswith("/"):
        rom = f"/{rom}"

    log.info(f"Title ID: %s", id_)

    build_dir = Directories.temp / id_
    control_template_file = Directories.assets / "control.nacp.xml"
    control_dir = build_dir / "control"
    romfs_dir = build_dir / "romfs"
    exefs_dir = build_dir / "exefs"
    logo_dir = build_dir / "logo"
    hacbrewpack_backup_dir = build_dir / "hacbrewpack_backup"
    control_file = control_dir / "control.nacp"
    icon_file = control_dir / "icon_AmericanEnglish.dat"
    next_argv_file = romfs_dir / "nextArgv"
    next_nro_path_file = romfs_dir / "nextNroPath"

    log.debug("Build Directory: %s", build_dir)

    try:
        if build_dir.exists():
            log.debug("Build Directory pre-existing")
            shutil.rmtree(build_dir)
        build_dir.mkdir(parents=True)
        control_dir.mkdir()
        romfs_dir.mkdir()

        shutil.copytree(Directories.assets / "exefs", exefs_dir)
        shutil.copytree(Directories.assets / "logo", logo_dir)

        control_file_res = nstool.get_nacp(path, control_file)
        if control_file_res:
            if control_file_res == "No NACP was extracted from the asset.":
                log.warning("The NRO does not have a NACP partition, building a new one.")
                if not name or not publisher or not version:
                    log.error("You must specify a Name, Publisher, and Version to be able to build the NACP.")
                    log.error("You may also want to specify an Icon but it is not strictly necessary.")
                    sys.exit(1)
                control_template = control_template_file.read_text(encoding="utf8")
                root = BeautifulSoup(control_template, "xml")
                for title in root.find_all("Title"):
                    title.Name.string = name
                    title.Publisher.string = publisher
                for title_id in root.find_all(["PresenceGroupId", "SaveDataOwnerId", "LocalCommunicationId"]):
                    title_id.string = f"0x{id_}"
                root.find("DisplayVersion").string = version
                root.find("AddOnContentBaseId").string = hex(int(id_, 16) + 0x1000)
                tmp_control_template = build_dir / "control.nacp.xml"
                tmp_control_template.write_text(str(root))
                try:
                    subprocess.check_output([
                        Binaries.hptnacp,
                        "-a", "createnacp",
                        "-i", str(tmp_control_template.absolute()),
                        "-o", str(control_file.absolute())
                    ])
                except subprocess.CalledProcessError as e:
                    log.critical(f"Failed to build a new NACP, {e.output} [{e.returncode}]")
                    sys.exit(2)
                log.info("Built a new NACP")
            else:
                log.critical(f"Failed extracting the NACP partition from the NRO, {control_file_res}")
                sys.exit(2)

        control_file_data = bytearray(control_file.read_bytes())
        log.debug("Got the Control partition")
        log.debug(base64.b64encode(control_file_data).decode())

        # enable video capture and screenshots if disabled
        if control_file_data[0x3035] != 0x02:
            # 0x00 = Disabled, 0x01 = Manual, 0x02 = Enabled
            control_file_data[0x3035] = 0x02
            log.info("Enabled Video Capture")
        if control_file_data[0x3034] != 0x00:
            # 0x00 = Enabled, 0x01 = Disabled
            control_file_data[0x3034] = 0x00
            log.info("Enabled Screenshots")

        # disable storage allocation as none of them would be used
        save_data_size_offsets = {
            0x3080: "User Account Save Data",
            0x3088: "User Account Save Data Journal",
            0x3090: "Device Save Data",
            0x3098: "Device Save Data Journal",
            0x30A0: "BCAT Delivery Cache Storage",
            0x3148: "Max User Account Save Data",
            0x3150: "Max User Account Save Data Journal",
            0x3158: "Max Device Save Data",
            0x3160: "Max Device Save Data Journal",
            0x3168: "Temporary Storage",
            0x3170: "Cache Storage",
            0x3178: "Cache Storage Journal",
            0x3180: "Max Cache Storage Data and Journal"
        }
        for offset, offset_name in save_data_size_offsets.items():
            save_data_size = int.from_bytes(control_file_data[offset:offset + 8], byteorder="little")
            if save_data_size != 0:
                control_file_data[offset:offset + 8] = b"\x00" * 8
                log.info(f"Removed {offset_name} Allocation")

        # set cache storage index max to 0
        control_file_data[0x3188:0x3188+0x2] = b"\x00\x00"

        # disable user profile selection as it's unnecessary
        control_file_data[0x3025] = 0x00

        if not name:
            # TODO: Assumes "AmericanEnglish" name is the one that's used and wanted
            name = control_file_data[0x0000:0x000F].replace(b"\x00", b"").strip().decode("utf8")
        if not name:
            log.error("The Control Partition does not have any listed Name nor was one manually specified.")
            sys.exit(1)
        if not any(x in string.ascii_letters + string.digits for x in name):
            log.error(f"The Application Name, \"{name}\", cannot be all special characters.")
            sys.exit(1)
        if len(name.encode("utf8")) > 0x200:  # fits 0x200 * 10 (16 fields)
            log.error(f"The Title Name \"{name}\" is too large to fit in the NSP.")
            sys.exit(1)
        log.info("Title Name: %s", name)

        if not publisher:
            # TODO: Assumes "AmericanEnglish" publisher is the one that's used and wanted
            publisher = control_file_data[0x0200:0x020F].replace(b"\x00", b"").strip().decode("utf8")
        if not publisher:
            log.error("The Control Partition does not have any listed Publisher nor was one manually specified.")
            sys.exit(1)
        if not any(x in string.ascii_letters + string.digits for x in publisher):
            log.error(f"The Publisher, \"{publisher}\", cannot be all special characters.")
            sys.exit(1)
        if len(publisher.encode("utf8")) > 0x100:  # fits 0x100 * 10 (16 fields)
            log.error(f"The Title Publisher \"{publisher}\" is too large to fit in the NSP.")
            sys.exit(1)
        log.info("Publisher: %s", publisher)

        # only keep one name/publisher, store as AmericanEnglish
        # this is because the CLI has only one name/publisher option to use
        control_file_data[0x0:0x3000] = b"\x00" * 0x3000
        control_file_data[0x0:0x200] = name.encode("utf8").rjust(0x200, b"\x00")
        control_file_data[0x200:0x300] = publisher.encode("utf8").rjust(0x100, b"\x00")

        if version:
            version_utf8 = version.encode("utf8")
            while len(version_utf8) < 0x10:
                version_utf8 += b"\x00"
            control_file_data[0x3060:0x306F] = version_utf8
        else:
            version = control_file_data[0x3060:0x306F].replace(b"\x00", b"").strip().decode("utf8")
            if not version:
                log.error("The Control Partition does not have any listed Version nor was one manually specified.")
                sys.exit(1)
        if len(version.encode("utf8")) > 0x10:
            log.error(f"The Title Version \"{version}\" is too large to fit in the NSP.")
            sys.exit(1)
        log.info("Version: %s", version)

        control_file.write_bytes(control_file_data)

        if icon:
            shutil.copy(icon, icon_file)
        else:
            icon_file_res = nstool.get_icon(path, icon_file)
            if icon_file_res:
                if icon_file_res == "No Icon was extracted from the asset.":
                    log.warning("The NRO does not have an Icon, proceeding without one.")
                else:
                    log.critical(f"Failed extracting the Icon partition from the NRO, {icon_file_res}")
                    sys.exit(2)
            else:
                log.debug("Got the Icon partition")
                log.debug(base64.b64encode(icon_file.read_bytes()).decode())

        if icon_file.exists():
            # We must strip every unnecessary metadata or the icon will be a '?'
            im = Image.open(icon_file)
            if im.size != (256, 256):
                im = im.resize((256, 256))
            if im.mode != "RGB":
                im = im.convert("RGB")
            clean_im = Image.new(im.mode, im.size)
            clean_im.putdata(list(im.getdata()))
            clean_im.save(icon_file, format="JPEG")
            clean_im.close()
            im.close()

        next_nro_path = sdmc
        next_nro_path_file.write_text(next_nro_path)

        next_argv = next_nro_path
        if rom:
            next_argv += f' "sdmc:{rom}"'
        next_argv_file.write_text(next_argv)

        # only make this directory at this point because we have a high chance of success
        Directories.output.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.check_output([
                Binaries.hacbrewpack,
                "--titleid", id_,
                "--titlename", name,
                "--titlepublisher", publisher,
                "--nspdir", str(Directories.output.absolute()),
                "-k", str(Files.keys.absolute())
            ], cwd=build_dir)
            os.system("")  # fixes logs, I don't know why or how
        except subprocess.CalledProcessError as e:
            log.critical(f"Failed to build NSP, \"{e.args}\", {e.output} [{e.returncode}]")
            sys.exit(2)

        nsp_final_path = Directories.output / f"{name} v{version} by {publisher} [{id_}].nsp"
        if nsp_final_path.exists():
            log.warning("An NSP forwarder of the same name, publisher and title ID already existed.")
            nsp_final_path.unlink()
        (Directories.output / f"{id_}.nsp").rename(nsp_final_path)

        log.info(f"Done! The NSP has been saved to {nsp_final_path}")
    finally:
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if hacbrewpack_backup_dir.exists():
            shutil.rmtree(hacbrewpack_backup_dir)


@main.command()
def update_game_ids():
    """
    Update the pre-existing Title ID registry.

    Note: This makes calls to Tinfoil.io that may fail.
    """
    print("Updating the Game Title ID registry via Tinfoil API, this may take a while...")
    game_title_ids = get_game_title_ids()
    Files.game_title_ids.write_text(jsonpickle.dumps(game_title_ids), encoding="utf8")
