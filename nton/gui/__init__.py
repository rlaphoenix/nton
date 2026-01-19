import ctypes
import os
import re
import shutil
import string
import subprocess
import sys
import tempfile
import webbrowser
from functools import partial
from pathlib import Path
from typing import Optional, Union

from PIL import Image
from PySide6.QtGui import QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QInputDialog, QMainWindow, QMessageBox

from nton import __version__, nstool, title_ids
from nton.constants import Binaries, Directories, Files
from nton.gui.logger import log
from nton.gui.main import Ui_MainWindow
from nton.gui.widgets import FileDropper
from nton.helpers import get_copyright_years

NRO_PATH: Optional[Path]
SDMC: Optional[str]
CONTROL_NACP: bytearray

RE_TITLE_ID = re.compile(r"^01([a-fA-F0-9]{11})000$")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def start(debug: bool = False) -> None:
    """Start the GUI and Qt execution loop."""
    # https://stackoverflow.com/a/12522799/13183782
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.rlaphoenix.nton")

    if debug:
        log.setLevel("DEBUG")

    gui = QApplication(sys.argv)
    loader = QUiLoader()
    loader.registerCustomWidget(FileDropper)

    window = MainWindow()
    window.setWindowTitle(f"NTON v{__version__}")

    ensure_dependencies(window)
    setup_logic(window)
    reset_ui(window)  # clear UI file's placeholder data

    window.show()

    gui.exec_()


def ensure_dependencies(window: MainWindow) -> None:
    for binary, path in vars(Binaries).items():
        if binary.startswith("__"):
            continue
        if not path:
            QMessageBox.critical(
                window,
                "Corrupt Installation",
                f"Could not find binary for {binary} which should be pre-bundled with NTON.<br/><br/>"
                "If this continues to happen <a href='https://github.com/rlaphoenix/nton/issues'>Create an Issue</a>.",
                QMessageBox.StandardButton.Ok,
            )
            sys.exit(1)
    if not Files.game_title_ids.exists():
        QMessageBox.critical(
            window,
            "Corrupt Installation",
            "Could not Game Title ID registry which should be pre-bundled with NTON.<br/><br/>"
            "If this continues to happen <a href='https://github.com/rlaphoenix/nton/issues'>Create an Issue</a>.",
            QMessageBox.StandardButton.Ok,
        )
        sys.exit(1)
    while not Files.keys.is_file():
        QMessageBox.critical(
            window,
            "No prod.keys",
            f'Could not find prod.keys file. Place it in the installation directory, or at "{Files.keys_home}".'
            "<br/><br/>"
            "Press OK once done to continue.",
            QMessageBox.StandardButton.Ok,
        )

    # TODO: Add GUI menu bar option to update Game Title ID registry, then warn if outdated
    # if Files.game_title_ids.stat().st_mtime + (60 * 24 * 30) < time.time():
    #     log.warning("Game Title ID registry is quite old, I recommend updating it with `nton update-game-ids`")


def setup_logic(window: MainWindow) -> None:
    # menu bar actions
    window.ui.actionOpen.triggered.connect(partial(open_nro_file, window))
    window.ui.actionClose.triggered.connect(partial(reset_ui, window))
    window.ui.actionExit.triggered.connect(window.close)
    window.ui.actionTroubleshooting.triggered.connect(
        lambda: webbrowser.open("https://github.com/rlaphoenix/nton#troubleshooting")
    )
    window.ui.actionAbout.triggered.connect(partial(about, window))

    # main ui fields
    window.ui.name.textChanged.connect(partial(update_control_nacp, 0x0, 0x200))
    window.ui.author.textChanged.connect(partial(update_control_nacp, 0x200, 0x100))
    window.ui.displayVersion.textChanged.connect(partial(update_control_nacp, 0x3060, 0x10))
    window.ui.videoCapture.currentIndexChanged.connect(partial(update_control_nacp, 0x3035, 0x01))
    window.ui.screenshots.currentIndexChanged.connect(partial(update_control_nacp, 0x3034, 0x01))
    window.ui.titleId.textChanged.connect(partial(title_id_validator, window))

    # main ui buttons
    window.ui.randomizeIdButton.clicked.connect(lambda: window.ui.titleId.setText(generate_title_id()))
    window.ui.loadRomButton.clicked.connect(partial(set_rom_args, window))
    window.ui.buildButton.clicked.connect(partial(build, window))

    # drag/drop to load nro
    def setOpenTextColor(color: str) -> None:
        window.ui.openLabel.setStyleSheet(f"border: 3px solid {color};\nborder-style: dashed;\nborder-radius: 8px;")

    nroDropper = FileDropper(window)
    nroDropper.onHover.connect(partial(setOpenTextColor, "#0868c0"))
    nroDropper.onLeave.connect(partial(setOpenTextColor, "#dcdcdc"))
    nroDropper.dropped.connect(partial(load_nro_file, window))
    nroDropper.clicked.connect(partial(open_nro_file, window))
    window.ui.appPage.setAcceptDrops(True)
    window.ui.appPage.installEventFilter(nroDropper)

    # drag/drop to load image
    imageDropper = FileDropper(window)
    imageDropper.dropped.connect(partial(load_icon_file, window))
    imageDropper.clicked.connect(partial(open_icon_file, window))
    window.ui.icon.setAcceptDrops(True)
    window.ui.icon.installEventFilter(imageDropper)


