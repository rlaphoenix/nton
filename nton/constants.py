import os
import shutil
import tempfile
from pathlib import Path


class Directories:
    root = Path(__file__).resolve().parent  # root of package/src
    temp = Path(tempfile.gettempdir()) / "rlaphoenix-nton"
    output = Path.home() / "Desktop" / "NTON"
    assets = root / "assets"
    bin = root / "bin"


PATH = os.environ.get("PATH", "")
PATH = os.pathsep.join([str(Directories.bin), PATH])
os.environ["PATH"] = PATH


class Binaries:
    nstool = shutil.which("nstool")
    hacbrewpack = shutil.which("hacbrewpack")
    hptnacp = shutil.which("hptnacp")


class Files:
    keys_home = (Path.home() / ".switch" / "prod.keys")
    keys_cwd = Path("./prod.keys").absolute()
    keys = keys_cwd if keys_cwd.is_file() else keys_home
    game_title_ids = Directories.assets / "game_title_ids.json"
    ui_file = Directories.root / "gui" / "main.ui"
