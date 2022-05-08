import os
from PIL import Image


def _get_format_from_extension(img_path: str) -> str:
    format_ = "RGB"
    if img_path.endswith('.gif'):
        format_ = "GIF"
    elif img_path.endswith('.png'):
        format_ = "PNG"
    return format_


def convert_based_on_file_extension(img_path: str) -> Image.Image:
    # Sanity Check if the path exists
    if not os.path.isfile(img_path):
        raise FileNotFoundError('Path not found')

    _format_map = {
        "GIF": lambda: Image.open(img_path),
        "PNG": lambda: Image.open(img_path).convert('RGBA'),
        "RGB": lambda: Image.open(img_path).convert('RGB')
    }

    return _format_map.get(_get_format_from_extension(img_path))()


def convert_based_on_file_format(src_img: Image.Image) -> Image.Image:
    _format_map = {
        "GIF": lambda: src_img,
        "PNG": lambda: src_img.convert('RGBA'),
    }

    return _format_map.get(src_img.format, lambda: src_img.convert('RGB'))()