def reset_ui(window: MainWindow) -> None:
    """Reset the UI to initial startup state."""
    global NRO_PATH
    global SDMC
    global CONTROL_NACP

    NRO_PATH = None
    SDMC = None
    CONTROL_NACP = bytearray()

    window.ui.appPage.setCurrentIndex(0)

    window.ui.openLabel.setStyleSheet("border: 3px solid #dcdcdc;\nborder-style: dashed;\nborder-radius: 8px;")

    window.ui.name.setText("")
    window.ui.author.setText("")
    window.ui.icon.setPixmap(QPixmap())
    window.ui.version.setValue(0)
    window.ui.displayVersion.setText("")
    window.ui.videoCapture.setCurrentIndex(0)
    window.ui.screenshots.setCurrentIndex(0)
    window.ui.titleId.setText("")

    disable_all_fields(window)

    window.ui.statusbar.showMessage("Ready")


def disable_all_fields(window: MainWindow) -> None:
    """Disable all modifiable fields."""
    window.ui.name.setEnabled(False)
    window.ui.author.setEnabled(False)
    window.ui.icon.setEnabled(False)
    window.ui.version.setEnabled(False)
    window.ui.displayVersion.setEnabled(False)
    window.ui.videoCapture.setEnabled(False)
    window.ui.screenshots.setEnabled(False)
    window.ui.titleId.setEnabled(False)


def enable_all_fields(window: MainWindow) -> None:
    """Enable all modifiable fields."""
    window.ui.name.setEnabled(True)
    window.ui.author.setEnabled(True)
    window.ui.icon.setEnabled(True)
    # https://github.com/The-4n/hacBrewPack/issues/15
    # window.version.setEnabled(True)
    window.ui.displayVersion.setEnabled(True)
    window.ui.videoCapture.setEnabled(True)
    window.ui.screenshots.setEnabled(True)
    window.ui.titleId.setEnabled(True)


