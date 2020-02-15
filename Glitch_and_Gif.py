from PIL import Image
from random import random
import numpy as np


def glitch_left(start_copy_x, start_copy_y, width, height, paste_x, paste_y):
    left_chunk = inputarr[start_copy_y : start_copy_y + height, start_copy_x : column_length]
    wrap_chunk = inputarr[start_copy_y : start_copy_y + height, 0 : start_copy_x]
    outputarr[paste_y : paste_y + height, paste_x : paste_x + width] = left_chunk
    outputarr[paste_y : paste_y + height, paste_x + width : column_length] = wrap_chunk

def glitch_right(start_copy_x, start_copy_y, width, height, paste_x, paste_y):
    right_chunk = inputarr[start_copy_y : start_copy_y + height, start_copy_x : width]
    wrap_chunk = inputarr[start_copy_y : start_copy_y + height, width : column_length]
    outputarr[paste_y : paste_y + height, paste_x : paste_x + width] = right_chunk
    outputarr[paste_y : paste_y + height, 0 : paste_x] = wrap_chunk

def get_randint(min, max):
    return int(random() * (max - min) + min)

src_img = Image.open('test.png')
# Fetching image attributes
pixel_tuple_len = len(src_img.getbands())
img_filename = src_img.filename
img_width, img_height = src_img.size
img_mode = src_img.mode

# Creating 2D arrays with pixel data
inputarr = np.asarray(src_img).reshape(img_height, -1)
outputarr = np.array(src_img).reshape(img_height, -1)
column_length = img_width * pixel_tuple_len

# Glitching begins here

glitch_amount = 3
max_offset = int((glitch_amount ** 2 / 100) * column_length)
for i in range(0, glitch_amount * 2):
    # Setting up values needed for the randomized glitching
    start_y = get_randint(0, img_height)
    chunk_height = get_randint(1, int(img_height / 4))
    chunk_height = min(chunk_height, img_height - start_y)
    current_offset = get_randint(-max_offset, max_offset)

    if current_offset is 0:
        # Can't wrap left OR right when offset is 0, End of Array
        continue
    if current_offset < 0: 
        glitch_left(-current_offset, start_y, column_length + current_offset, chunk_height, 0, start_y)
    else:
        glitch_right(0, start_y, column_length - current_offset, chunk_height, current_offset, start_y)

# Converting 2D array back to original 3D array and saving as glitched image
outputarr = np.reshape(outputarr, (img_height, img_width, pixel_tuple_len))
glitch_img = Image.fromarray(outputarr, img_mode)
glitch_img.save('glitched_{}'.format(img_filename))