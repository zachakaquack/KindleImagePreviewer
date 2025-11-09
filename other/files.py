from pathlib import Path
import json
from other.notifications import get_notification_daemon
from classes.kindle import Kindle


def write_default_config(path: Path) -> None:
    d = {
        "settings": {
            "image_path": f"{image_path()}",
            "gray_prefix": "",
            "gray_suffix": "_gray",
        },
        "kindle_settings": {
            "width": 600,
            "height": 800,
        },
    }

    with open(path, "w") as f:
        f.write(json.dumps(d, indent=4))


def config_path() -> Path:
    return Path.cwd() / ".settings.json"


def image_path() -> Path:
    return Path.cwd() / "images/"


def config() -> dict:
    path: Path = config_path()
    img_path: Path = image_path()

    if not path.exists():
        notification_daemon = get_notification_daemon()
        notification_daemon.new_message.emit(f"Config not found! Creating at: {path}")
        write_default_config(path)

    if not img_path.exists():
        notification_daemon = get_notification_daemon()
        notification_daemon.new_message.emit(
            f"Image directory not found! Creating at: {img_path}"
        )
        img_path.mkdir()

    with open(path, "r") as f:
        return json.load(f)


def get_kindle():
    cfg: dict = config()
    kindle: Kindle = Kindle()
    return kindle.from_dict(cfg["kindle_settings"])


def write_config(config: dict):
    path = config_path()
    with open(path, "w") as f:
        f.write(json.dumps(config, indent=4))


def update_kindle_width(width: int) -> None:
    cfg: dict = config()
    cfg["kindle_settings"]["width"] = int(width)
    write_config(cfg)


def update_kindle_height(height: int) -> None:
    cfg: dict = config()
    cfg["kindle_settings"]["height"] = int(height)
    write_config(cfg)


def create_export_path(original_image_path: Path) -> Path:
    cfg: dict = config()
    settings = cfg["settings"]
    img_path = settings["image_path"]
    prefix = settings["gray_prefix"]
    suffix = settings["gray_suffix"]
    name = original_image_path.stem

    # doozy
    # extension is png because it is always transferred into that
    return Path(f"{img_path}/{prefix}{name}{suffix}.png")
