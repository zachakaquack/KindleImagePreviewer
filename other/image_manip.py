from PIL import Image
from pathlib import Path

from other import files
from other.notifications import get_notification_daemon


def resize_image_fill_transparent(image_path: Path):
    kindle = files.get_kindle()
    kindle_size = kindle.width, kindle.height
    gray_path = files.create_export_path(image_path)

    with Image.open(image_path) as img:
        img = img.convert("RGBA")

        # check if its horizontal / vertical
        # if horizontal, rotate 90deg
        if img.width > img.height:
            img = img.rotate(90, expand=True)

        img = img.resize(kindle_size, Image.Resampling.LANCZOS)

        # LA = grayscale + alpha channel
        img.convert("LA").save(gray_path)

        notif = get_notification_daemon()
        notif.new_message.emit(f"Image saved to: {gray_path}")

    return gray_path
