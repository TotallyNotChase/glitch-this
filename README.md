## Glitch This!
A commandline tool + `python` library to glitchify images and **even make GIFs** out of them!
Featuring *10 different levels of glitching intensity*! The algorithm used to create glitched images is a slightly modifed version of the popular [ImageGlitcher](https://www.airtightinteractive.com/demos/js/imageglitcher/) tool's algorithm, so you can expect the glitched images to look really cool!

**NOW EASIER THAN EVER TO USE!**

If you like using this tool, please consider **starring on Github**!

![demo](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched2.gif)

What are you waiting for? Import the library and get glitching!

**NOTE** : Works best with RGB/RGBA images

## What others have to say ~
* [#1 hot in r/python](https://www.reddit.com/r/Python/comments/f7taiy/my_python_imagegif_glitching_library_is_now_on/)
* [#1 hot in r/programming](https://www.reddit.com/r/programming/comments/f7q2q3/i_made_a_commandline_script_to_make_glitched/)
* [#1 hot in r/broken_gifs](https://www.reddit.com/r/brokengifs/comments/f7pyqw/i_made_a_commandline_script_to_make_glitched_gifs/)
* [#1 hot in r/glitch_art](https://www.reddit.com/r/glitch_art/comments/f7q0hc/i_made_a_script_to_make_glitched_images_and_gifs/)

## Changelog
View the changelog [here](https://github.com/TotallyNotChase/glitch-this/blob/master/CHANGELOG.md)

## FEATURES!
* Choose from *10 gradually different levels* of **glitching intensity**!
  Want just a tiny bit of glitching, enough to make your image look cool? - use level 2 (my favorite)!
* Create **Glitched GIFs** from a normal image!
  That's right, before this tool, I had to manually download each image from [ImageGlitcher](https://www.airtightinteractive.com/demos/js/imageglitcher/), save them, and then head to a GIF creation website.
  Now you can do it *all* at once!
* Customize the **number of frames** in a GIF as well as their **duration** - all from the comfort of your terminal!
* Add **scan lines** for a retro CRT effect!
* Oh and did I mention, **color offset**? Just like [ImageGlitcher](https://www.airtightinteractive.com/demos/js/imageglitcher/), this tool *glitches the color channels* as well as the pixels - for **very convincing** looking glitched images!

## Requirements
* `python 3`
* `pillow`
* `numpy`

You can install the required packages all at once through the included `requirements.txt`
## Installation

Simply install `glitch-this` from [pypi](https://pypi.org/project/glitch-this/)!

```
pip install glitch-this
```

(OR)

```
pip3 install glitch-this
```

## Quick Start

Now that you have the library installed, all you need to do is invoke the script and pass in the params

`glitch_this [IMAGE PATH] [GLITCH_LEVEL]`

[!quick_basic](https://github.com/TotallyNotChase/glitch-this/blob/master/example/basic_usage.gif)

Try `glitch_this -h` for more info! Directly from your commandline!

Or, Check out the [docs](https://github.com/TotallyNotChase/glitch-this/wiki/Documentation/)!

## DOCS! WHERE TO?!

Read the [docs](https://github.com/TotallyNotChase/glitch-this/wiki/Documentation/)!

## Whoa! Cool Glitches
Here's some glitched images generated from this script - of different intensity levels!

**NOTE**: All these images had `-c` parameter included, for color offset

#### Original image for reference:-

![og_img](https://github.com/TotallyNotChase/glitch-this/blob/master/example/source.png)

#### Glitched version - Level 2:-

![glitched_2](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched2.png)

*Not badly glitched now is it?*

#### Glitched version - Level 5:-

![glitched_5](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched5.png)

*Well it's certainly starting to get glitchy*

#### Glitched version - Level 8:-

![glitched_8](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched8.png)

*I don't know what I'm looking at*

Let's get some **scan lines** on there!

#### Glitched version (scan_lines)- Level 2:-

![glitched_2_scan](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched2scan.png)

#### Glitched version (scan_lines) - Level 5:-

![glitched_5_scan](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched5scan.png)

#### Glitched version (scan_lines) - Level 8:-

![glitched_8_scan](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched8scan.png)

That's neat, but how about some GIFs? Here's some GIFs from the same image:-

*Note: All the GIFs use default values from `FRAMES` and `DURATION`, i.e 23 and 200 respectively*

#### Glitched GIF - Level 2:-

![glitched_gif2](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched2.gif)

#### Glitched GIF - Level 5:-

![glitched_gif5](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched5.gif)

#### Glitched GIF - Level 8:-

![glitched_gif8](https://github.com/TotallyNotChase/glitch-this/blob/master/example/glitched8.gif)
