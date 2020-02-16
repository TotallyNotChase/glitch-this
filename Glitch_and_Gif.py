from PIL import Image
from random import randint
import numpy as np

def glitch_left(start_copy_x, start_copy_y, width, height, start_paste_x, start_paste_y):
    left_chunk = inputarr[start_copy_y : start_copy_y + height, start_copy_x : img_width]
    wrap_chunk = inputarr[start_copy_y : start_copy_y + height, 0 : start_copy_x]
    outputarr[start_paste_y : start_paste_y + height, start_paste_x : start_paste_x + width] = left_chunk
    outputarr[start_paste_y : start_paste_y + height, start_paste_x + width : img_width] = wrap_chunk

def glitch_right(start_copy_x, start_copy_y, width, height, paste_x, paste_y):
    right_chunk = inputarr[start_copy_y : start_copy_y + height, start_copy_x : width]
    wrap_chunk = inputarr[start_copy_y : start_copy_y + height, width : img_width]
    outputarr[paste_y : paste_y + height, paste_x : paste_x + width] = right_chunk
    outputarr[paste_y : paste_y + height, 0 : paste_x] = wrap_chunk

def get_random_channel():
    return randint(0, pixel_tuple_len - 1)

def copy_channel(start_copy_x, start_copy_y, width, height, channel_index):
    start_y = start_copy_y
    stop_y = start_y + height
    start_x = (start_copy_x - 1) * pixel_tuple_len + channel_index
    stop_x = start_x + width * pixel_tuple_len
    step_x = pixel_tuple_len
    return inputarr[start_y : stop_y, start_x : stop_x : step_x]

def paste_channel(start_paste_x, start_paste_y, width, height, channel_index, channel_chunk):
    start_y = start_paste_y
    stop_y = start_y + height
    start_x = (start_paste_x - 1) * pixel_tuple_len + channel_index
    stop_x = start_x + width * pixel_tuple_len
    step_x = pixel_tuple_len
    outputarr[start_y : stop_y, start_x : stop_x : step_x] = channel_chunk

src_img = Image.open('test.png')
# Fetching image attributes
pixel_tuple_len = len(src_img.getbands())
img_filename = src_img.filename
img_width, img_height = src_img.size
img_mode = src_img.mode
column_length = img_width * pixel_tuple_len

# Creating 2D arrays with pixel data
inputarr = np.asarray(src_img)
outputarr = np.array(src_img)

# Glitching begins here

glitch_amount = 2
max_offset = int((glitch_amount ** 2 / 100) * img_width)
for i in range(0, glitch_amount * 2):
    # Setting up values needed for the randomized glitching
    start_y = randint(0, img_height)
    chunk_height = randint(1, int(img_height / 4))
    chunk_height = min(chunk_height, img_height - start_y)
    current_offset = randint(-max_offset, max_offset)

    if current_offset is 0:
        # Can't wrap left OR right when offset is 0, End of Array
        continue
    if current_offset < 0: 
        glitch_left(-current_offset, start_y, img_width + current_offset, chunk_height, 0, start_y)
    else:
        glitch_right(0, start_y, img_width - current_offset, chunk_height, current_offset, start_y)

# Converting 3D array to 2D array, Ex - breaking down [[[R, G, B]....]] to [[R, G, B...]]
inputarr = inputarr.reshape(img_height, -1)
outputarr = outputarr.reshape(img_height, -1)

# Channel offset for glitched colors
channel_chunk_start_x = randint(0, int(img_width / 4))
channel_chunk_width = img_width - channel_chunk_start_x
channel_chunk_start_y = randint(0, int(img_height / 4))
channel_chunk_height = img_height - channel_chunk_start_y

channel_index = get_random_channel()
channel_chunk = copy_channel(channel_chunk_start_x, channel_chunk_start_y, channel_chunk_width, channel_chunk_height, channel_index)
paste_channel(randint(0, channel_chunk_start_x), randint(0, channel_chunk_start_y), channel_chunk_width, channel_chunk_height, channel_index, channel_chunk)

# Converting 2D array back to original 3D array and saving as glitched image
outputarr = np.reshape(outputarr, (img_height, img_width, pixel_tuple_len))

# Creating image with modified data
glitch_img = Image.fromarray(outputarr, img_mode)
glitch_img.save('glitched_{}'.format(img_filename))