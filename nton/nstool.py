from __future__ import annotations

import subprocess
from pathlib import Path

from nton.constants import Binaries, Files

BIN = Binaries.nstool
FILE_TYPES = ("xci", "pfs", "romfs", "nca", "meta", "cnmt", "nso", "nro", "ini", "kip", "nacp", "aset", "cert", "tik")
SUBPROCESS_STARTUP_INFO = subprocess.STARTUPINFO()
SUBPROCESS_STARTUP_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def verify(path: Path, type_: str) -> str | int | None:
    """
    Verify if the Nintendo Switch file is valid.
    Returns an empty string if valid, an error str or return code otherwise.
    """
    if not path:
        raise ValueError("The path must not be empty.")
    if not isinstance(path, Path):
        raise TypeError("The path variable is not a Path object.")
    if not path.is_file():
        raise FileNotFoundError("The path was not found or is not a file.")

    if not type_:
        raise ValueError("The type must not be empty.")
    if not isinstance(type_, str):
        raise TypeError("The type_ variable is not a str object.")
    type_ = type_.lower()
    if type_ not in FILE_TYPES:
        raise ValueError(f"The type_ \"{type_}\" is not a valid type. File types: {', '.join(FILE_TYPES)}")

    try:
        subprocess.check_output(
            [
                BIN,
                "-k", str(Files.keys.absolute()),
                "-t", type_,
                "--verify", str(path.absolute())
            ],
            stderr=subprocess.PIPE,
            startupinfo=SUBPROCESS_STARTUP_INFO
        )
        return None
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf8").strip() or e.returncode


def get_nacp(asset_path: Path, output_path: Path) -> str | int | None:
    """
    Extract the NACP partition from a Homebrew Asset Blob.

    Parameters:
        asset_path: Homebrew Asset Blob to get the NACP from. E.g., an NRO.
        output_path: Path to save the NACP to.

    Returns an empty string if valid, an error str or return code otherwise.
    """
    try:
        subprocess.check_output(
            [
                BIN,
                "-k", str(Files.keys.absolute()),
                "--nacp", str(output_path.absolute()),
                str(asset_path.absolute())
            ],
            startupinfo=SUBPROCESS_STARTUP_INFO
        )
        if not output_path.is_file():
            return "No NACP was extracted from the asset."
        if output_path.stat().st_size <= 2:
            return "An empty NACP was extracted from the asset."
        return None
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf8").strip() or e.returncode


def get_icon(asset_path: Path, output_path: Path) -> str | int | None:
    """
    Extract the Icon partition from a Homebrew Asset Blob.

    Parameters:
        asset_path: Homebrew Asset Blob to get the Icon from. E.g., an NRO.
        output_path: Path to save the Icon to.

    Returns an empty string if valid, an error str or return code otherwise.
    """
    try:
        subprocess.check_output(
            [
                BIN,
                "-k", str(Files.keys.absolute()),
                "--icon", str(output_path.absolute()),
                str(asset_path.absolute())
            ],
            startupinfo=SUBPROCESS_STARTUP_INFO
        )
        if not output_path.is_file():
            return "No Icon was extracted from the asset."
        if output_path.stat().st_size <= 2:
            return "An empty Icon was extracted from the asset."
        return None
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf8").strip() or e.returncode
