#!/usr/bin/env python3
import argparse
import os
from datetime import datetime
from pathlib import Path
from time import time
from typing import Dict

from glitch_this import ImageGlitcher
from glitch_this.exceptions import OutFileNotFoundException, CanNotOverwriteUntilForceIsProvided


def read_version() -> str:
    with open(version_filepath, 'r') as version_file:
        content = version_file.read()
    return content.strip()


def write_version(version: str):
    with open(version_filepath, 'w') as version_file:
        version_file.write(version + '\n')


def is_expired(filepath: str) -> bool:
    # Check if the file has been created 2 weeks prior
    file_creation = datetime.fromtimestamp(os.stat(filepath).st_mtime)
    now = datetime.now()
    return (now - file_creation).days > 14


def is_latest(version: str) -> bool:
    # Check pypi for the latest version number
    from urllib import request
    import json
    if os.path.isfile(version_filepath) and not is_expired(version_filepath):
        # If a version log already exists, and it's not more than 14 days old
        latest_version = read_version()
    else:
        # Either version log does not exist or is outdated
        try:
            contents = request.urlopen(
                'https://pypi.org/pypi/glitch-this/json').read()
        except Exception:
            # Connection issue
            # Silent return True, update check failed
            return True
        data = json.loads(contents)
        latest_version = data['info']['version']
        write_version(latest_version)

    print(f'Current version: {version} | Latest version: {latest_version}')
    return version == latest_version


def get_help(glitch_min: float, glitch_max: float) -> Dict:
    return {
        'path': 'Relative or Absolute string path to source image',
        'level': f'Number between {glitch_min} and {glitch_max}, inclusive, representing amount of glitchiness',
        'color': 'Include if you want to add color offset',
        'scan': 'Include if you want to add scan lines effect\nDefaults to False',
        'seed': 'Set a random seed for generating similar images across runs',
        'gif': 'Include if you want output to be a GIF',
        'frames': 'Number of frames to include in output GIF, default - 23',
        'step': "Glitch every step'th frame of output GIF, default - 1 (every frame)",
        'increment': 'Increment glitch_amount by given value after glitching every frame of output GIF',
        'cycle': f'Include if glitch_amount should be cycled back to {glitch_min} or {glitch_max} if it over/underflows',
        'duration': 'How long to display each frame (in centiseconds), default - 200',
        'relative_duration': "Multiply given value to input GIF's original duration and use that as duration",
        'loop': 'How many times the glitched GIF should loop, default - 0 (infinite loop)',
        'inputgif': 'Include if input image is GIF',
        'force': 'Forcefully overwrite output file',
        'out': 'Explicitly supply full/relative path to output file'
    }


def main():
    glitch_min, glitch_max = 0.1, 10.0
    current_version = ImageGlitcher.__version__
    help_text = get_help(glitch_min, glitch_max)
    args = _add_cli_arguments(current_version, help_text)
    _validate_cli_arguments(args)

    full_path = _handle_out_path_and_out_file(args)

    # Actual work begins here
    glitcher = ImageGlitcher()
    global version_filepath
    version_filepath = os.path.join(glitcher.lib_path, 'version.info')
    t0 = time()
    if not args.input_gif:
        # Get glitched image or GIF (from image)
        glitch_img = glitcher.glitch_image(args.src_img_path, args.glitch_level,
                                           glitch_change=args.increment,
                                           cycle=args.cycle,
                                           scan_lines=args.scan_lines,
                                           color_offset=args.color,
                                           seed=args.seed,
                                           gif=args.gif,
                                           frames=args.frames,
                                           step=args.step)
    else:
        # Get glitched image or GIF (from GIF)
        glitch_img, src_duration, args.frames = glitcher.glitch_gif(args.src_img_path, args.glitch_level,
                                                                    glitch_change=args.increment,
                                                                    cycle=args.cycle,
                                                                    scan_lines=args.scan_lines,
                                                                    color_offset=args.color,
                                                                    seed=args.seed,
                                                                    step=args.step)
        # Set args.gif to true if it isn't already in this case
        args.gif = True
        # Set args.duration to src_duration * relative duration, if one was given
        args.duration = int(args.rel_duration * src_duration) if args.rel_duration else args.duration

    t1 = time()
    # End of glitching
    t2 = time()
    # Save the image
    if not args.gif:
        glitch_img.save(full_path, compress_level=3)
        t3 = time()
        print(f'Glitched Image saved in "{full_path}"')
    else:
        glitch_img[0].save(full_path,
                           format='GIF',
                           append_images=glitch_img[1:],
                           save_all=True,
                           duration=args.duration,
                           loop=args.loop,
                           compress_level=3)
        t3 = time()
        print(
            f'Glitched GIF saved in "{full_path}"\nFrames = {args.frames}, Duration = {args.duration}, Loop = {args.loop}')
    print(f'Time taken to glitch: {t1 - t0}')
    print(f'Time taken to save: {t3 - t2}')
    print(f'Total Time taken: {t3 - t0}')

    _inform_about_new_version(current_version)


