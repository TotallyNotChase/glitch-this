import os, shutil
import numpy as np
from random import randint
from PIL import Image, ImageSequence

class ImageGlitcher:
# Handles Image/GIF Glitching Operations

    __version__ = '0.0.9'

    def __init__(self):
        # Setting up global variables needed for glitching
        self.pixel_tuple_len = 0
        self.img_width, self.img_height = 0, 0
        self.img_mode = 'Unknown'

        # Creating 3D arrays for pixel data
        self.inputarr = None
        self.outputarr = None

        # Getting PATH of temp folders
        self.lib_path = os.path.split(os.path.abspath(__file__))[0]
        self.gif_dirpath = os.path.join(self.lib_path, 'Glitched GIF')

    def __isgif(self, img):
        # Returns true if input image is a GIF and/or animated
        if isinstance(img, str):
            return img.endswith('.gif')
        index = 0
        for frame in ImageSequence.Iterator(img):
            # More than one frames means image is animated
            index += 1
            if index >= 2:
                return True
        return False

    def __open_image(self, img_path):
        # Returns an Image object
        # Will throw exception if img_path doesn't point to Image
        if img_path.endswith('.gif'):
            # Do not convert GIF file
            return Image.open(img_path)
        elif img_path.endswith('.png'):
            # Convert the Image to RGBA if it's png
            return Image.open(img_path).convert('RGBA')
        else:
            # Otherwise convert it to RGB
            return Image.open(img_path).convert('RGB')

    def __fetch_image(self, src_img, gif_allowed):
        """
         The following code resolves whether input was a path or an Image
         Then returns an Image object

         Raises an exception if `img` param is not an Image
        """
        if isinstance(src_img, str) and (gif_allowed or not src_img.endswith('.gif')):
            """
             An str object was passed

             If GIF is not allowed and the Image path is a GIF
             the function will raise an Exception
             If GIF is allowed, any Image path is good to go
            """
            # Sanity Check if the path exists
            if not os.path.isfile(src_img):
                raise FileNotFoundError('No image found at given path')
            try:
                # Open the image at given path
                img = self.__open_image(src_img)
            except:
                # File is not an Image
                raise Exception('Wrong format')
        elif isinstance(src_img, Image.Image) and (gif_allowed or not self.__isgif(src_img)):
            """
             An Image object was passed

             If GIF is not allowed and the Image object is a GIF
             the function will raise an Exception
             If GIF is allowed, any Image object is good to go
            """
            if src_img.format == 'GIF':
                # Do not convert GIF file
                return src_img
            elif src_img.format == 'PNG':
                # Convert the Image to RGBA if it's png
                img = src_img.convert('RGBA')
            else:
                # Otherwise convert it to RGB
                img = src_img.convert('RGB')
        else:
            # File is not an Image
            # OR it's a GIF but GIF is not allowed

            # Raise the GENERIC exception here
            raise Exception('Wrong format')
        return img

    def glitch_image(self, src_img, glitch_amount, color_offset=False, scan_lines=False, gif=False, frames=23):
        """
         Sets up values needed for glitching the image
         Returns created Image object if gif=False
         Returns list of Image objects if gif=True

         PARAMETERS:-
         src_img: Either the path to input Image or an Image object itself
         glitch_amount: Level of glitch intensity, [1, 10] (inclusive)

         color_offset: Specify True if color_offset effect should be applied
         scan_lines: Specify True if scan_lines effect should be applied
         gif: True if output should be ready to be saved as GIF
         frames: How many glitched frames should be generated for GIF
        """
        # Sanity checking the inputs
        if not 1 <= glitch_amount <= 10:
            raise ValueError('glitch_amount parameter must be in range 1 to 10, inclusive')

        try:
            # Get Image, whether input was an str path or Image object
            # GIF input is NOT allowed in this method
            img = self.__fetch_image(src_img, False)
        except:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise Exception('File format not supported - must be a non-animated image file')

        # Fetching image attributes
        self.pixel_tuple_len = len(img.getbands())
        self.img_width, self.img_height = img.size
        self.img_mode = img.mode

        # Assigning the 3D arrays with pixel data
        self.inputarr = np.asarray(img)
        self.outputarr = np.array(img)

        # Glitching begins here
        if not gif:
            # Return glitched image
            return self.__get_glitched_img(glitch_amount, color_offset, scan_lines)

        # Return glitched GIF
        # Set up directory for storing glitched images
        if os.path.isdir(self.gif_dirpath):
            shutil.rmtree(self.gif_dirpath)
        os.mkdir(self.gif_dirpath)

        glitched_imgs = []
        for _ in range(frames):
            """
             * Glitch the image for n times
             * Where n is 0,1,2...frames
             * Save the image the in temp directory
             * Open the image and append a copy of it to the list
            """
            glitched_img  = self.__get_glitched_img(glitch_amount, color_offset, scan_lines)
            file_path = os.path.join(self.gif_dirpath, 'glitched_frame.png')
            glitched_img.save(file_path)
            glitched_imgs.append(Image.open(file_path).copy())

        # Cleanup
        shutil.rmtree(self.gif_dirpath)
        return glitched_imgs

    def glitch_gif(self, src_gif, glitch_amount, color_offset=False, scan_lines=False):
        """
         Glitch each frame of input GIF
         Returns the following:
         * List of PngImage objects,
         * Average duration (in centiseconds)
           of each frame in the original GIF,
         * Number of frames in the original GIF

         NOTE: This is a time consuming process, especially for large GIFs
               with many frames
         PARAMETERS:-
         src_img: Either the path to input Image or an Image object itself
         glitch_amount: Level of glitch intensity, [1, 10] (inclusive)

         color_offset: Specify True if color_offset effect should be applied
         scan_lines: Specify True if scan_lines effect should be applied
        """
        # Sanity checking the inputs
        if not 1 <= glitch_amount <= 10:
            raise ValueError('glitch_amount parameter must be in range 1 to 10, inclusive')
        if not self.__isgif(src_gif):
            raise Exception('Input image must be a path to a GIF or be a GIF Image object')

        try:
            # Get Image, whether input was an str path or Image object
            # GIF input is allowed in this method
            gif = self.__fetch_image(src_gif, True)
        except:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise Exception('File format not supported - must be an image file')

        # Set up directory for storing glitched images
        if os.path.isdir(self.gif_dirpath):
            shutil.rmtree(self.gif_dirpath)
        os.mkdir(self.gif_dirpath)

        i = 0
        duration = 0
        glitched_imgs = []
        for frame in ImageSequence.Iterator(gif):
            """
             * Save each frame in the temp directory (always png)
             * Glitch the saved image
             * Save the glitched image in temp directory
             * Open the image and append a copy of it to the list
            """
            duration += frame.info['duration']
            file_path = os.path.join(self.gif_dirpath, 'frame.png')
            frame.save(file_path)
            glitched_img  = self.glitch_image(file_path, glitch_amount, color_offset, scan_lines)
            file_path = os.path.join(self.gif_dirpath, 'glitched_{}.png'.format(str(i)))
            glitched_img.save(file_path)
            glitched_imgs.append(Image.open(file_path).copy())
            i += 1
        # Cleanup
        shutil.rmtree(self.gif_dirpath)
        return glitched_imgs, duration / i, i

    def __get_glitched_img(self, glitch_amount, color_offset, scan_lines):
        """
         Glitches the image located at given path
         Intensity of glitch depends on glitch_amount
        """
        max_offset = int((glitch_amount ** 2 / 100) * self.img_width)
        for _ in range(0, glitch_amount * 2):
            # Setting up offset needed for the randomized glitching
            current_offset = randint(-max_offset, max_offset)

            if current_offset == 0:
                # Can't wrap left OR right when offset is 0, End of Array
                continue
            if current_offset < 0:
                # Grab a rectangle of specific width and heigh, shift it left
                # by a specified offset
                # Wrap around the lost pixel data from the right
                self.__glitch_left(-current_offset)
            else:
                # Grab a rectangle of specific width and height, shift it right
                # by a specified offset
                # Wrap around the lost pixel data from the left
                self.__glitch_right(current_offset)

        if color_offset:
            # Add color channel offset if checked true
            self.__color_offset(randint(-glitch_amount * 2, glitch_amount * 2),
                              randint(-glitch_amount * 2, glitch_amount * 2),
                              self.__get_random_channel())

        if scan_lines:
            # Add scan lines if checked true
            self.__add_scan_lines()

        # Creating glitched image from output array
        return Image.fromarray(self.outputarr, self.img_mode)

    def __add_scan_lines(self):

        # Make every other row have only black pixels

        self.outputarr[::2, :, :3] = [0, 0, 0]

    def __glitch_left(self, offset):
        """
         Grabs a rectange from inputarr and shifts it leftwards
         Any lost pixel data is wrapped back to the right
         Rectangle's Width and Height are determined from offset

         Consider an array like so-
         [[ 0, 1, 2, 3],
         [ 4, 5, 6, 7],
         [ 8, 9, 10, 11],
         [12, 13, 14, 15]]
         If we were to left shift the first row only, starting from the 1st index;
         i.e a rectangle of width = 3, height = 1, starting at (0, 0)
         We'd grab [1, 2, 3] and left shift it until the start of row
         so it'd look like [[1, 2, 3, 3]]
         Now we wrap around the lost values, i.e 0
         now it'd look like [[1, 2, 3, 0]]
         That's the end result!
        """
        # Setting up values that will determine the rectangle height
        start_y = randint(0, self.img_height)
        chunk_height = randint(1, int(self.img_height / 4))
        chunk_height = min(chunk_height, self.img_height - start_y)
        stop_y = start_y + chunk_height

        # For copy
        start_x = offset
        # For paste
        stop_x = self.img_width - start_x

        left_chunk = self.inputarr[start_y:stop_y, start_x:]
        wrap_chunk = self.inputarr[start_y:stop_y, :start_x]
        self.outputarr[start_y:stop_y, :stop_x] = left_chunk
        self.outputarr[start_y:stop_y, stop_x:] = wrap_chunk

    def __glitch_right(self, offset):
        """
         Grabs a rectange from inputarr and shifts it rightwards
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
         We'd grab [0, 1, 2] and right shift it until the end of row
         so it'd look like [[0, 0, 1, 2]]
         Now we wrap around the lost values, i.e 3
         now it'd look like [[3, 0, 1, 2]]
         That's the end result!
        """
        # Setting up values that will determine the rectangle height
        start_y = randint(0, self.img_height)
        chunk_height = randint(1, int(self.img_height / 4))
        chunk_height = min(chunk_height, self.img_height - start_y)
        stop_y = start_y + chunk_height

        # For copy
        stop_x = self.img_width - offset
        # For paste
        start_x = offset

        right_chunk = self.inputarr[start_y:stop_y, :stop_x]
        wrap_chunk = self.inputarr[start_y:stop_y, stop_x:]
        self.outputarr[start_y:stop_y, start_x:] = right_chunk
        self.outputarr[start_y:stop_y, :start_x] = wrap_chunk

    def __color_offset(self, offset_x, offset_y, channel_index):
        """
         Takes the given channel's color value from inputarr,
         starting from (0, 0)
         and puts it in the same channel's slot in outputarr,
         starting from (offset_y, offset_x)
        """
         # Make sure offset_x isn't negative in the actual algo
        offset_x = offset_x if offset_x >= 0 else self.img_width + offset_x
        offset_y = offset_y if offset_y >= 0 else self.img_height + offset_y

        # Assign values from 0th row of inputarr to offset_y th
        # row of outputarr
        # If outputarr's columns run out before inputarr's does,
        # wrap the remaining values around
        self.outputarr[offset_y,
                       offset_x:,
                       channel_index] = self.inputarr[0,
                                                      :self.img_width - offset_x,
                                                      channel_index]
        self.outputarr[offset_y,
                       :offset_x,
                       channel_index] = self.inputarr[0,
                                                      self.img_width - offset_x:,
                                                      channel_index]

        # Continue afterwards till end of outputarr
        # Make sure the width and height match for both slices
        self.outputarr[offset_y + 1:,
                       :,
                       channel_index] = self.inputarr[1:self.img_height - offset_y,
                                                      :,
                                                      channel_index]

        # Restart from 0th row of outputarr and go until the offset_y th row
        # This will assign the remaining values in inputarr to outputarr
        self.outputarr[:offset_y,
                       :,
                       channel_index] = self.inputarr[self.img_height - offset_y:,
                                                      :,
                                                      channel_index]

    def __get_random_channel(self):
        # Returns a random index from 0 to pixel_tuple_len
        # For an RGB image, a 0th index represents the RED channel
        return randint(0, self.pixel_tuple_len - 1)
