#!/usr/bin/env python3

import argparse
import sys
import os
import png
import zlib
import math

DIMENSIONS = {(800, 600), (1200, 825)}
SIZE_TO_DIMENSIONS = {x*y//2: (x,y) for x,y in DIMENSIONS}

def read_content(file):
    with open(file, 'rb') as content_file:
        return content_file.read()

def to_pixelbuf(raw, dimension):
    expected_size = math.prod(dimension)//2
    if len(raw) != expected_size:
        print('Warning: Wrong dimensions given', file=sys.stderr)
        if len(raw) > expected_size:
            exit(-1)

    w, h = dimension
    buf = [[0 for x in range(w)] for y in range(h)]
    for idx, c in enumerate(raw):
        idx = idx*2
        first = int(c) >> 4
        sec = int(c) & 0xF
        buf[idx//w][idx%w] = sec
        buf[(idx+1)//w][(idx+1)%w] = first
    return buf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a *.rawz image back to *_.png for inspection purposes.')
    parser.add_argument('image', type=str, help='file to convert to png')
    parser.add_argument('-d', metavar=('X', 'Y'), type=int, nargs=2, help='optional image dimension')
    args = parser.parse_args(args=None if sys.argv[1:] else ['-h'])

    for filename in [args.image]:
        filename_out = os.path.splitext(filename)[0]+'_.png'
        print(f'Writing {filename_out}')

        rawz = read_content(filename)
        try:
            raw = zlib.decompress(rawz)
        except:
            print('Could not decompress. This is not a rawz file.')
            exit(-1)
        if not args.d:
            args.d = SIZE_TO_DIMENSIONS.get(len(raw))
        if not args.d:
            print('Can\'t guess dimensions of the image. Use -d to add dimensions manually.', file=sys.stderr)
            exit(-1)
        png.from_array(to_pixelbuf(raw, args.d), 'L;4').save(filename_out)
