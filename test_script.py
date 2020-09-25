import os
import shutil
from decimal import getcontext, Decimal
from random import choice
from time import time

from PIL import Image

from glitch_this import ImageGlitcher

"""
Tester Script for the glitch_this library (not script)

This provides practical examples and tutorials of the
library commands as well

For an in-depth tutorial please refer to docs: https://github.com/TotallyNotChase/glitch-this/wiki
"""

# Set up glitch_amount values that will be used
# Float numbers from 1 to 10, upto a single decimal precision

# Setting floating point precision to 1 (after decimal point)
getcontext().prec = 2
amount_list = []
start = Decimal(0.1)
for i in range(100):
    amount_list.append(float(start))
    start += Decimal(0.1)


def test_loop():
    # A method to stress test
    count = 0
    timesum = 0
    try:
        with open('Collections/imglog.txt', 'w') as logtxt:
            while(1):
                t0 = time()
                level = choice(amount_list)
                """
                 Example of getting a glitched image and saving it,
                 with all default params

                 glitch_image() will return a PIL.Image.Image object
                 since gif is set to False

                 Check DOCS for more info!
                """
                glitch_img = glitcher.glitch_image(f'test.{fmt}', level)
                # You can then save it or do anything else you want with it
                glitch_img.save(f'Collections/glitched_test_{count}.{fmt}')
                t1 = time()
                logtxt.write(f'img_num: {count}, level: {level}\n')
                count += 1
                timesum += (t1 - t0)
                print(f'Time taken: {t1 - t0}')
    except KeyboardInterrupt:
        print(f'Average time: {timesum / count}')


def test_image_to_image():
    """
     Example of getting a glitched Image and saving it

     We use glitch_level = 2 in this example
     You may change this to whatever you'd like
    """

    # All default params(i.e color_offset = False, scan_lines = False)
    glitch_img = glitcher.glitch_image(f'test.{fmt}', 2)
    glitch_img.save(f'Collections/glitched_test_default.{fmt}')

    # Now try with scan_lines set to true
    glitch_img = glitcher.glitch_image(f'test.{fmt}', 2, scan_lines=True)
    glitch_img.save(f'Collections/glitched_test_scan.{fmt}')

    # Now try with color_offset set to true
    glitch_img = glitcher.glitch_image(f'test.{fmt}', 2, color_offset=True)
    glitch_img.save(f'Collections/glitched_test_color.{fmt}')

    # Now try glitching with a seed
    # This will base the RNG used within the glitching on given seed
    glitch_img = glitcher.glitch_image(f'test.{fmt}', 2, seed=42)
    glitch_img.save(f'Collections/glitched_test_seed.{fmt}')

    # How about all of them?
    glitch_img = glitcher.glitch_image(f'test.{fmt}', 2, color_offset=True, scan_lines=True, seed=42)
    glitch_img.save(f'Collections/glitched_test_all.{fmt}')

    # You can also pass an Image object inplace of the path
    # Applicable in all of the examples above
    img = Image.open(f'test.{fmt}')
    glitch_img = glitcher.glitch_image(img, 2, color_offset=True, scan_lines=True, seed=42)
    glitch_img.save(f'Collections/glitched_test_all_obj.{fmt}')


