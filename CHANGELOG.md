## Version History
* 0.0.1 -> Base setup
* 0.0.2 -> Make `color_offset` optional, you can set it to `True` when calling `glitch_image()` or, if you're using the script, include the param `-c`.
* 0.0.3 -> Fix not being able to use image names with dots in them

  *Thanks to @ojensen5115*
* 0.0.4 -> Add detailed exceptions

  *Thanks to @amancevice*
* 0.0.5 -> Change `==` to `is`

  *Thanks to @amancevice and @KopfKrieg*
* 0.0.6 -> **MAJOR OVERHAUL**

  Added entrypoint to `setup.py`, now you don't have to install the commandline script seperately!

  Simply use `glitch_this args` from the commandline after `pip3 install glitch-this`!

  Add **Glitching an image to GIF support** in the library! Now you can specify the necessary arguments to get a list of frames that you can use to make a GIF as well as normal images!

* 0.0.7 -> Implement **version checker** in commandline script

  The commandline tool will now inform you if the package is out of date!