def about(window: MainWindow) -> None:
    """Displays the Help->About Message Box."""
    QMessageBox.about(
        window,
        "About",
        f"<h1><strong>NTON v{__version__}</strong></h1>"
        + "<p>"
        + f"Version {__version__}<br/>"
        + f"Copyright &copy; {get_copyright_years()} &nbsp; rlaphoenix<br/>"
        + "GNU General Public License, Version 3.0."
        + "</p>"
        + "<a href='https://github.com/rlaphoenix/nton' style='color:blue'>https://github.com/rlaphoenix/nton</a>"
        + "<br/>"
        + "<hr/>"
        + "<p>"
        + " • hacBrewPack licensed under GPL-v2 for packing the NSP:<br/>"
        + "&nbsp;&nbsp; <a href='https://github.com/The-4n/hacBrewPack' style='color:blue'>https://github.com/The-4n/hacBrewPack</a><br/>"
        + " • nstool licensed under MIT for NRO extraction and verification:<br/>"
        + "&nbsp;&nbsp; <a href='https://github.com/jakcron/nstool' style='color:blue'>https://github.com/jakcron/nstool</a><br/>"
        + " • hptnacp from hacPack licensed under GPL-v2 for creating new NACP partitions if the NRO did not have one:<br/>"
        + "&nbsp;&nbsp; <a href='https://github.com/The-4n/hacPack/tree/master/hacPack-Tools/hacPackTools-NACP' style='color:blue'>https://github.com/The-4n/hacPack/tree/master/hacPack-Tools/hacPackTools-NACP</a><br/>"
        + "<br/>"
        + "No changes were made to any of the aforementioned software.<br/>"
        + "<br/>"
        + ' • <a href="https://flaticon.com/free-icons/open-folder">Open folder icons created by Freepik - Flaticon</a><br/>'
        + ' • <a href="https://flaticon.com/free-icons/close">Close icons created by Freepik - Flaticon</a><br/>'
        + ' • <a href="https://flaticon.com/free-icons/delete">Delete icons created by Pixel perfect - Flaticon</a>'
        + "</p>"
        + "<hr/>"
        + "<br/>"
        + 'Made with ❤️ in Ireland &nbsp; <span style="color:green">█</span><span style="color:white">█</p><span style="color:orange">█</span>',
    )


def open_nro_file(window: MainWindow) -> bool:
    """Open a File Dialogue to open and load a file as an NRO."""
    loc = QFileDialog.getOpenFileName(window, "Homebrew Applet (NRO)", "", "NRO files (*.nro);;All files (*.*)")
    if not loc[0]:
        return False

    file_path = Path(loc[0])
    log.debug("Opened File %s", file_path)

    return load_nro_file(window, file_path)


def load_nro_file(window: MainWindow, file_path: Path) -> bool:
    """
    Load NRO file by path.

    This calculates the SDMC path (path to NRO relative to microSD card), loads the data
    to the UI fields, and sets the Stacked Widget to page 2 (the main file-loaded UI).
    """
    global SDMC
    global NRO_PATH

    reset_ui(window)

    window.ui.statusbar.showMessage(f"Loading {file_path.name}")
    log.info("Loading NRO: %s", file_path)
    if not load_nro_data(window, file_path):
        window.ui.statusbar.showMessage(f"Failed loading {file_path.name}")
        log.error("Failed loading NRO: %s", file_path)
        return False

    NRO_PATH = file_path

    path_root = Path(file_path.anchor)
    if not (
        ((path_root / "Nintendo").exists() and (path_root / "switch").exists())
        or ((path_root / "atmosphere").exists() and ((path_root / "bootloader").exists()))
    ):
        log.debug("Couldn't find a Switch-related folder in %s", path_root)
        sdmc, ok = QInputDialog.getText(
            window,
            "SDMC Path",
            "This NRO file is on your PC but NTON is intended to be used with NROs on your Switch's microSD card.<br/>"
            "Please specify where the NRO will be located on your Switch's microSD card. (e.g., /switch/daybreak.nro).",
        )
        sdmc = sdmc.strip()
        if not ok or not sdmc:
            log.debug("User did not give an SDMC")
            window.ui.statusbar.showMessage(f"Cancelled loading {file_path.name}")
            window.ui.appPage.setCurrentIndex(0)
            return False
        log.debug("SDMC given: %s", sdmc)
        if not sdmc.startswith("/"):
            sdmc = f"/{sdmc}"
        SDMC = Path(sdmc).resolve().absolute().as_posix().replace(file_path.anchor.replace("\\", "/"), "sdmc:/")
    else:
        SDMC = file_path.resolve().absolute().as_posix().replace(file_path.anchor.replace("\\", "/"), "sdmc:/")
    log.debug("Resolved SDMC: %s", SDMC)

    window.ui.appPage.setCurrentIndex(1)
    window.ui.statusbar.showMessage(f"Loaded {file_path.name}")
    log.info("Loaded NRO: %s", file_path)

    return True


