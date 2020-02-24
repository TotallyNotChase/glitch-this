#!/usr/bin/env python3
import os, argparse
from pathlib import Path
from time import time
from glitch_this import ImageGlitcher
from check_version import is_uptodate

def glitch_script(src_img_path, glitch_level, scan_lines, color, gif, frames, duration):
    t0 = time()
    # Fetching image attributes
    img_path, img_file = os.path.split(Path(src_img_path))
    img_filename, img_fileex = img_file.rsplit('.', 1)

    # Glitching begins here
    glitcher = ImageGlitcher()
    glitch_img = glitcher.glitch_image(src_img_path, glitch_level, scan_lines=scan_lines, color_offset=color, gif=gif)
    if not gif:
        full_path = os.path.join(img_path, 'glitched_' + img_file)
        glitch_img.save(full_path)
        t1 = time()
        print('Glitched image saved in "{}"'.format(full_path))
        print('Time taken: ' + str(t1 - t0))
    else:
        full_path = os.path.join(img_path, 'glitched_{}.gif'.format(img_filename))
        glitch_img[0].save(full_path,
                              format='GIF',
                              append_images=glitch_img[1:],
                              save_all=True,
                              duration=duration,
                              loop=0)
        t1 = time()
        print('Glitched GIF saved in "{}"\nFrames = {}, Duration = {}'.format(full_path, frames, duration))
        print('Time taken: ' + str(t1 - t0))

def main():
    # Add commandline arguments parser
    argparser = argparse.ArgumentParser(description='Glitchify images to static images and GIFs!')
    argparser.add_argument('src_img_path', metavar='Image_Path', type=str,
                           help='Relative or Absolute string path to source image')
    argparser.add_argument('glitch_level', metavar='Glitch_Level', type=int,
                           help='Integer between 1 and 10, inclusive, representing amount of glitchiness')
    argparser.add_argument('-c', '--color', dest='color', action='store_true',
                           help='Whether or not to add color offset, defaults to False')
    argparser.add_argument('-s', '--scan', dest='scan_lines', action='store_true',
                           help='Whether or not to add scan lines effect, defaults to False')
    argparser.add_argument('-g', '--gif', dest='gif', action='store_true',
                           help='Include if you want a GIF instead of static image')
    argparser.add_argument('-f', '--frames', dest='frames', type=int, default=23,
                           help='How many frames to include in GIF, defaults to 23')
    argparser.add_argument('-d', '--duration', dest='duration', type=int, default=200,
                           help='How long to display each frame (in centiseconds), defaults to 200')
    args = argparser.parse_args()

    # Sanity checking the inputs
    if not 1 <= args.glitch_level <= 10:
        raise ValueError('glitch_amount parameter must be in range 1 to 10, inclusive')
    if not os.path.exists(args.src_img_path):
        raise FileNotFoundError('No image found at given path')
    if not args.frames > 1:
        raise ValueError('Frames must be greather than 1')
    if not args.duration > 0:
        raise ValueError('Duration must be greather than 0')

    # Call the actual script
    glitch_script(args.src_img_path, args.glitch_level, args.scan_lines, args.color, args.gif, args.frames, args.duration)

    # Let the user know if new version is available
    if not is_uptodate(ImageGlitcher.__version__):
        print('A new version of "glitch-this" is available. Please consider upgrading via `pip install --upgrade glitch-this`')

if __name__=='__main__':
    main()
