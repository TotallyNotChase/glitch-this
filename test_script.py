import os, shutil
from random import randint
from time import time
from glitch_this import ImageGlitcher

def test_loop():
    # A method to stress test
    count = 0
    sum = 0
    try:
        with open('Collections/imglog.txt', 'w') as logtxt:
            while(1):
                t0 = time()
                level = randint(1, 10)
                """
                 Example of getting a glitched image and saving it,
                 with all default params

                 glitch_image() will return a PIL.Image.Image object
                 since gif is set to False

                 Check DOCS for more info!
                 https://github.com/TotallyNotChase/glitch-this/wiki
                """
                glitch_img = glitcher.glitch_image('test.png', level)
                # You can then save it or do anything else you want with it
                glitch_img.save('Collections/glitched_test_{}.png'.format(str(count)))
                t1 = time()
                logtxt.write('img_num: {}, level: {}\n'.format(count, level))
                count += 1
                sum += (t1 - t0)
                print('Time taken: ' + str(t1 - t0))
    except KeyboardInterrupt:
        print('Average time: ' + str(sum / count))

def test_image_to_image():
    """
     Example of getting a glitched Image and saving it

     We use glitch_level = 2 in this example
     You may change this to whatever you'd like
    """

    # All default params(i.e color_offset = False, scan_lines = False)
    glitch_img = glitcher.glitch_image('test.png', 2)
    glitch_img.save('Collections/glitched_test_default.png')

    # Now try with scan_lines set to true
    glitch_img = glitcher.glitch_image('test.png', 2, scan_lines=True)
    glitch_img.save('Collections/glitched_test_scan.png')

    # Now try with color_offset set to true
    glitch_img = glitcher.glitch_image('test.png', 2, color_offset=True)
    glitch_img.save('Collections/glitched_test_color.png')

    # How about all of them?
    glitch_img = glitcher.glitch_image('test.png', 2, color_offset=True, scan_lines=True)
    glitch_img.save('Collections/glitched_test_all.png')


def test_image_to_gif():
    """
     Example of getting a glitched GIF and saving it

     We use glitch_level = 2 in this example
     We also are making infinitely looping GIFs
     i.e loop = 0
     You may change these to whatever you'd like
    """

    DURATION = 200      # Set this to however many centiseconds each frame should be visible for

    # All default params (i.e FRAMES = 23, color_offset = False, scan_lines = False)
    glitch_imgs = glitcher.glitch_image('test.png', 2, gif=True)
    glitch_imgs[0].save('Collections/glitched_test_default.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=0)
    # Now try with scan_lines set to true
    glitch_imgs = glitcher.glitch_image('test.png', 2, gif=True, scan_lines=True)
    glitch_imgs[0].save('Collections/glitched_test_scan.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=0)

    # Now try with color_offset set to true
    glitch_imgs = glitcher.glitch_image('test.png', 2, gif=True, color_offset=True)
    glitch_imgs[0].save('Collections/glitched_test_color.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=0)

    # Now try with 10 frames
    glitch_imgs = glitcher.glitch_image('test.png', 2, gif=True, frames=10)
    glitch_imgs[0].save('Collections/glitched_test_frames.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=0)

    # How about all of the above?
    glitch_imgs = glitcher.glitch_image('test.png', 2, gif=True, scan_lines=True, color_offset=True, frames=10)
    glitch_imgs[0].save('Collections/glitched_test_all.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=0)

if __name__=='__main__':
    # Create the ImageGlitcher object
    glitcher = ImageGlitcher()
    if os.path.isdir('Collections'):
        shutil.rmtree('Collections')
    os.mkdir('Collections')
    print('Testing image to image glitching....')
    test_image_to_image()
    print('Done!')
    print('Testing image to GIF glitching....')
    test_image_to_gif()
    print('Done!')
    print('Testing infinite stress test.....\nNOTE: Use ctrl+c to stop the test')
    test_loop()
    print('Done!')
