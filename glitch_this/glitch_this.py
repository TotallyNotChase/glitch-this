from PIL import Image
from random import randint
import numpy as np
import os

class ImageGlitcher:
# Handles Image/GIF Glitching Operations

    def glitch_image(self, src_img_path, glitch_amount):
        """
         Glitches the image located at given path
         Intensity of glitch depends on glitch_amount
        """
        # Sanity checking the inputs
        if not 1 <= glitch_amount <= 10:
            raise Exception('glitch_amount parameter must be in range 1 to 10, inclusive')
        if not os.path.exists(src_img_path):
            raise Exception('No image found at given path')

        try:
            src_img = Image.open(src_img_path)
        except:
            raise Exception('File format not supported - must be an image file')

        # Fetching image attributes
        pixel_tuple_len = len(src_img.getbands())
        img_width, img_height = src_img.size
        img_filename = src_img.filename
        img_mode = src_img.mode

        # Assigning global img attributes
        self.img_width = img_width
        self.img_height = img_height
        self.pixel_tuple_len = pixel_tuple_len

        # Creating 3D arrays with pixel data
        self.inputarr = np.asarray(src_img)
        self.outputarr = np.array(src_img)

        # Glitching begins here

        max_offset = int((glitch_amount ** 2 / 100) * img_width)
        for _ in range(0, glitch_amount * 2):
            # Setting up offset needed for the randomized glitching
            current_offset = randint(-max_offset, max_offset)

            if current_offset is 0:
                # Can't wrap left OR right when offset is 0, End of Array
                continue
            if current_offset < 0:
                # Grab a rectangle of specific width and heigh, shift it left by a specified offset
                # Wrap around the lost pixel data from the right
                self.glitch_left(-current_offset)
            else:
                # Grab a rectangle of specific width and height, shift it right by a specified offset
                # Wrap around the lost pixel data from the left
                self.glitch_right(current_offset)

        # Channel offset for glitched colors
        # The start point (y, x) as well as the channel is randomized
        self.color_offset(randint(-glitch_amount * 2, glitch_amount * 2), randint(-glitch_amount * 2, glitch_amount * 2), self.get_random_channel())

        # Creating glitched image from output array
        glitch_img = Image.fromarray(self.outputarr, img_mode)
        return glitch_img

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

        left_chunk = self.inputarr[start_y : stop_y, start_x : ]
        wrap_chunk = self.inputarr[start_y : stop_y, : start_x]
        self.outputarr[start_y : stop_y, : stop_x] = left_chunk
        self.outputarr[start_y : stop_y, stop_x : ] = wrap_chunk

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
         If we were to right shift the first row only, starting from the 0th index;
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

        right_chunk = self.inputarr[start_y : stop_y, : stop_x]
        wrap_chunk = self.inputarr[start_y : stop_y, stop_x : ]
        self.outputarr[start_y : stop_y, start_x : ] = right_chunk
        self.outputarr[start_y : stop_y, : start_x] = wrap_chunk

    def color_offset(self, offset_x, offset_y, channel_index):
        """
         Takes the given channel's color value from inputarr, starting from (0, 0)
         and puts it in the same channel's slot in outputarr, starting from (offset_y, offset_x)
        """
         # Make sure offset_x isn't negative in the actual algo
        offset_x = offset_x if offset_x >= 0 else self.img_width + offset_x
        offset_y = offset_y if offset_y >= 0 else self.img_height + offset_y

        # Assign values from 0th row of inputarr to offset_y th row of outputarr
        # If outputarr's columns run out before inputarr's does, wrap the remaining values around
        self.outputarr[offset_y, offset_x:, channel_index] = self.inputarr[0, :self.img_width - offset_x, channel_index]
        self.outputarr[offset_y, :offset_x, channel_index] = self.inputarr[0, self.img_width - offset_x:, channel_index]

        # Continue afterwards till end of outputarr
        # Make sure the width and height match for both slices in this case
        self.outputarr[offset_y + 1: , :, channel_index] = self.inputarr[1:self.img_height - offset_y, :, channel_index]

        # Restart from 0th row of outputarr and go until the offset_y th row
        # This will assign the remaining values in inputarr to outputarr
        self.outputarr[:offset_y, :, channel_index] = self.inputarr[self.img_height - offset_y: , :, channel_index]

    def get_random_channel(self):
        # Returns a random index from 0 to pixel_tuple_len
        # For an RGB image, a 0th index represents the RED channel
        return randint(0, self.pixel_tuple_len - 1)
