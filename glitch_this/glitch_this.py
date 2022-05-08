import os
import shutil
import random
from decimal import getcontext, Decimal
from typing import List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageSequence
from glitch_this.exceptions import WrongImageFormatException


def _is_gif(img: Union[str, Image.Image]) -> bool:
    # Returns true if input image is a GIF and/or animated
    if isinstance(img, str):
        if not os.path.isfile(img):
            return False
        img = Image.open(img)
    return any(index >= 2 for index, _ in enumerate(ImageSequence.Iterator(img), start=1))


def _open_image_file(src: Union[str, Image.Image]) -> Optional[Image.Image]:
    if isinstance(src, str):
        try:
            return _convert_based_on_file_extension(src)
        except Exception as err:
            # File is not an Image
            raise WrongImageFormatException('Wrong format') from err
    if isinstance(src, Image.Image):
        return _convert_based_on_file_format(src)


def _get_format_from_extension(img_path: str) -> str:
    format_ = "RGB"
    if img_path.endswith('.gif'):
        format_ = "GIF"
    elif img_path.endswith('.png'):
        format_ = "PNG"
    return format_


def _convert_based_on_file_extension(img_path: str) -> Image.Image:
    # Sanity Check if the path exists
    if not os.path.isfile(img_path):
        raise FileNotFoundError('Path not found')

    _format_map = {
        "GIF": lambda: Image.open(img_path),
        "PNG": lambda: Image.open(img_path).convert('RGBA'),
        "RGB": lambda: Image.open(img_path).convert('RGB')
    }

    return _format_map.get(_get_format_from_extension(img_path))()


def _convert_based_on_file_format(src_img: Image.Image) -> Image.Image:
    _format_map = {
        "GIF": lambda: src_img,
        "PNG": lambda: src_img.convert('RGBA'),
    }

    return _format_map.get(src_img.format, lambda: src_img.convert('RGB'))()


def _fetch_image(src_img: Union[str, Image.Image], gif_allowed: bool) -> Image.Image:
    """
     The following code resolves whether input was a path or an Image
     Then returns an Image object

     Raises an exception if `img` param is not an Image
    """
    if gif_allowed or (not _is_gif(src_img) or not src_img.endswith('.gif')):
        return _open_image_file(src_img)
    else:
        # File is not an Image
        # OR it's a GIF but GIF is not allowed

        # Raise the GENERIC exception here
        raise WrongImageFormatException('Wrong format')


