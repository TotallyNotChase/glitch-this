import functools
import os
from PIL import Image, ImageSequence
from typing import Union, Optional


def is_gif(img: Union[str, Image.Image]) -> bool:
    # Returns true if input image is a GIF and/or animated
    if isinstance(img, str):
        if not os.path.isfile(img):
            return False
        img = Image.open(img)
    return any(index >= 2 for index, _ in enumerate(ImageSequence.Iterator(img), start=1))


def _boolean_type_validator(argument_map: dict[str, bool]):
    boolean = 'param must be a boolean'
    for argument_name, argument in argument_map.items():
        if not isinstance(argument, bool):
            raise ValueError(f'{argument_name} {boolean}')


def _glitch_image_bool_type_validator(color_offset: bool, cycle: bool, gif: bool, scan_lines: bool) -> None:
    map_ = {
        "cycle": cycle,
        "color_offset": color_offset,
        "scan_lines": scan_lines,
        "gif": gif
    }

    _boolean_type_validator(argument_map=map_)


def _is_in_range_positive_integer(glitch_amount, glitch_change, glitch_min, glitch_max):
    if not (isinstance(glitch_amount, (float, int)) and glitch_min <= glitch_amount <= glitch_max):
        raise ValueError('glitch_amount parameter must be a positive number '
                         f'in range {glitch_min} to {glitch_max}, inclusive')
    if not (isinstance(glitch_change, (float, int)) and -glitch_max <= glitch_change <= glitch_max):
        raise ValueError(
            f'glitch_change parameter must be a number between {-glitch_max} and {glitch_max}, inclusive')


def _is_positive_integer(positive_integer_map: dict[str, int]):
    for argument_name, argument in positive_integer_map.items():
        if argument <= 0 or not isinstance(argument, int):
            raise ValueError(
                f'{argument_name} param must be a positive integer value greater than 0')


def _is_number(number_map: dict[str, Union[int, float]]):
    for argument_name, argument in number_map.items():
        if argument and not isinstance(argument, (float, int)):
            raise ValueError(f'{argument_name} parameter must be a number')


def _glitch_image_number_type_validator(frames, glitch_amount, glitch_change, seed, step, glitch_min, glitch_max):
    positive_int_map = {"frames": frames, "step": step}
    number_map = {
        "seed": seed
    }
    _is_in_range_positive_integer(glitch_amount, glitch_change, glitch_min, glitch_max)
    _is_positive_integer(positive_int_map)
    _is_number(number_map)


def glitch_image_validators(self, src_img: Union[str, Image.Image], glitch_amount: Union[int, float],
                            seed: Optional[Union[int, float]] = None, glitch_change: Union[int, float] = 0.0,
                            color_offset: bool = False, scan_lines: bool = False, gif: bool = False,
                            cycle: bool = False,
                            frames: int = 23, step: int = 1):
    # Sanity checking the inputs
    _glitch_image_number_type_validator(frames, glitch_amount, glitch_change, seed, step,
                                        self.glitch_min, self.glitch_max)
    _glitch_image_bool_type_validator(color_offset, cycle, gif, scan_lines)


def validate_images(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        glitch_image_validators(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper
