# ArtFrame Tools
Sample implementation for converting images to and from the format used by the ArtFrame.

## to_rawz.py
Converts any image format that is supported by Pillow to rawz. Note that this implementation does **not** implement
* dithering
* resizing
* cropping

So make sure that you use the screen resolution of your device.

## from_rawz.py
Converts a rawz file back to a 4-bit grayscale png. It trys to deduce the image dimensions.

# Help: to_rawz.py
```
usage: to_rawz.py [-h] image [image ...]

Convert images for usage with the ArtFrame's mode 'Remote'.

positional arguments:
  image       images to convert to rawz

optional arguments:
  -h, --help  show this help message and exit
```

# Help: from_rawz.py
```
usage: from_rawz.py [-h] [-d X Y] image

Convert a *.rawz image back to *_.png for inspection purposes.

positional arguments:
  image       file to convert to png

optional arguments:
  -h, --help  show this help message and exit
  -d X Y      optional image dimension
```
