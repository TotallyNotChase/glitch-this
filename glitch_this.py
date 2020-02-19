from PIL import Image
from random import randint
from time import time
import numpy as np
import os, argparse

# Add commandline arguments parser
argparser = argparse.ArgumentParser(description = 'Create glitched images or GIFs from an image!')
argparser.add_argument('src_img_path', metavar = 'Image_Path', type = str, help = 'Relative or Absolute string path to source image')
argparser.add_argument('glitch_level', metavar = 'Glitch_Level', type = int, help = 'Integer between 1 and 10, inclusive, representing amount of glitchiness')
args = argparser.parse_args()

# Sanity checking the inputs
if not 1 <= args.glitch_level <= 10:
    raise Exception('glitch_amount parameter must be in range 1 to 10, inclusive')
if not os.path.exists(args.src_img_path):
    raise Exception('No image found at given path')

def glitch_left(offset):
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
    start_y = randint(0, img_height)
    chunk_height = randint(1, int(img_height / 4))
    chunk_height = min(chunk_height, img_height - start_y)
    stop_y = start_y + chunk_height

    # For copy
    start_x = offset
    # For paste
    stop_x = img_width - start_x

    left_chunk = inputarr[start_y : stop_y, start_x : ]
    wrap_chunk = inputarr[start_y : stop_y, : start_x]
    outputarr[start_y : stop_y, : stop_x] = left_chunk
    outputarr[start_y : stop_y, stop_x : ] = wrap_chunk

def glitch_right(offset):
    """
    Grabs a rectange from inputarr and shifts it rightwards
    Any lost pixel data is wrapped back to the left
    Rectangle's Width and Height are determined from offset

    Consider an array like so-
    [[ 0, 1, 2, 3],
    [ 4, 5, 6, 7],
    [ 8, 9, 10, 11],
    [12, 13, 14, 15]]
    If we were to left shift the first row only, starting from the 1st index;
    i.e a rectangle of width = 3, height = 1, starting at (0, 0)
    We'd grab [0, 1, 2] and right shift it until the end of row
    so it'd look like [[0, 0, 1, 2]]
    Now we wrap around the lost values, i.e 3
    now it'd look like [[3, 0, 1, 2]]
    That's the end result!
    """
    start_y = randint(0, img_height)
    chunk_height = randint(1, int(img_height / 4))
    chunk_height = min(chunk_height, img_height - start_y)
    stop_y = start_y + chunk_height

    # For copy
    stop_x = img_width - offset
    # For paste
    start_x = offset

    right_chunk = inputarr[start_y : stop_y, : stop_x]
    wrap_chunk = inputarr[start_y : stop_y, stop_x : ]
    outputarr[start_y : stop_y, start_x : ] = right_chunk
    outputarr[start_y : stop_y, : start_x] = wrap_chunk


def color_offset(offset_x, offset_y, channel_index):
    """
     Takes the given channel's color value from inputarr, starting from (0, 0)
     and puts it in the same channel's slot in outputarr, starting from (offset_y, offset_x)
    """
        # Make sure offset_x isn't negative in the actual algo
    offset_x = offset_x if offset_x >= 0 else img_width + offset_x
    offset_y = offset_y if offset_y >= 0 else img_height + offset_y

    # Assign values from 0th row of inputarr to offset_y th row of outputarr
    # If outputarr's columns run out before inputarr's does, wrap the remaining values around
    outputarr[offset_y, offset_x:, channel_index] = inputarr[0, :img_width - offset_x, channel_index]
    outputarr[offset_y, :offset_x, channel_index] = inputarr[0, img_width - offset_x:, channel_index]

    # Continue afterwards till end of outputarr
    # Make sure the width and height match for both slices in this case
    outputarr[offset_y + 1: , :, channel_index] = inputarr[1:img_height - offset_y, :, channel_index]

    # Restart from 0th row of outputarr and go until the offset_y th row
    # This will assign the remaining values in inputarr to outputarr
    outputarr[:offset_y, :, channel_index] = inputarr[img_height - offset_y: , :, channel_index]

def get_random_channel():
    # Returns a random index from 0 to pixel_tuple_len
    # For an RGB image, a 0th index represents the RED channel
    return randint(0, pixel_tuple_len - 1)

if __name__ == '__main__':
    try:
        src_img = Image.open(args.src_img_path)
    except:
        raise Exception('File format not supported - must be an image file')

    t0 = time()
    # Fetching image attributes
    pixel_tuple_len = len(src_img.getbands())
    img_width, img_height = src_img.size
    img_filename = src_img.filename
    img_mode = src_img.mode

    # Assigning global img attributes
    img_width = img_width
    img_height = img_height
    pixel_tuple_len = pixel_tuple_len

    # Creating 3D arrays with pixel data
    inputarr = np.asarray(src_img)
    outputarr = np.array(src_img)

    # Glitching begins here
    glitch_amount = args.glitch_level
    max_offset = int((glitch_amount ** 2 / 100) * img_width)
    for _ in range(0, glitch_amount * 2):
        # Setting up values needed for the randomized glitching
        start_y = randint(0, img_height)
        chunk_height = randint(1, int(img_height / 4))
        chunk_height = min(chunk_height, img_height - start_y)
        current_offset = randint(-max_offset, max_offset)

        if current_offset is 0:
            # Can't wrap left OR right when offset is 0, End of Array
            continue
        if current_offset < 0:
            # Grab a rectangle of specific width and heigh, shift it left by a specified offset
            # Wrap around the lost pixel data from the right
            glitch_left(-current_offset)
        else:
            # Grab a rectangle of specific width and height, shift it right by a specified offset
            # Wrap around the lost pixel data from the left
            glitch_right(current_offset)

    # Converting 3D array to 2D array, Ex - breaking down [[[R, G, B]....]] to [[R, G, B...]]
    inputarr = inputarr.reshape(img_height, -1)
    outputarr = outputarr.reshape(img_height, -1)

    # Channel offset for glitched colors
    # The start point (x, y) is randomized and the end point is always (img_width, img_height)
    color_offset(randint(-glitch_amount, glitch_amount), randint(-glitch_amount, glitch_amount), get_random_channel())
    # Converting 2D array back to original 3D array
    outputarr = np.reshape(outputarr, (img_height, img_width, pixel_tuple_len))

    # Creating glitched image from output array
    glitch_img = Image.fromarray(outputarr, img_mode)
    glitch_img.save('glitched_{}'.format(img_filename))
    t1 = time()
    print('Glitched image saved as "glitched_{}"'.format(img_filename))
    print('Time taken: ' + str(t1 - t0))
