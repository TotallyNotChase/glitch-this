## Version 0.0.1
* Base setup
## Version 0.0.2
* Make `color_offset` optional, you can set it to `True` when calling `glitch_image()` or, if you're using the script, include the param `-c`.
## Version 0.0.3
* Fix not being able to use image names with dots in them

  *Thanks to @[ojensen5115](https://github.com/ojensen5115)*
## Version 0.0.4
* Add detailed exceptions

  *Thanks to @[amancevice](https://github.com/amancevice)*
## Version 0.0.5
* Change `==` to `is`

  *Thanks to @[amancevice](https://github.com/amancevice) and @[KopfKrieg](https://github.com/KopfKrieg)*
## Version 0.0.6 - **MAJOR**
* Added entrypoint to `setup.py`, now you don't have to install the commandline script seperately!
* Simply use `glitch_this args` from the commandline after `pip3 install glitch-this`!
* Add **Glitching an image to GIF support** in the library! Now you can specify the necessary arguments to get a list of frames that you can use to make a GIF as well as normal images!

## Version 0.0.7 
* Implement **version checker** in commandline script

  The commandline tool will now inform you if the package is out of date!

## Version 0.0.7.1 - Patch
* Fix a script breaking bug

## Version 0.0.7.2 - Patch
* Fix missing frames argument

## Version 0.0.8 - **MAJOR**
* Add support for `Image` object input, now you can directly pass an `Image` object to the library!
* Add support for glitching GIFs to GIFs, That's right! You can now input a GIF to turn it into a **GLITCHED GIF**!
* Cleanup code
* Add more docs

## Version 0.0.9 - **Major**
* The library will now cleanup after itself when making glitched GIFs
*  NEW Parameters for `commandline.py`:-
  * `-l, --loop`: Specify how many times the GIF should loop

    Defaults to 0, i.e infinite loop
  * `-f, --force`: The script will no longer automatically overwrite existing files, you need to include `-f` for it do so

    Defaults to False
  * `-o, --outfile`: Specify a full/relative path to write the output file to

    check out the [docs](https://github.com/TotallyNotChase/glitch-this/wiki) for information on how to use these!
* Add more sanity checks in `commandline.py`
* Reduce compression level from 6 to 3 in `commandline.py` (improves performance significantly)
* `-f,--frames` has been renamed to `-fr, --frames`

## Version 0.0.9.1 - Patch
* Reduce compression level from 6 to 3 `glitch_this.py` (improves performance)
