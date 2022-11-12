from __future__ import annotations

import base64
import logging
import os
import shutil
import string
import subprocess
from datetime import datetime
from pathlib import Path

import click as click

from nton import __version__, nstool
from nton.constants import Directories, Binaries, Files


@click.group(invoke_without_command=True)
@click.option("-v", "--version", is_flag=True, default=False, help="Print version information.")
@click.option("-d", "--debug", is_flag=True, default=False, help="Enable DEBUG level logs.")
def main(version: bool, debug: bool) -> None:
    """nton—Nintendo Switch NRO to NSP Forwarder."""
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    log = logging.getLogger()

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
@click.option("-i", "--icon", type=Path, default=None, help="Title Icon (256x256px recommended, supports any image).")
@click.option("--id", "id_", type=str, default=None, help="Title ID.")
def build(path: Path, name: str | None, publisher: str | None, icon: Path | None, id_: str | None) -> int:
    """
    Build an NSP that loads an NRO on the Switch's microSD card.

    Parameters:
        path: Path to the NRO file. You MUST provide the path on the Switch's microSD card, NOT a file on your PCs
            HDD! This is so we can automatically get the sdmc:/ path in a foolproof way.
        name: Override the Title name that is automatically retrieved from the NRO.
        publisher: Override the Publisher name that is automatically retrieved from the NRO.
        icon: Override the Icon that is automatically retrieved from the NRO. This can be any image of any format or
            resolution. A 256x256px image is recommended.
        id_: Set a specific Title ID, otherwise a Random Title ID is used. There's a miniscule chance it could get the
            same Title ID as another installed Title, but it's so miniscule you shouldn't realistically worry about it.

    """
    log = logging.getLogger("build")
    log.info("Building!")

    if not path.is_file():
        log.error(f"The NRO path \"{path}\" does not exist, or is not a file.")
        return 1

    if path.suffix.lower() != ".nro":
        log.error(f"The NRO path \"{path}\" is not to an NRO file.")
        return 1

    # TODO: Improve this check by using win32 calls to see if the drive is a removable drive or not.
    #       Perhaps there's also a way to see if it's specifically an SD card, but it might not be reliable.
    if path.drive == "C":
        log.error(f"The NRO path must be a path on your Switch's microSD card.")
        return 1

    verification = nstool.verify(path, "nro")
    if verification:
        log.critical(f"The NRO \"%s\" is invalid, %s", path, verification)
        return 2

    log.info("NRO checked and verified")

    if id_:
        if any(c not in string.hexdigits for c in id_):
            log.error(f"The Title ID \"{id_}\" is an invalid hex string. It must be a-fA-f0-9.")
            return 1
        id_ = id_.lower()
        # TODO: Ensure the id is valid for an NSP, is there restrictions?
    else:
        id_ = "01%s000" % os.urandom(6).hex()[:-1]

    log.info(f"Title ID: %s", id_)

    build_dir = Directories.temp / id_
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
            log.critical(f"Failed extracting the NACP partition from the NRO, {control_file_res}")
            return 2

        control_file_data = control_file.read_bytes()
        # version = control_file_data[0x3060:0x306F].replace(b"\x00", b"").strip().decode("utf8")

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
        control_file.write_bytes(control_file_data)

        if not name:
            # TODO: Assumes first region/language of the NROs title/name data is wanted
            #       Is UTF8 or ANSI wanted here when decoding? UTF8 should be fine
            name = control_file_data[0x0000:0x000F].replace(b"\x00", b"").strip().decode("utf8")
        elif len(name.encode("utf8")) > 0x200:  # fits 0x200 * 10 (16 fields)
            log.error(f"The Title Name \"{name}\" is too large to fit in the NSP.")
            return 1

        log.info("Title Name: %s", name)

        if not publisher:
            publisher = control_file_data[0x0200:0x020F].replace(b"\x00", b"").strip().decode("utf8")
        elif len(publisher.encode("utf8")) > 0x100:  # fits 0x100 * 10 (16 fields)
            log.error(f"The Title Publisher \"{publisher}\" is too large to fit in the NSP.")
            return 1

        log.info("Publisher: %s", publisher)

        if icon:
            shutil.copy(icon, icon_file)
        else:
            icon_file_res = nstool.get_icon(path, icon_file)
            if icon_file_res:
                log.critical(f"Failed extracting the Icon partition from the NRO, {icon_file_res}")
                return 2
            log.debug("Got the Icon partition")
            log.debug(base64.b64encode(icon_file.read_bytes()).decode())

        # We must strip every unnecessary metadata or the icon will be a '?'
        try:
            subprocess.check_output([
                Binaries.magick, "mogrify",
                "-format", "jpg",
                "-resize", "256x256",
                "-strip", icon_file
            ])
            # magick changes the .dat to .jpg, let's undo that
            icon_file.unlink()
            shutil.move(icon_file.with_suffix(".jpg"), icon_file)
        except subprocess.CalledProcessError as e:
            log.critical(f"Failed to convert and strip the Icon, {e.output} [{e.returncode}]")
            return 2

        sdmc_path = f"sdmc:{str(path.resolve().absolute()).split(':', maxsplit=1)[1]}"
        next_argv_file.write_text(sdmc_path)
        next_nro_path_file.write_text(sdmc_path)

        # only make this directory at this point because we have a high chance of success
        Directories.output.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.check_output([
                Binaries.hacbrewpack,
                "--titleid", id_,
                "--titlename", name,
                "--titlepublisher", publisher,
                "--nspdir", Directories.output,
                "-k", Files.keys
            ], cwd=build_dir)
        except subprocess.CalledProcessError as e:
            log.critical(f"Failed to build NSP, \"{e.args}\", {e.output} [{e.returncode}]")
            return 2

        nsp_final_path = Directories.output / f"{name} by {publisher} [{id_}].nsp"
        (Directories.output / f"{id_}.nsp").rename(nsp_final_path)

        log.info(f"Done! The NSP has been saved to {nsp_final_path}")
    finally:
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if hacbrewpack_backup_dir.exists():
            shutil.rmtree(hacbrewpack_backup_dir)
