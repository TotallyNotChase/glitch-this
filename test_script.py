import os, shutil
from random import randint
from time import time
from glitch_this import ImageGlitcher

if __name__=='__main__':
    # Create the ImageGlitcher object
    # You don't have to do this, you can also call ImageGlitcher.glitch_image()
    glitcher = ImageGlitcher()
    count = 0
    sum = 0
    try:
        if os.path.isdir('Collections'):
            shutil.rmtree('Collections')
        os.mkdir('Collections')
        logtxt = open('Collections/imglog.txt', 'w')
        while(1):
            t0 = time()
            level = randint(1, 10)
            # glitch_image() will return a PIL.Image.Image object
            # Make sure to supply the full/relative path to the image as well as glitch level
            glitch_img = glitcher.glitch_image('test.png', level)
            # You can then save it or do anything else you want with it
            glitch_img.save('Collections/glitched_test_{}.png'.format(str(count)))
            t1 = time()
            logtxt.write('img_num: {}, level: {}\n'.format(count, level))
            count += 1
            sum += (t1 - t0)
            print('Time taken: ' + str(t1 - t0))
    except KeyboardInterrupt:
        logtxt.close()
        print('Average time: ' + str(sum / count))
