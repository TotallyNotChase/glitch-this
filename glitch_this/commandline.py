#!/usr/bin/env python3
import os, argparse
from pathlib import Path
from time import time
from glitch_this import ImageGlitcher

def islatest(version):
    # Check pypi for the latest version number
    from urllib import request
    import json
    try:
        contents = request.urlopen('https://pypi.org/pypi/glitch-this/json').read()
    except:
        # Connection issue
        # Silenty return True, update check failed
        return True
    data = json.loads(contents)
    latest_version = data['info']['version']

    return version == latest_version

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
                           help='Include if you want a GIF instead of static image'
                           '\nNOTE: Does nothing if input image is GIF, i.e when using `-ig`')
    argparser.add_argument('-fr', '--frames', dest='frames', metavar='Frames', type=int, default=23,
                           help='How many frames to include in GIF, defaults to 23'
                           '\nNOTE: Does nothing if input image is GIF, i.e when using `-ig`')
    argparser.add_argument('-d', '--duration', dest='duration', metavar='Duration', type=int, default=200,
                           help='How long to display each frame (in centiseconds), defaults to 200')
    argparser.add_argument('-l', '--loop', dest='loop', metavar='Loop_Count', type=int, default=0,
                           help='How many times the glitched GIF should loop, defaults to 0 '
                           '(i.e infinite loop)')
    argparser.add_argument('-ig', '--inputgif', dest='input_gif', action='store_true',
                           help='If input image is GIF, use for glitching GIFs to GIFs! '
                           'Defaults to False\nNOTE: This is a slow process')
    argparser.add_argument('-f', '--force', dest='force', action='store_true',
                           help='If included, overwrites existing output file of same name (if found)'
                           '\nDefaults to False')
    argparser.add_argument('-o', '--outfile', dest='outfile', metavar='Outfile_path', type=str,
                           help='Explictly supply the full or relative `path/filename`\
                           \nDefaults to ./glitched_src_image_path')
    args = argparser.parse_args()

    # Sanity check inputs
    if not args.duration > 0:
        raise ValueError('Duration must be greater than 0')
    if not args.loop >= 0:
        raise ValueError('Loop must be greater than or equal to 0')
    if not args.frames > 0:
        raise ValueError('Frames must be greater than 0')
    if not os.path.isfile(args.src_img_path):
        raise FileNotFoundError('No image found at given path')

    # Set up full_path, for output saving location
    out_path, out_file = os.path.split(Path(args.src_img_path))
    out_filename, out_fileex = out_file.rsplit('.', 1)
    out_filename = 'glitched_' + out_filename
    # Output file extension should be '.gif' if output file is going to be a gif
    out_fileex = 'gif' if args.gif else out_fileex
    if args.outfile:
        # If output file path is already given
        # Overwrite the previous values
        out_path, out_file = os.path.split(Path(args.outfile))
        if out_path != '' and not os.path.exists(out_path):
            raise Exception('Given outfile path, ' + out_path + ', does not exist')
        # The extension in user provided outfile path is ignored
        out_filename = out_file.rsplit('.', 1)[0]
    # Now create the full path
    full_path = os.path.join(out_path, '{}.{}'.format(out_filename, out_fileex))
    if os.path.exists(full_path) and not args.force:
        raise Exception(full_path + ' already exists\nCannot overwrite '
        'existing file unless -f or --force is included\nProgram Aborted')

    # Actual work begins here
    glitcher = ImageGlitcher()
    t0 = time()
    if not args.input_gif:
        # Get glitched image or GIF (from image)
        glitch_img = glitcher.glitch_image(args.src_img_path, args.glitch_level,
                                           scan_lines=args.scan_lines,
                                           color_offset=args.color,
                                           gif=args.gif,
                                           frames=args.frames)
    else:
        # Get glitched image or GIF (from GIF)
        glitch_img, src_duration, args.frames = glitcher.glitch_gif(args.src_img_path, args.glitch_level,
                                                                     scan_lines=args.scan_lines,
                                                                     color_offset=args.color)
        args.gif = True     # Set args.gif to true if it isn't already in this case
    t1 = time()
    # End of glitching
    t2 = time()
    # Save the image
    if not args.gif:
        glitch_img.save(full_path, compress_level=3)
        t3 = time()
        print('Glitched Image saved in "{}"'.format(full_path))
    else:
        glitch_img[0].save(full_path,
                    format='GIF',
                    append_images=glitch_img[1:],
                    save_all=True,
                    duration=args.duration,
                    loop=args.loop,
                    compress_level=3)
        t3 = time()
        print('Glitched GIF saved in "{}"\nFrames = {}, Duration = {}, Loop = {}'.format(full_path, args.frames, args.duration, args.loop))
    print('Time taken to glitch: ' + str(t1 - t0))
    print('Time taken to save: ' + str(t3 - t2))
    print('Total Time taken: ' + str(t3 - t0))

    # Let the user know if new version is available
    if not islatest(ImageGlitcher.__version__):
        print('A new version of "glitch-this" is available. Please consider upgrading via `pip install --upgrade glitch-this`')

if __name__=='__main__':
    main()