class ImageGlitcher:
    # Handles Image/GIF Glitching Operations

    __version__ = '1.0.2'

    def __init__(self):
        # Setting up global variables needed for glitching
        self.pixel_tuple_len = 0
        self.img_width, self.img_height = 0, 0
        self.img_mode = 'Unknown'

        # Creating 3D arrays for pixel data
        self.input_array = None
        self.output_array = None

        # Getting PATH of temp folders
        self.lib_path = os.path.split(os.path.abspath(__file__))[0]
        self.gif_dir_path = os.path.join(self.lib_path, 'Glitched GIF')

        # Setting glitch_amount max and min
        self.glitch_max = 10.0
        self.glitch_min = 0.1

    def glitch_image(self, src_img: Union[str, Image.Image], glitch_amount: Union[int, float],
                     seed: Optional[Union[int, float]] = None, glitch_change: Union[int, float] = 0.0,
                     color_offset: bool = False, scan_lines: bool = False, gif: bool = False, cycle: bool = False,
                     frames: int = 23, step: int = 1) -> Union[Image.Image, List[Image.Image]]:
        """
         Sets up values needed for glitching the image

         Returns created Image object if gif=False

         Returns list of Image objects if gif=True

         PARAMETERS:-

         src_img: Either the path to input Image or an Image object itself

         glitch_amount: Level of glitch intensity, [0.1, 10.0] (inclusive)

         glitch_change: Increment/Decrement in glitch_amount after every glitch

         cycle: Whether to cycle glitch_amount back to glitch_min or glitch_max
                if it over/underflow's

         color_offset: Specify True if color_offset effect should be applied

         scan_lines: Specify True if scan_lines effect should be applied

         gif: True if output should be ready to be saved as GIF

         frames: How many glitched frames should be generated for GIF

         step: Glitch every step'th frame, defaults to 1 (i.e all frames)

         seed: Set a random seed for generating similar images across runs,
               defaults to None (random seed).
        """

        # Sanity checking the inputs
        if not (isinstance(glitch_amount, (float, int)) and self.glitch_min <= glitch_amount <= self.glitch_max):
            raise ValueError('glitch_amount parameter must be a positive number '
                             f'in range {self.glitch_min} to {self.glitch_max}, inclusive')
        if not (isinstance(glitch_change, (float, int)) and -self.glitch_max <= glitch_change <= self.glitch_max):
            raise ValueError(
                f'glitch_change parameter must be a number between {-self.glitch_max} and {self.glitch_max}, inclusive')
        if seed and not isinstance(seed, (float, int)):
            raise ValueError('seed parameter must be a number')
        if frames <= 0 or not isinstance(frames, int):
            raise ValueError(
                'frames param must be a positive integer value greater than 0')
        if step <= 0 or not isinstance(step, int):
            raise ValueError(
                'step parameter must be a positive integer value greater than 0')
        if not isinstance(cycle, bool):
            raise ValueError('cycle param must be a boolean')
        if not isinstance(color_offset, bool):
            raise ValueError('color_offset param must be a boolean')
        if not isinstance(scan_lines, bool):
            raise ValueError('scan_lines param must be a boolean')
        if not isinstance(gif, bool):
            raise ValueError('gif param must be a boolean')

        self.seed = seed
        if self.seed:
            # Set the seed if it was given
            self.__reset_rng_seed()

        try:
            # Get Image, whether input was an str path or Image object
            # GIF input is NOT allowed in this method
            img = _fetch_image(src_img, gif_allowed=False)
        except FileNotFoundError:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise FileNotFoundError(f'No image found at given path: {src_img}')
        # Fetching image attributes
        self.pixel_tuple_len = len(img.getbands())
        self.img_width, self.img_height = img.size
        self.img_mode = img.mode

        # Assigning the 3D arrays with pixel data
        self.input_array = np.asarray(img)
        self.output_array = np.array(img)

        # Glitching begins here
        if not gif:
            # Return glitched image
            return self.__get_glitched_img(glitch_amount, color_offset, scan_lines)

        # Return glitched GIF
        # Set up directory for storing glitched images
        if os.path.isdir(self.gif_dir_path):
            shutil.rmtree(self.gif_dir_path)
        os.mkdir(self.gif_dir_path)

        # Set up decimal precision for glitch_change
        original_precision = getcontext().prec
        getcontext().prec = 4

        glitched_images = []
        for i in range(frames):
            """
             * Glitch the image for n times
             * Where n is 0,1,2...frames
             * Save the image the in temp directory
             * Open the image and append a copy of it to the list
            """
            if i % step != 0:
                # Only every step'th frame should be glitched
                # Other frames will be appended as they are
                glitched_images.append(img.copy())
                continue
            glitched_img = self.__get_glitched_img(
                glitch_amount, color_offset, scan_lines)
            file_path = os.path.join(self.gif_dir_path, 'glitched_frame.png')
            glitched_img.save(file_path, compress_level=3)
            glitched_images.append(Image.open(file_path).copy())
            # Change glitch_amount by given value
            glitch_amount = self.__change_glitch(
                glitch_amount, glitch_change, cycle)

        # Set decimal precision back to original value
        getcontext().prec = original_precision
        # Cleanup
        shutil.rmtree(self.gif_dir_path)
        return glitched_images

    def glitch_gif(self, src_gif: Union[str, Image.Image], glitch_amount: Union[int, float],
                   seed: Union[int, float] = None, glitch_change: Union[int, float] = 0.0,
                   color_offset: bool = False, scan_lines: bool = False, gif: bool = False, cycle: bool = False,
                   step=1) -> Tuple[List[Image.Image], float, int]:
        """
         Glitch each frame of input GIF
         Returns the following:
         * List of PngImage objects,
         * Average duration (in centi seconds)
           of each frame in the original GIF,
         * Number of frames in the original GIF

         NOTE: This is a time-consuming process, especially for large GIFs
               with many frames
         PARAMETERS:-
         src_gif: Either the path to input Image or an Image object itself
         glitch_amount: Level of glitch intensity, [0.1, 10.0] (inclusive)

         glitch_change: Increment/Decrement in glitch_amount after every glitch
         cycle: Whether to cycle glitch_amount back to glitch_min or glitch_max
                if it over/underflow's
         color_offset: Specify True if color_offset effect should be applied
         scan_lines: Specify True if scan_lines effect should be applied
         step: Glitch every step'th frame, defaults to 1 (i.e all frames)
         seed: Set a random seed for generating similar images across runs,
               defaults to None (random seed)
        """

        # Sanity checking the params
        if not (isinstance(glitch_amount, (float, int)) and self.glitch_min <= glitch_amount <= self.glitch_max):
            raise ValueError('glitch_amount parameter must be a positive number '
                             f'in range {self.glitch_min} to {self.glitch_max}, inclusive')
        if not isinstance(glitch_change, (float, int)) or not -self.glitch_max <= glitch_change <= self.glitch_max:
            raise ValueError(
                f'glitch_change parameter must be a number between {-self.glitch_max} and {self.glitch_max}, inclusive')
        if seed and not isinstance(seed, (float, int)):
            raise ValueError('seed parameter must be a number')
        if step <= 0 or not isinstance(step, int):
            raise ValueError(
                'step parameter must be a positive integer value greater than 0')
        if not isinstance(cycle, bool):
            raise ValueError('cycle param must be a boolean')
        if not isinstance(color_offset, bool):
            raise ValueError('color_offset param must be a boolean')
        if not isinstance(scan_lines, bool):
            raise ValueError('scan_lines param must be a boolean')
        if not _is_gif(src_gif):
            raise Exception(
                'Input image must be a path to a GIF or be a GIF Image object')

        self.seed = seed
        if self.seed:
            # Set the seed if it was given
            self.__reset_rng_seed()

        try:
            # Get Image, whether input was an str path or Image object
            # GIF input is allowed in this method
            gif = _fetch_image(src_gif, gif_allowed=True)
        except FileNotFoundError:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise FileNotFoundError(f'No image found at given path: {src_gif}')
        # Set up directory for storing glitched images
        if os.path.isdir(self.gif_dir_path):
            shutil.rmtree(self.gif_dir_path)
        os.mkdir(self.gif_dir_path)

        # Set up decimal precision for glitch_change
        original_precision = getcontext().prec
        getcontext().prec = 4

        i = 0
        duration = 0
        glitched_images = []
        for frame in ImageSequence.Iterator(gif):
            """
             * Save each frame in the temp directory (always png)
             * Glitch the saved image
             * Save the glitched image in temp directory
             * Open the image and append a copy of it to the list
            """
            try:
                duration += frame.info['duration']
            except KeyError as e:
                # Override error message to provide more info
                e.args = (
                    'The key "duration" does not exist in frame.'
                    'This means PIL(pillow) could not extract necessary information from the input image',
                )
                raise
            src_frame_path = os.path.join(self.gif_dir_path, 'frame.png')
            frame.save(src_frame_path, compress_level=3)
            if i % step != 0:
                # Only every step'th frame should be glitched
                # Other frames will be appended as they are
                glitched_images.append(Image.open(src_frame_path).copy())
                i += 1
                continue
            glitched_img: Image.Image = self.glitch_image(src_frame_path, glitch_amount,
                                                          color_offset=color_offset, scan_lines=scan_lines)
            file_path = os.path.join(self.gif_dir_path, 'glitched_frame.png')
            glitched_img.save(file_path, compress_level=3)
            glitched_images.append(Image.open(file_path).copy())
            # Change glitch_amount by given value
            glitch_amount = self.__change_glitch(
                glitch_amount, glitch_change, cycle)
            i += 1

        # Set decimal precision back to original value
        getcontext().prec = original_precision
        # Cleanup
        shutil.rmtree(self.gif_dir_path)
        return glitched_images, duration / i, i

    def __change_glitch(self, glitch_amount: Union[int, float], glitch_change: Union[int, float], cycle: bool) -> float:
        # A function to change glitch_amount by given increment/decrement
        glitch_amount = float(Decimal(glitch_amount) + Decimal(glitch_change))
        # glitch_amount must be between glith_min and glitch_max
        if glitch_amount < self.glitch_min:
            # If it's less, it will be cycled back to max when cycle=True
            # Otherwise, it'll stay at the least possible value -> glitch_min
            glitch_amount = float(
                Decimal(self.glitch_max) + Decimal(glitch_amount)) if cycle else self.glitch_min
        if glitch_amount > self.glitch_max:
            # If it's more, it will be cycled back to min when cycle=True
            # Otherwise, it'll stay at the max possible value -> glitch_max
            glitch_amount = float(Decimal(glitch_amount) % Decimal(
                self.glitch_max)) if cycle else self.glitch_max
        return glitch_amount

    def __get_glitched_img(self, glitch_amount: Union[int, float], color_offset: int, scan_lines: bool) -> Image.Image:
        """
         Glitches the image located at given path
         Intensity of glitch depends on glitch_amount
        """
        max_offset = int((glitch_amount ** 2 / 100) * self.img_width)
        doubled_glitch_amount = int(glitch_amount * 2)
        for shift_number in range(doubled_glitch_amount):

            if self.seed:
                # This is not deterministic as glitch amount changes the amount of shifting,
                # so get the same values on each iteration on a new pseudo-seed that is
                # offset by the index we're iterating
                self.__reset_rng_seed(offset=shift_number)

            # Setting up offset needed for the randomized glitching
            current_offset = random.randint(-max_offset, max_offset)

            if current_offset == 0:
                # Can't wrap left OR right when offset is 0, End of Array
                continue
            if current_offset < 0:
                # Grab a rectangle of specific width and height, shift it left
                # by a specified offset
                # Wrap around the lost pixel data from the right
                self.__glitch_left(-current_offset)
            else:
                # Grab a rectangle of specific width and height, shift it right
                # by a specified offset
                # Wrap around the lost pixel data from the left
                self.__glitch_right(current_offset)

        if self.seed:
            # Get the same channels on the next call, we have to reset the rng seed
            # as the previous loop isn't fixed in size of iterations and depends on glitch amount
            self.__reset_rng_seed()

        if color_offset:
            # Get the next random channel we'll offset, needs to be before the random.randints
            # arguments because they will use up the original seed (if a custom seed is used)
            random_channel = self.__get_random_channel()
            # Add color channel offset if checked true
            self.__color_offset(random.randint(-doubled_glitch_amount, doubled_glitch_amount),
                                random.randint(-doubled_glitch_amount,
                                               doubled_glitch_amount),
                                random_channel)

        if scan_lines:
            # Add scan lines if checked true
            self.__add_scan_lines()

        # Creating glitched image from output array
        return Image.fromarray(self.output_array, self.img_mode)

    def __add_scan_lines(self):
        # Make every other row have only black pixels
        # Only the R, G, and B channels are assigned 0 values
        # Alpha is left untouched (if present)
        self.output_array[::2, :, :3] = [0, 0, 0]

    def __glitch_left(self, offset: int):
        """
         Grabs a rectangle from input array and shifts it leftwards
         Any lost pixel data is wrapped back to the right
         Rectangle's Width and Height are determined from offset

         Consider an array like so-
         [[ 0, 1, 2, 3],
         [ 4, 5, 6, 7],
         [ 8, 9, 10, 11],
         [12, 13, 14, 15]]
         If we were to left shift the first row only, starting from the 1st index;
         i.e a rectangle of width = 3, height = 1, starting at (0, 0)
         We'd grab [1, 2, 3] and left shift it until the start of row,
         so it'd look like [[1, 2, 3, 3]]
         Now we wrap around the lost values, i.e 0
         now it'd look like [[1, 2, 3, 0]]
         That's the end result!
        """
        # Setting up values that will determine the rectangle height
        start_y = random.randint(0, self.img_height)
        chunk_height = random.randint(1, int(self.img_height / 4))
        chunk_height = min(chunk_height, self.img_height - start_y)
        stop_y = start_y + chunk_height

        # For copy
        start_x = offset
        # For paste
        stop_x = self.img_width - start_x

        left_chunk = self.input_array[start_y:stop_y, start_x:]
        wrap_chunk = self.input_array[start_y:stop_y, :start_x]
        self.output_array[start_y:stop_y, :stop_x] = left_chunk
        self.output_array[start_y:stop_y, stop_x:] = wrap_chunk

    def __glitch_right(self, offset: int):
        """
         Grabs a rectangle from input_array and shifts it rightwards
         Any lost pixel data is wrapped back to the left
         Rectangle's Width and Height are determined from offset

         Consider an array like so-
         [[ 0, 1, 2, 3],
         [ 4, 5, 6, 7],
         [ 8, 9, 10, 11],
         [12, 13, 14, 15]]
         If we were to right shift the first row only, starting from
         the 0th index;
         i.e a rectangle of width = 3, height = 1 starting at (0, 0)
         We'd grab [0, 1, 2] and right shift it until the end of row,
         so it'd look like [[0, 0, 1, 2]]
         Now we wrap around the lost values, i.e 3
         now it'd look like [[3, 0, 1, 2]]
         That's the end result!
        """
        # Setting up values that will determine the rectangle height
        start_y = random.randint(0, self.img_height)
        chunk_height = random.randint(1, int(self.img_height / 4))
        chunk_height = min(chunk_height, self.img_height - start_y)
        stop_y = start_y + chunk_height

        # For copy
        stop_x = self.img_width - offset
        # For paste
        start_x = offset

        right_chunk = self.input_array[start_y:stop_y, :stop_x]
        wrap_chunk = self.input_array[start_y:stop_y, stop_x:]
        self.output_array[start_y:stop_y, start_x:] = right_chunk
        self.output_array[start_y:stop_y, :start_x] = wrap_chunk

    def __color_offset(self, offset_x: int, offset_y: int, channel_index: int):
        """
         Takes the given channel's color value from input_array,
         starting from (0, 0)
         and puts it in the same channel's slot in output_array,
         starting from (offset_y, offset_x)
        """
        # Make sure offset_x isn't negative in the actual algo
        offset_x = offset_x if offset_x >= 0 else self.img_width + offset_x
        offset_y = offset_y if offset_y >= 0 else self.img_height + offset_y

        # Assign values from 0th row of input_array to offset_y th
        # row of output_array
        # If output_array's columns run out before input_array's does,
        # wrap the remaining values around
        self.output_array[offset_y, offset_x:, channel_index] = self.input_array[0, :self.img_width - offset_x, channel_index]
        self.output_array[offset_y, :offset_x, channel_index] = self.input_array[0, self.img_width - offset_x:, channel_index]

        # Continue afterwards till end of output_array
        # Make sure the width and height match for both slices
        self.output_array[offset_y + 1:, :, channel_index] = self.input_array[1:self.img_height - offset_y, :, channel_index]

        # Restart from 0th row of output_array and go until the offset_y th row
        # This will assign the remaining values in input_array to output_array
        self.output_array[:offset_y, :, channel_index] = self.input_array[self.img_height - offset_y:, :, channel_index]

    def __get_random_channel(self) -> int:
        # Returns a random index from 0 to pixel_tuple_len
        # For an RGB image, a 0th index represents the RED channel

        return random.randint(0, self.pixel_tuple_len - 1)

    def __reset_rng_seed(self, offset: int = 0):
        """
        Calls random.seed() with self.seed variable

        offset is for looping and getting new positions for each iteration that contains the
        previous one, otherwise we would get the same position on every loop and different 
        results afterwards on non-fixed size loops
        """
        random.seed(self.seed + offset)