def load_nro_data(window: MainWindow, nro_path: Path) -> bool:
    """Load NRO Name, Author, Icon, Version, and more to the UI."""
    global CONTROL_NACP

    if nro_path.stem.lower() in title_ids.unofficial:
        title_id = title_ids.unofficial[nro_path.stem.lower()]
        log.info("Got Title ID from NTON registry: %s", title_id)
    else:
        title_id = generate_title_id()
        log.info("Got Randomized Title ID: %s", title_id)
    window.ui.titleId.setText(title_id.upper())

    with tempfile.TemporaryDirectory(prefix="rlaphoenix-nton") as t:
        log.debug("Opened Temporary Directory: %s", t)
        load_dir = Path(t)

        control_file = load_dir / "control.nacp"
        icon_file = load_dir / "icon_AmericanEnglish.dat"

        control_file_res = nstool.get_nacp(nro_path, control_file)
        if control_file_res:
            log.info("Error loading NACP: %s", control_file_res)
            if control_file_res == "No NACP was extracted from the asset.":
                window.ui.name.setText(nro_path.stem)
                window.ui.icon.setPixmap(QPixmap(":/branding/images/sad.png"))
                window.ui.displayVersion.setText("v1.0.0")
                window.ui.videoCapture.setCurrentIndex(2)
                enable_all_fields(window)
                QMessageBox.information(
                    window,
                    "Notice: Crappy NRO",
                    f"The NRO file '{nro_path.name}' is poorly made; it has no NACP partition.<br/>"
                    "This means NTON cannot infer ANY information. Some common defaults have been set, and "
                    "some have been assumed based on the filename.<br/><br/>"
                    "Please note that this is not an error, but there are few NROs without a NACP "
                    "partition. If this is not expected, please verify the integrity of your NRO file.",
                    QMessageBox.StandardButton.Ok,
                )
                return True

            window.ui.appPage.setCurrentIndex(0)
            if "Input file type was undetermined" in str(control_file_res):
                QMessageBox.critical(
                    window,
                    "Failed to load file",
                    f"The file '{nro_path.name}' does not seem to be a valid NRO file,<br/><br/>{control_file_res}",
                    QMessageBox.StandardButton.Ok,
                )
            else:
                QMessageBox.critical(
                    window,
                    "Failed to load file",
                    f"The NRO file '{nro_path.name}' failed to load while extracting the NACP partition,<br/><br/>"
                    f"{control_file_res}<br/><br/>"
                    f"Cannot continue...",
                    QMessageBox.StandardButton.Ok,
                )
            return False

        CONTROL_NACP = bytearray(control_file.read_bytes())
        log.info("Extracted the Control NACP Partition")

        window.ui.videoCapture.setCurrentIndex(CONTROL_NACP[0x3035])
        log.info("Video Capture: %d", CONTROL_NACP[0x3035])
        window.ui.screenshots.setCurrentIndex(CONTROL_NACP[0x3034])
        log.info("Screenshots: %s", CONTROL_NACP[0x3034])

        language_data = {
            lang: {
                "name": CONTROL_NACP[offset : offset + 0x10].replace(b"\x00", b"").strip().decode("utf8"),
                "publisher": CONTROL_NACP[offset + 0x200 : offset + 0x210].replace(b"\x00", b"").strip().decode("utf8"),
            }
            for i, lang in enumerate(
                (
                    "AmericanEnglish",
                    "BritishEnglish",
                    "Japanese",
                    "French",
                    "German",
                    "LatinAmericanSpanish",
                    "Spanish",
                    "Italian",
                    "Dutch",
                    "CanadianFrench",
                    "Portuguese",
                    "Russian",
                    "Korean",
                    "TraditionalChinese",
                    "SimplifiedChinese",
                )
            )
            for offset in [0x0300 * i]
        }

        log.info("Language Data:")

        for lang, data in language_data.items():
            if not data["name"] and not data["publisher"]:
                continue
            log.info(' - %s: [Name: "%s", Publisher: "%s"]', lang, data["name"], data["publisher"])

        for lang, data in language_data.items():
            if data["name"]:
                # TODO: What if another is preferred?
                window.ui.name.setText(data["name"])
                window.ui.author.setText(data["publisher"])
                log.info("Chosen NRO name and publisher from %s Language Data", lang)
                break

        # only keep one name/publisher, store as AmericanEnglish
        # this is because the GUI has only one name/publisher field to use
        update_control_nacp(0x0, 0x300 * 0x10, 0x0)
        update_control_nacp(0x0, 0x200, window.ui.name.text())
        update_control_nacp(0x200, 0x100, window.ui.author.text())
        log.info("Removed all languages, set chosen data as AmericanEnglish")

        icon_file_res = nstool.get_icon(nro_path, icon_file)
        if icon_file_res:
            if icon_file_res == "No Icon was extracted from the asset.":
                log.info("The NRO did not have an Icon")
            else:
                log.error("Failed extracting the Icon partition from the NRO, %s", icon_file_res)
                res = QMessageBox.question(
                    window,
                    "Failed to extract Icon",
                    f"The NRO file '{nro_path.name}' failed to load while extracting the Icon,<br/><br/>"
                    f"{icon_file_res}",
                    QMessageBox.StandardButton.Cancel,
                    QMessageBox.StandardButton.Ignore,
                )
                if res != QMessageBox.StandardButton.Ignore:
                    sys.exit(2)
        else:
            log.info("Got the Icon from the NRO")
        window.ui.icon.setPixmap(QPixmap(icon_file))

        window.ui.displayVersion.setText(CONTROL_NACP[0x3060:0x306F].replace(b"\x00", b"").strip().decode("utf8"))
        log.info("Display Version: %s", window.ui.displayVersion.text())

        enable_all_fields(window)

        return True