def test_image_to_gif():
    """
     Example of getting a glitched GIF and saving it

     We use glitch_level = 2 in this example
     Please note you can use any number in between 1 and 10
     Including floats, floats with one or two decimal precision
     will work the best

     We also are making infinitely looping GIFs
     i.e loop = 0
     You may change these to whatever you'd like
    """

    DURATION = 200      # Set this to however many centiseconds each frame should be visible for
    LOOP = 0            # Set this to how many times the gif should loop
    # LOOP = 0 means infinite loop

    # All default params (i.e step = 1, glitch_change = 0, cycle = False, Frames = 23, color_offset = False, scan_lines = False)
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, gif=True)
    glitch_imgs[0].save('Collections/glitched_test_default.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with scan_lines set to true
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, gif=True, scan_lines=True)
    glitch_imgs[0].save('Collections/glitched_test_scan.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with color_offset set to true
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, gif=True, color_offset=True)
    glitch_imgs[0].save('Collections/glitched_test_color.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with 10 frames
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, gif=True, frames=10)
    glitch_imgs[0].save('Collections/glitched_test_frames.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by 1 every time, with cycle set to False
    # glitch_amount will reach glitch_max after (glitch_max - glitch_amount)/glitch_change glitches
    # in this case that's 8
    # It'll just stay at glitch_max for the remaining duration since cycle = False
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, glitch_change=1, gif=True)
    glitch_imgs[0].save('Collections/glitched_test_increment.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by 1 every time, with cycle set to True
    # glitch_amount will reach glitch_max after (glitch_max - glitch_amount)/glitch_change glitches
    # in this case that's 8
    # It'll cycle back to glitch_min after that and keep incrementing by glitch_change again
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, glitch_change=1, cycle=True, gif=True)
    glitch_imgs[0].save('Collections/glitched_test_increment_cycle.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by -1 every time, with cycle set to True
    # glitch_amount will reach glitch_min after (glitch_min - glitch_amount)/glitch_change glitches
    # in this case that's 1
    # It'll cycle back to glitch_max after that and keep incrementing (actually decrementing, in this case)
    # by glitch_change again
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, glitch_change=-1, cycle=True, gif=True)
    glitch_imgs[0].save('Collections/glitched_test_decrement_cycle.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with glitching only every 2nd frame
    # There will still be the specified number of frames (23 in this case)
    # But only every 2nd of the frames will be glitched
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, step=2, gif=True)
    glitch_imgs[0].save('Collections/glitched_test_step.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # How about all of the above?
    glitch_imgs = glitcher.glitch_image(f'test.{fmt}', 2, glitch_change=-1,
                                        cycle=True, gif=True, scan_lines=True, color_offset=True, frames=10, step=2)
    glitch_imgs[0].save('Collections/glitched_test_all.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # You can also pass an Image object inplace of the path
    # Applicable in all of the examples above
    img = Image.open(f'test.{fmt}')
    glitch_imgs = glitcher.glitch_image(img, 2, glitch_change=-1,
                                        cycle=True, gif=True, scan_lines=True, color_offset=True, frames=10, step=2)
    glitch_imgs[0].save('Collections/glitched_test_all_obj.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)


def test_gif_to_gif():
    """
     Example of getting a glitched GIF (from another GIF)
     and saving it

     `glitch_gif` also returns the duration (of each frame)
     in centiseconds and the number of frames in the given GIF, you may
     use these when saving your GIF too!

     We use glitch_level = 2 in this example
     We also are making infinitely looping GIFs
     i.e loop = 0
     You may change these to whatever you'd like
    """

    DURATION = 200      # Set this to however many centiseconds each frame should be visible for
    LOOP = 0            # Set this to how many times the gif should loop
    # LOOP = 0 means infinite loop

    # All default params (i.e step = 1, glitch_change = 0, cycle = False, color_offset = False, scan_lines = False)
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2)
    glitch_imgs[0].save('Collections/glitched_gif_default.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)
    # Now try with scan_lines set to true
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2, scan_lines=True)
    glitch_imgs[0].save('Collections/glitched_gif_scan.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with color_offset set to true
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2, color_offset=True)
    glitch_imgs[0].save('Collections/glitched_gif_color.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by 1 every time, with cycle set to False
    # glitch_amount will reach glitch_max after (glitch_max - glitch_amount)/glitch_change glitches
    # in this case that's 8
    # It'll just stay at glitch_max for the remaining duration since cycle = False
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2, glitch_change=1)
    glitch_imgs[0].save('Collections/glitched_gif_increment.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by 1 every time, with cycle set to True
    # glitch_amount will reach glitch_max after (glitch_max - glitch_amount)/glitch_change glitches
    # in this case that's 8
    # It'll cycle back to glitch_min after that and keep incrementing by glitch_change again
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2, glitch_change=1, cycle=True)
    glitch_imgs[0].save('Collections/glitched_gif_increment_cycle.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by -1 every time, with cycle set to True
    # glitch_amount will reach glitch_min after (glitch_min - glitch_amount)/glitch_change glitches
    # in this case that's 1
    # It'll cycle back to glitch_max after that and keep incrementing (actually decrementing, in this case)
    # by glitch_change again
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2, glitch_change=-1, cycle=True)
    glitch_imgs[0].save('Collections/glitched_gif_decrement_cycle.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with glitching only every 2nd frame
    # There will still be the same number of frames as in the source gif
    # But only every 2nd of the frames will be glitched
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2, step=2)
    glitch_imgs[0].save('Collections/glitched_gif_step.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try glitching with a seed
    # This will base the RNG used within the glitching on given seed
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif('test.gif', 2, seed=42)
    glitch_imgs[0].save('Collections/glitched_gif_seed.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # How about all of the above?
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif(
        'test.gif', 2, glitch_change=-1, cycle=True, scan_lines=True, color_offset=True, step=2, seed=42)
    glitch_imgs[0].save('Collections/glitched_gif_all.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # You can also pass an Image object inplace of the path
    # Applicable in all of the examples above
    img = Image.open('test.gif')
    glitch_imgs, src_duration, src_frames = glitcher.glitch_gif(
        img, 2, glitch_change=-1, cycle=True, scan_lines=True, color_offset=True, step=2, seed=42)
    glitch_imgs[0].save('Collections/glitched_test_all_obj.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)


if __name__ == '__main__':
    # Create the ImageGlitcher object
    glitcher = ImageGlitcher()
    if os.path.isdir('Collections'):
        shutil.rmtree('Collections')
    os.mkdir('Collections')

    # Start Testing
    # Set format of test image to png (file being used is test.png)
    fmt = 'png'

    print('Testing GIF to GIF glitching....')
    t0 = time()
    test_gif_to_gif()
    t1 = time()
    print(f'Done! Time taken: {t1 - t0}')

    print('Testing image to image glitching....')
    t0 = time()
    test_image_to_image()
    t1 = time()
    print(f'Done! Time taken: {t1 - t0}')

    print('Testing image to GIF glitching....')
    t0 = time()
    test_image_to_gif()
    t1 = time()
    print(f'Done! Time taken: {t1 - t0}')

    print('Testing infinite stress test.....\nNOTE: Use ctrl+c to stop the test')
    test_loop()
    print('Done!')
