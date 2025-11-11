from pathlib import Path
from PIL import Image, ImageQt

from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QTransform, Qt

from other import files
from other.signals import get_signals
from other.notifications import get_notification_daemon


def grayscale_image(image_path: Path) -> QImage:
    img = Image.open(f"{image_path}")

    # grayscale it
    img = img.convert("LA")

    # convert back to rgba for the image
    img = img.convert("RGBA")

    # there is no image format built into qt that allows for grayscale + alpha,
    # so we have to do this weird workaround
    return ImageQt.toqimage(img)


def create_grayscaled_color_bg(size: tuple[int, int], original_color: str) -> QImage:
    color = QColor(original_color)
    gray = int((color.red() * 0.299) + (color.green() * 0.587) + (color.blue() * 0.114))
    alpha = color.alpha()

    gray_color = QColor(gray, gray, gray, alpha)

    qt = QImage(QSize(size[0], size[1]), QImage.Format.Format_ARGB32)
    qt.fill(gray_color)
    return qt


def create_text_image(image: QImage, text: str):
    kindle = files.get_kindle()

    use_dark_mode_text = files.get_singleton("use_dark_mode_text")

    # base image
    composed = QImage(QSize(kindle.width, kindle.height), QImage.Format.Format_ARGB32)
    painter = QPainter(composed)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    if use_dark_mode_text:
        # hsl(0, 0%, 10%)
        composed.fill(QColor(26, 26, 26))
        painter.setPen(QColor(255, 255, 255))
    else:
        # hsl(0, 0%, 80%)
        composed.fill(QColor(179, 179, 179))
        painter.setPen(QColor("black"))

    # text
    # painter.setPen(QColor(255, 255, 255))
    painter.setFont(QFont("Helvetica", 20))

    # get the boundary of the rect
    padding = 0
    text_rect = QRect(padding, padding, kindle.width - padding, kindle.height - padding)
    flags = (
        Qt.AlignmentFlag.AlignLeft
        | Qt.AlignmentFlag.AlignTop
        | Qt.TextFlag.TextWordWrap
    )
    painter.drawText(text_rect, flags, text)

    # draw image on top
    painter.drawImage(0, 0, image)
    painter.end()

    return composed


def scale_image(image_path: Path) -> tuple[QImage, QImage]:
    kindle = files.get_kindle()
    settings = files.get_image_settings()
    signal = get_signals()

    image = grayscale_image(image_path)
    image = image.convertToFormat(QImage.Format.Format_ARGB32)

    # the base image to draw on
    # base_image = QImage(QSize(kindle.width, kindle.height), QImage.Format.Format_ARGB32)
    # base_image.fill(settings["fill_color"])
    base_image = create_grayscaled_color_bg(
        (kindle.width, kindle.height), settings["fill_color"]
    )

    goal_width = image.width()
    goal_height = image.height()
    offset_x = settings["offset_x"]
    offset_y = settings["offset_y"]

    # only "scale" the image when you dont fit it
    if settings["fit_x"]:
        goal_width = kindle.width
    else:
        goal_width *= settings["scale_factor"] / 100

    if settings["fit_y"]:
        goal_height = kindle.height
    else:
        goal_height *= settings["scale_factor"] / 100

    image = image.scaled(
        QSize(goal_width, goal_height),
        mode=Qt.TransformationMode.FastTransformation,
    )

    degrees = settings["rotation_count"] * 90
    degrees += settings["rotation_offset"]

    image = image.transformed(QTransform().rotate(degrees))
    signal.update_image_resolution.emit(goal_width, goal_height)

    painter = QPainter(base_image)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    painter.drawImage(offset_x, offset_y, image)
    painter.end()

    # base_image now has the actual image that we want - now put make the text image
    # this function puts text "behind" the image
    text_image = create_text_image(
        base_image,
        """\tLorem ipsum dolor sit amet, consectetur adipiscing elit. Duis faucibus diam condimentum enim vulputate volutpat. Ut sed mauris ac purus luctus porta. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut varius pulvinar eros, sit amet hendrerit elit pellentesque in. Praesent elit neque, auctor sed elit vitae, fringilla consectetur nisi. Vestibulum eget viverra nisi, non suscipit urna. Nulla porttitor accumsan diam, eu eleifend purus sodales sit amet. Curabitur tincidunt rhoncus suscipit.

\tDonec ac aliquet justo, quis aliquam lorem. Nam condimentum enim et vulputate auctor. Duis at diam commodo justo pretium volutpat ut eget velit. Vivamus vitae massa odio. Vestibulum porttitor cursus eros ac rhoncus. Aenean sed neque at est malesuada mattis sed quis magna. In aliquam dolor est, vitae hendrerit dolor ullamcorper id. Proin urna tortor, mattis in mattis non, tincidunt a mi.

\tNam eget fermentum leo. Mauris est leo, egestas volutpat risus sit amet, bibendum rutrum metus. Pellentesque ultrices arcu vel dui dapibus, eget pellentesque leo venenatis. Morbi fermentum, sem non mollis viverra, sem quam efficitur diam, ut pulvinar ex ligula a turpis. Curabitur non felis lectus. Morbi iaculis feugiat volutpat. Phasellus fermentum urna quis nunc efficitur, eu condimentum nisi suscipit. Cras in turpis sed purus tristique consequat in a sapien. Proin at justo tempor, pellentesque orci sed, dapibus massa. Ut sed arcu elementum, sodales urna at, vulputate quam. Suspendisse nec felis at elit congue facilisis. Praesent semper at diam eget laoreet. Phasellus in ornare dui, non placerat nisi. Praesent eleifend ipsum non tincidunt posuere. Nulla laoreet ut neque a feugiat. Vivamus libero sapien, consequat sed congue eu, euismod a ante.
""",
    )

    return text_image, base_image
