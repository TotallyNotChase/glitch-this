<h1 align="center">glitch-this!</h1>
<p align="center"><i>Create glitched images and GIFs, with highly customizable options!</i></p>
<hr><p align="center">
  <a href="https://pypi.org/project/glitch-this"><img alt="Pypi release" src="https://img.shields.io/pypi/v/glitch-this?color=red&label=pypi%20release&logo=pypi&logoColor=blue" /></a>
  <img alt="Stars" src="https://img.shields.io/github/stars/TotallyNotChase/glitch-this.svg?label=Stars&style=flat" />
  <a href="https://pepy.tech/project/glitch-this"><img alt="Pypi downloads" src="https://pepy.tech/badge/glitch-this" /></a>
  <a href="http://www.python.org/download/"><img alt="Python 3" src="https://img.shields.io/badge/Python-3-yellow.svg"></a>
  <a href="https://github.com/TotallyNotChase/glitch-this/blob/master/LICENSE"><img src="https://img.shields.io/github/license/TotallyNotChase/glitch-this.svg" alt="License"/></a>
</p>

A commandline tool + `python` library to glitchify images and **even make GIFs** out of them!
Featuring *100 gradually different levels of glitching intensity*! The algorithm used to create glitched images is a slightly modifed version of the popular [ImageGlitcher](https://www.airtightinteractive.com/demos/js/imageglitcher/) tool's algorithm, so you can expect the glitched images to look really cool!

**NOW WITH GIF TO GLITCHED GIF SUPPORT! Check out the [docs](https://github.com/TotallyNotChase/glitch-this/wiki/Home)!**

If you like using this tool, please consider **starring on Github**!

![demo](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched2.gif)

What are you waiting for? Import the library and get glitching!

**NOTE** : Works best with RGB/RGBA images

Checkout a web demo right [here](https://github.com/pahefu/web-glitch-this), courtesy of @[pahefu](https://github.com/pahefu)

## What others have to say ~
* [#1 hot in r/python](https://www.reddit.com/r/Python/comments/f7taiy/my_python_imagegif_glitching_library_is_now_on/)
* [#1 hot in r/programming](https://www.reddit.com/r/programming/comments/f7q2q3/i_made_a_commandline_script_to_make_glitched/)
* [#1 hot in r/broken_gifs](https://www.reddit.com/r/brokengifs/comments/f7pyqw/i_made_a_commandline_script_to_make_glitched_gifs/)
* [#1 hot in r/glitch_art](https://www.reddit.com/r/glitch_art/comments/f7q0hc/i_made_a_script_to_make_glitched_images_and_gifs/)
* [#4 product of the day in producthunt](https://www.producthunt.com/posts/glitch-this)

<a href="https://www.producthunt.com/posts/glitch-this?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-glitch-this" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=186201&theme=light" alt="glitch-this - Create highly customizable glitched images and GIFs! | Product Hunt Embed" style="width: 250px; height: 54px;" width="250" height="54" /></a>

## FEATURES!
* Choose any **glitching intensity** between 0.1 and 10.0, yes those are floats!

  *Each level is gradually different*!

  Want just a tiny bit of glitching, enough to make your image look cool? - use level 2 (my favorite)!
* Add **scan lines** for a retro CRT effect! Add **color offset** for even cooler glitching!
* Create **Glitched GIFs** from a normal image!

  That's right, before this tool, I had to manually download each image from [ImageGlitcher](https://www.airtightinteractive.com/demos/js/imageglitcher/), save them, and then head to a GIF creation website.

  Now you can do it *all* at once!
* Glitch normal **GIFs** into **glitched GIFs**!
* Customize **step** of glitching, you can glitch *every step'th frame* instead of all frames!
* **Increment/Decrement glitching intensity** while glitching every frame!

  So you can have a frame *glitched with intensity 2*, but the *next can be 5*, the *next to that can be 8* and so on!

* Customize the **number of frames** in a GIF as well as their **duration** - all from the comfort of your terminal!
* Set how many times the GIF should **loop**!
* Set your own custom **seed** for a predictable RNG!

## Changelog
View the changelog [here](https://github.com/TotallyNotChase/glitch-this/blob/master/CHANGELOG.md)

## Requirements
* `python 3`
* `pillow`
* `numpy`

These will be automatically installed when you install the library! (assuming you have `python3`)
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

![quick_basic](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/basic_command.gif)

Try `glitch_this -h` for more info! Directly from your commandline!

Or, Check out the [script docs](https://github.com/TotallyNotChase/glitch-this/wiki/Documentation:-The-commandline-script)!

Interested in the library? Check out the [library docs](https://github.com/TotallyNotChase/glitch-this/wiki/Documentation:-The-glitch-this-library)!

## DOCS! WHERE TO?!

Read the [script docs](https://github.com/TotallyNotChase/glitch-this/wiki/Documentation:-The-commandline-script)!

Read the [library docs](https://github.com/TotallyNotChase/glitch-this/wiki/Documentation:-The-glitch-this-library)!

Check out a [full example](https://github.com/TotallyNotChase/glitch-this/blob/master/test_script.py) using the library!

## Whoa! Cool Glitches
Here's some glitched images generated from this script - of different intensity levels!

**NOTE**: All these images had `-c` parameter included, for color offset

#### Original image for reference:-

![og_img](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/source.png)

#### Glitched version - Level 2:-

![glitched_2](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched2.png)

*Not badly glitched now is it?*

#### Glitched version - Level 5:-

![glitched_5](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched5.png)

*Well it's certainly starting to get glitchy*

#### Glitched version - Level 8:-

![glitched_8](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched8.png)

*I don't know what I'm looking at*

Let's get some **scan lines** on there!

#### Glitched version (scan_lines)- Level 2:-

![glitched_2_scan](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched2scan.png)

#### Glitched version (scan_lines) - Level 5:-

![glitched_5_scan](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched5scan.png)

#### Glitched version (scan_lines) - Level 8:-

![glitched_8_scan](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched8scan.png)

That's neat, but how about some GIFs? Here's some GIFs from the same image:-

*Note: All the GIFs use default values from `FRAMES` and `DURATION`, i.e 23 and 200 respectively*

#### Glitched GIF - Level 2:-

![glitched_gif2](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched2.gif)

#### Glitched GIF - Level 5:-

![glitched_gif5](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched5.gif)

#### Glitched GIF - Level 8:-

![glitched_gif8](https://raw.githubusercontent.com/TotallyNotChase/glitch-this/master/example/glitched8.gif)
