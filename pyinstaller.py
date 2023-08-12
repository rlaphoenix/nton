import itertools
import os
import shutil
from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent

from nton import __version__

from PyInstaller.__main__ import run

from nton.helpers import get_copyright_years


parser = ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Enable debug mode (keeps leftover build files)")
parser.add_argument("--name", default="NTON", help="Set the Project Name")
parser.add_argument("--author", default="rlaphoenix", help="Set the Project Author")
parser.add_argument("--version", default=__version__, help="Set the EXE Version")
parser.add_argument("--icon-file", default="nton/gui/resources/images/nton.ico",
                    help="Set the Icon file path (must be a .ICO file)")
parser.add_argument("--one-file", action="store_true", help="Build to a singular .exe file")
parser.add_argument("--console", action="store_true", help="Show the Console window")
args = parser.parse_args()


"""Configuration options that may be changed or referenced often."""
ADDITIONAL_DATA = [
    # local file path, destination in build output
    ["nton/assets", "nton/assets"],
    ["nton/bin", "nton/bin"],
    ["nton/gui/main.ui", "nton/gui"]
]
HIDDEN_IMPORTS = []
EXTRA_ARGS = [
    "-y", "--win-private-assemblies", "--win-no-prefer-redirects"
]

"""Prepare environment to ensure output data is fresh."""
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)
Path("NTON.spec").unlink(missing_ok=True)
version_file = Path("pyinstaller.version.txt")


"""Set Version Info Structure."""
VERSION_4_TUP = tuple(map(int, ("%s.0" % args.version).split(".")))
version_file.write_text(
    dedent(f"""
    VSVersionInfo(
      ffi=FixedFileInfo(
        filevers=({", ".join(args.version.split("."))}, 0),
        prodvers=({", ".join(args.version.split("."))}, 0),
        OS=0x40004,  # Windows NT
        fileType=0x1,  # Application
        subtype=0x0  # type is undefined
      ),
      kids=[
        StringFileInfo(
          [
          StringTable(
            '040904b0',
            [StringStruct('CompanyName', '{args.author}'),
            StringStruct('FileDescription', 'Nintendo Switch NRO to NSP Forwarder'),
            StringStruct('FileVersion', '{args.version}'),
            StringStruct('InternalName', '{args.name}'),
            StringStruct('LegalCopyright', '{f"Copyright (C) {get_copyright_years()} %s" % args.author}'),
            StringStruct('OriginalFilename', 'NTON.exe'),
            StringStruct('ProductName', '{args.name}'),
            StringStruct('ProductVersion', '{args.version}'),
            StringStruct('Comments', '{args.name}')])
          ]), 
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
      ]
    )
    """).strip(),
    encoding="utf8"
)

"""Run PyInstaller with the provided configuration."""
try:
    run([
        "nton/__main__.py",
        "-n", args.name,
        "-i", ["NONE", args.icon_file][bool(args.icon_file)],
        ["-D", "-F"][args.one_file],
        ["-w", "-c"][args.console],
        *itertools.chain(*[["--add-data", os.pathsep.join(x)] for x in ADDITIONAL_DATA]),
        *itertools.chain(*[["--hidden-import", x] for x in HIDDEN_IMPORTS]),
        "--version-file", str(version_file),
        *EXTRA_ARGS
    ])
finally:
    if not args.debug:
        shutil.rmtree("build", ignore_errors=True)
        Path("NTON.spec").unlink(missing_ok=True)
        version_file.unlink(missing_ok=True)
