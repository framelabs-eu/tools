#!/usr/bin/env python3

import os
import sys
import zlib
import argparse
from PIL import Image

WIDTHS = {800, 1200, 1600}

def to_rawz(image_path):
    grayscaled = to_grayscale(image_path)
    raw = to_raw(grayscaled)
    return zlib.compress(raw, level=9)

def to_raw(image):
    px = image.load()
    width, height = image.size
    if width not in WIDTHS:
        print(f'\tWarning: image width is {width}, should be one of {WIDTHS}', file=sys.stderr)

    buf = bytearray(width * height // 2)
    for y in range(height):
        for x in range(width):
            i = (y*width+x)
            if i % 2 == 0:
                buf[i//2] |= px[x, y] // 16
            else:
                buf[i//2] |= px[x, y] // 16 << 4
    return buf

def to_grayscale(image_path):
    return Image.open(image_path).convert('L')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert images for usage with the ArtFrame\'s mode \'Remote\'.')
    parser.add_argument('image', type=str, nargs='+', help='images to convert to rawz')
    args = parser.parse_args(args=None if sys.argv[1:] else ['-h'])

    for image_path in args.image:
        rawz_path = os.path.splitext(image_path)[0] + '.rawz'
        print(rawz_path)
        rawz = to_rawz(image_path)
        with open(rawz_path, 'wb') as file:
            file.write(rawz)