def open_icon_file(window: MainWindow) -> None:
    loc = QFileDialog.getOpenFileName(
        window,
        "Homebrew Icon",
        "",
        "Image files (*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.webp *.heif);;All files (*.*)",
    )
    if loc[0]:
        file_path = Path(loc[0])
        load_icon_file(window, file_path)


def load_icon_file(window: MainWindow, icon_path: Path) -> None:
    window.ui.statusbar.showMessage(f"Loading Icon {icon_path.name}")
    window.ui.icon.setPixmap(QPixmap(icon_path))
    window.ui.statusbar.showMessage(f"Set {icon_path.name} as Icon")


def title_id_validator(window: MainWindow, value: str) -> None:
    """Ensure the Title ID is Valid."""
    if RE_TITLE_ID.match(value):
        window.ui.titleId.setStyleSheet("")
    else:
        window.ui.titleId.setStyleSheet("color:red")


def generate_title_id() -> str:
    """
    Generate a Random Title ID.

    The Title ID is ensured to begin with `01` and end with `000`.
    A Base Title typically ends with `000` while a Patch ends with `800`.
    """
    title_id = "0100000000000000"
    while title_id in title_ids.ALL:
        title_id = "01%s000" % os.urandom(6).hex()[:-1]
    return title_id


def update_control_nacp(offset: int, length: int, value: Union[int, str, bytes]) -> None:
    """
    Overwrite Data on the Control NACP at specific offsets.

    If the specified length is larger than the value itself, then it will be
    right-padded with 0x00. If the value is a string, it will be UTF-8 encoded.
    If the value is a number, it will be encoded to bytes in little-endian order.
    """
    if isinstance(value, str):
        vb = value.encode("utf8")
    elif isinstance(value, int):
        vb = value.to_bytes(length, "little")
    elif not isinstance(value, bytes):
        raise TypeError("Value must be int, str, or bytes")
    if len(vb) < length:
        vb = vb.ljust(length, b"\x00")
    CONTROL_NACP[offset : offset + length] = vb


