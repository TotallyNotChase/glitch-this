import os
import numpy as np
from random import randint
from PIL import Image

class ImageGlitcher:
# Handles Image/GIF Glitching Operations

    def __init__(self):
        # Setting up global variables needed for glitching
        self.pixel_tuple_len = 0
        self.img_width, self.img_height = 0, 0
        self.img_mode = 'Unknown'

        # Creating 3D arrays for pixel data
        self.inputarr = None
        self.outputarr = None

    def glitch_image(self, src_img_path, glitch_amount, scan_lines=False):
        """
         Sets up values needed for glitching the image
         Returns created Image object
        """
        # Sanity checking the inputs
        if not 1 <= glitch_amount <= 10:
            raise Exception('glitch_amount parameter must be in range 1 to 10, inclusive')
        if not os.path.exists(src_img_path):
            raise Exception('No image found at given path')

        try:
            src_img = Image.open(src_img_path).convert('RGBA')
        except:
            raise Exception('File format not supported - must be an image file')

        # Fetching image attributes
        self.pixel_tuple_len = len(src_img.getbands())
        self.img_width, self.img_height = src_img.size
        self.img_mode = src_img.mode

        # Assigning the 3D arrays with pixel data
        self.inputarr = np.asarray(src_img)
        self.outputarr = np.array(src_img)

        # Glitching begins here
        return self.get_glitched_img(glitch_amount, scan_lines)

    def get_glitched_img(self, glitch_amount, scan_lines):
        """
         Glitches the image located at given path
         Intensity of glitch depends on glitch_amount
        """
        max_offset = int((glitch_amount ** 2 / 100) * self.img_width)
        for _ in range(0, glitch_amount * 2):
            # Setting up offset needed for the randomized glitching
            current_offset = randint(-max_offset, max_offset)

            if current_offset is 0:
                # Can't wrap left OR right when offset is 0, End of Array
                continue
            if current_offset < 0:
                # Grab a rectangle of specific width and heigh, shift it left
                # by a specified offset
                # Wrap around the lost pixel data from the right
                self.glitch_left(-current_offset)
            else:
                # Grab a rectangle of specific width and height, shift it right
                # by a specified offset
                # Wrap around the lost pixel data from the left
                self.glitch_right(current_offset)

        # Channel offset for glitched colors
        # The start point (y, x) is randomized
        self.color_offset(randint(-glitch_amount * 2, glitch_amount * 2),
                          randint(-glitch_amount * 2, glitch_amount * 2),
                          self.get_random_channel())

        if scan_lines and self.pixel_tuple_len >= 3:

            # Add scan lines if checked true

            # Input picture must be RGB or RGBA

            self.add_scan_lines()


        # Creating glitched image from output array
        return Image.fromarray(self.outputarr, self.img_mode)

    def add_scan_lines(self):

        # Make every other row have only black pixels

        self.outputarr[::2, :, :3] = [0, 0, 0]

    def glitch_left(self, offset):
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

    def glitch_right(self, offset):
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

    def color_offset(self, offset_x, offset_y, channel_index):
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

    def get_random_channel(self):
        # Returns a random index from 0 to pixel_tuple_len
        # For an RGB image, a 0th index represents the RED channel
        return randint(0, self.pixel_tuple_len - 1)