def _inform_about_new_version(current_version):
    # Let the user know if new version is available
    if not is_latest(current_version):
        print(
            'A new version of "glitch-this" is available. Please consider upgrading via '
            '`pip3 install --upgrade glitch-this`')


def _handle_out_path_and_out_file(args):
    # Set up full_path, for output saving location
    out_path, out_file = os.path.split(Path(args.src_img_path))
    out_filename, out_file_extension = out_file.rsplit('.', 1)
    out_filename = f'glitched_{out_filename}'
    # Output file extension should be '.gif' if output file is going to be a gif
    out_file_extension = 'gif' if args.gif else out_file_extension
    if args.outfile:
        # If output file path is already given
        # Overwrite the previous values
        out_path, out_file = os.path.split(Path(args.outfile))
        if out_path != '' and not os.path.exists(out_path):
            raise OutFileNotFoundException(f'Given outfile path, {out_path}, does not exist')
        # The extension in user provided outfile path is ignored
        out_filename = out_file.rsplit('.', 1)[0]
    # Now create the full path
    full_path = os.path.join(out_path, f'{out_filename}.{out_file_extension}')
    if os.path.exists(full_path) and not args.force:
        raise CanNotOverwriteUntilForceIsProvided(f'{full_path} already exists\nCannot overwrite '
                                                  f'existing file unless -f or --force is included\nProgram Aborted')
    return full_path


def _validate_cli_arguments(args):
    # Sanity check inputs
    if args.duration <= 0:
        raise ValueError('Duration must be greater than 0')
    if args.loop < 0:
        raise ValueError('Loop must be greater than or equal to 0')
    if args.frames <= 0:
        raise ValueError('Frames must be greater than 0')
    if not os.path.isfile(args.src_img_path):
        raise FileNotFoundError('No image found at given path')


def _add_cli_arguments(current_version, help_text):
    # Add commandline arguments parser
    argparser = argparse.ArgumentParser(
        description='glitch_this: Glitchify images and GIFs, with highly customizable options!\n\n'
                    '* Website: https://github.com/TotallyNotChase/glitch-this \n'
                    f'* Version: {current_version}\n'
                    '* Changelog: https://github.com/TotallyNotChase/glitch-this/blob/master/CHANGELOG.md',
        formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument('--version', action='version',
                           version=f'glitch_this {current_version}')
    argparser.add_argument('src_img_path', metavar='Image_Path', type=str,
                           help=help_text['path'])
    argparser.add_argument('glitch_level', metavar='Glitch_Level', type=float,
                           help=help_text['level'])
    argparser.add_argument('-c', '--color', dest='color', action='store_true',
                           help=help_text['color'])
    argparser.add_argument('-s', '--scan', dest='scan_lines', action='store_true',
                           help=help_text['scan'])
    argparser.add_argument('-g', '--gif', dest='gif', action='store_true',
                           help=help_text['gif'])
    argparser.add_argument('-ig', '--inputgif', dest='input_gif', action='store_true',
                           help=help_text['inputgif'])
    argparser.add_argument('-f', '--force', dest='force', action='store_true',
                           help=help_text['force'])
    argparser.add_argument('-sd', '--seed', dest='seed', metavar='Seed', type=float, default=None,
                           help=help_text['seed'])
    argparser.add_argument('-fr', '--frames', dest='frames', metavar='Frames', type=int, default=23,
                           help=help_text['frames'])
    argparser.add_argument('-st', '--step', dest='step', metavar='Step', type=int, default=1,
                           help=help_text['step'])
    argparser.add_argument('-i', '--increment', dest='increment', metavar='Increment', type=float, default=0.0,
                           help=help_text['increment'])
    argparser.add_argument('-cy', '--cycle', dest='cycle', action='store_true',
                           help=help_text['cycle'])
    argparser.add_argument('-d', '--duration', dest='duration', metavar='Duration', type=int, default=200,
                           help=help_text['duration'])
    argparser.add_argument('-rd', '--relative_duration', dest='rel_duration', metavar='Relative_Duration', type=float,
                           help=help_text['relative_duration'])
    argparser.add_argument('-l', '--loop', dest='loop', metavar='Loop_Count', type=int, default=0,
                           help=help_text['loop'])
    argparser.add_argument('-o', '--outfile', dest='outfile', metavar='Outfile_path', type=str,
                           help=help_text['out'])
    return argparser.parse_args()


if __name__ == '__main__':
    main()