def set_rom_args(window: MainWindow) -> None:
    """
    Helper utility for writing a ROM argv to load a SDMC file.

    This function is not actually specific for Game ROMs, it can be used as a helper
    to write the args to load any kind of file. It just specifies Game ROM just for
    UX reasons as Forwarders mainly use arguments for Game ROM specification.
    """
    loc = QFileDialog.getOpenFileName(
        window,
        "Game ROM (from SD card!)",
        "",
        "Game ROMs (*.3ds *.a26 *.a52 *.amiga *.amstrad *.atari *.c64 *.cpc *.dcm *.fds *.gamegear *.gb *.gbc *.gba"
        "*.gdi *.gg *.intellivision *.lynx *.mame *.md *.msx *.nds *.neogeo *.nes *.ngp *.ngpc *.pce *.pcfx *.pico"
        "*.ps1 *.ps2 *.ps3 *.psp *.psvita *.rom *.sfc *.sg1000 *.sgb *.sms *.snes *.virtualboy *.wii *.wiiu *.xbox);;"
        "All Files (*)",
    )
    if not loc[0]:
        return

    rom_path = Path(loc[0])

    path_root = Path(rom_path.anchor)
    if not (
        ((path_root / "Nintendo").exists() and (path_root / "switch").exists())
        or ((path_root / "atmosphere").exists() and ((path_root / "bootloader").exists()))
    ):
        sdmc, ok = QInputDialog.getText(
            window,
            "ROM Path",
            "This ROM file is on your PC but NTON is intended to be used with ROMs on your Switch's microSD card.<br/>"
            "Please specify where the ROM will be located on your Switch's microSD card. (e.g., /roms/system/game.gb).",
        )
        sdmc = sdmc.strip()
        if not ok or not sdmc:
            return
        if not sdmc.startswith("/"):
            sdmc = f"/{sdmc}"
        sdmc = Path(sdmc).resolve().absolute().as_posix().replace(rom_path.anchor.replace("\\", "/"), "sdmc:/")
    else:
        sdmc = rom_path.resolve().absolute().as_posix().replace(rom_path.anchor.replace("\\", "/"), "sdmc:/")

    existing_args = window.ui.args.text().strip()
    if existing_args:
        existing_args += " "
    existing_args += f'"{sdmc}"'
    window.ui.args.setText(existing_args)


def build(window: MainWindow) -> bool:
    """Build the NSP using the currently loaded Control NACP and UI fields."""
    if not Binaries.hacbrewpack:
        QMessageBox.critical(
            window,
            "Missing Dependency",
            "The hacBrewPack binary is missing, which is required to build NSP files.<br/><br/>"
            "Please reinstall NTON or visit <a href='https://github.com/switchbrew/hacBrewPack'>https://github.com/switchbrew/hacBrewPack</a>",
            QMessageBox.StandardButton.Ok,
        )
        return False
    if not NRO_PATH:
        QMessageBox.critical(
            window,
            "No NRO Selected",
            "No NRO file is currently selected. Please load an NRO file before building an NSP.",
        )
        return False
    if not SDMC:
        QMessageBox.critical(
            window,
            "No SDMC Path",
            "No SDMC path is currently set. Please load an NRO file and set its SDMC path before building an NSP.",
        )
        return False

    name = window.ui.name.text()
    author = window.ui.author.text()
    version = window.ui.version.text()
    title_id = window.ui.titleId.text().lower()

    if any(c not in string.hexdigits for c in title_id):
        QMessageBox.critical(
            window,
            "Title ID Error",
            f'The Title ID "{title_id}" is an invalid hex string. It must be a-fA-F0-9.<br/><br/>'
            "Build cannot continue...",
        )
        return False
    if not RE_TITLE_ID.match(title_id):
        QMessageBox.critical(
            window,
            "Title ID Error",
            f'The Title ID "{title_id}" is not a valid range or length. It must begin with 01 and end with 000.'
            "<br/><br/>Build cannot continue...",
        )
        return False
    if title_id in title_ids.ALL_SYSTEM:
        QMessageBox.critical(
            window,
            "System Title ID Conflict",
            f'The Title ID "{title_id}" is a reserved System Title! It cannot be used!<br/><br/>'
            "Build cannot continue...",
        )
        return False
    if title_id in title_ids.game_title_ids:
        res = QMessageBox.question(
            window,
            "Game Title ID Conflict",
            f'The Title ID "{title_id}" is already used by "{title_ids.game_title_ids[title_id]}".<br/><br/>'
            "Are you sure you want to continue?",
        )
        if res != QMessageBox.StandardButton.Yes:
            return False

    verification = nstool.verify(NRO_PATH, "nro")
    if verification:
        log.error("Integrity Error on the NRO file: %s", verification)
        QMessageBox.critical(
            window,
            "Integrity Error",
            f'The NRO "{NRO_PATH}" is invalid, {verification}<br/><br/>Build cannot continue...',
        )
        return False
    log.info("NRO Integrity: OK")

    save_filename = QFileDialog.getSaveFileName(
        window,
        "Build NSP",
        str(Directories.output / f"{name} by {author} [{title_id.upper()}][v{version}].nsp"),
        "NSP (*.nsp);;All files (*.*)",
    )[0]
    if not save_filename:
        log.info("Cancelled Build as no file save path was chosen")
        return False

    save_path = Path(save_filename)
    log.debug("Chosen Save Path: %s", save_path)

    build_dir = Directories.temp / title_id
    control_dir = build_dir / "control"
    romfs_dir = build_dir / "romfs"
    exefs_dir = build_dir / "exefs"
    logo_dir = build_dir / "logo"
    hacbrewpack_backup_dir = build_dir / "hacbrewpack_backup"
    control_file = control_dir / "control.nacp"
    icon_file = control_dir / "icon_AmericanEnglish.dat"
    next_argv_file = romfs_dir / "nextArgv"
    next_nro_path_file = romfs_dir / "nextNroPath"

    try:
        if build_dir.exists():
            log.debug("Build Directory already exists, somehow, deleting...")
            shutil.rmtree(build_dir)
        build_dir.mkdir(parents=True)
        control_dir.mkdir()
        romfs_dir.mkdir()

        shutil.copytree(Directories.assets / "exefs", exefs_dir)
        shutil.copytree(Directories.assets / "logo", logo_dir)

        # disable user profile selection as it's unnecessary
        update_control_nacp(0x3025, 0x01, 0x0)

        # disable all storage allocation to ensure a 1MB install size
        update_control_nacp(0x3080, 0x08, 0x00)  # User Account Save Data
        update_control_nacp(0x3088, 0x08, 0x00)  # User Account Save Data Journal
        update_control_nacp(0x3090, 0x08, 0x00)  # Device Save Data
        update_control_nacp(0x3098, 0x08, 0x00)  # Device Save Data Journal
        update_control_nacp(0x30A0, 0x08, 0x00)  # BCAT Delivery Cache Storage
        update_control_nacp(0x3148, 0x08, 0x00)  # Max User Account Save Data
        update_control_nacp(0x3150, 0x08, 0x00)  # Max User Account Save Data Journal
        update_control_nacp(0x3158, 0x08, 0x00)  # Max Device Save Data
        update_control_nacp(0x3160, 0x08, 0x00)  # Max Device Save Data Journal
        update_control_nacp(0x3168, 0x08, 0x00)  # Temporary Storage
        update_control_nacp(0x3170, 0x08, 0x00)  # Cache Storage
        update_control_nacp(0x3178, 0x08, 0x00)  # Cache Storage Journal
        update_control_nacp(0x3180, 0x08, 0x00)  # Max Cache Storage Data and Journal
        update_control_nacp(0x3188, 0x02, 0x00)  # Max Cache Storage Index

        control_file.write_bytes(CONTROL_NACP)
        log.debug("Written %d bytes to Control NACP file", len(CONTROL_NACP))
        window.ui.icon.pixmap().save(str(icon_file), "JPG")

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
            log.debug("Converted and Stripped Icon File")

        next_nro_path_file.write_text(SDMC)

        next_argv = SDMC
        args = window.ui.args.text().strip()
        if args:
            next_argv += f" {args}"
        next_argv_file.write_text(next_argv)

        # only make this directory at this point because we have a high chance of success
        Directories.output.mkdir(parents=True, exist_ok=True)

        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.check_output(
                [
                    Binaries.hacbrewpack,
                    "--titleid",
                    title_id,
                    "--nspdir",
                    str(Directories.output.absolute()),
                    "-k",
                    str(Files.keys.absolute()),
                ],
                cwd=build_dir,
                startupinfo=startupinfo,
            )
        except subprocess.CalledProcessError as e:
            log.error('Failed to build NSP, "%s", %s [%d]', e.args, e.output, e.returncode)
            QMessageBox.critical(
                window, "Build Failed", f'Failed to build NSP, "{e.args}", {e.output} [{e.returncode}]'
            )
            return False

        if save_path.exists():
            save_path.unlink()
        shutil.move(Directories.output / f"{title_id}.nsp", save_path)

        log.info("Build NSP to %s", save_path)
        QMessageBox.information(window, "Success", f'An NSP forwarder was built to "{save_path}".')
        return True
    finally:
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if hacbrewpack_backup_dir.exists():
            shutil.rmtree(hacbrewpack_backup_dir)


if __name__ == "__main__":
    start()
