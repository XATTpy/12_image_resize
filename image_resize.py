import PIL
from PIL import Image
import argparse
import os
import math


def get_args():
    parser = argparse.ArgumentParser(description='Resize image.')
    parser.add_argument(
        'input',
        type=str,
        help='Input path to imagefile.'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=False,
        help='Width of the resulting image.'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=False,
        help='Height of the resulting image.'
    )
    parser.add_argument(
        '--scale', 
        type=float,
        default=1,
        help='How many times to enlarge the image (maybe less than 1). Cannot be used if width or height is specified.'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Where to put the resulting file.'
    )
    args = parser.parse_args()
    return args


def load_image(image_path):
    image = Image.open(image_path)
    return image


def get_new_sizes(width, height, input_width, input_height):
    ratio = width / height

    if input_width and input_height:
        new_width, new_height = input_width, input_height
    elif input_width and not input_height:
        new_width = input_width
        new_height = round(new_width/ratio)
    elif not input_width and input_height:
        new_height = input_height
        new_width = round(new_height*ratio)
    else:
        new_width, new_height = width, height
    return new_width, new_height


def get_new_sizes_by_scale(scale, width, height):
    new_width = round(width*scale)
    new_height = round(height*scale)
    return new_width, new_height


def get_new_image(image, new_width, new_height):
    new_image = image.resize((new_width, new_height), PIL.Image.ANTIALIAS)
    return new_image


def get_image_info(image_path):
    imagedirpath = os.path.split(image_path)[0]
    imagename, imageformat = os.path.split(image_path)[1].split('.')
    return imagename, imageformat, imagedirpath


def save_new_image(new_image, output, imagename, imageformat, imagedirpath, new_width, new_height):
    if output:
        imagename = '{}.{}'.format(imagename, imageformat)
        path = os.path.join(output, imagename)
    else:
        imagename = '{}__{}x{}.{}'.format(imagename, new_width, new_height, imageformat)
        path = os.path.join(imagedirpath, imagename)
    new_image.save(path)


def initialize_new_sizes(scale, width, height, input_width, input_height):
    if scale <= 0:
        quit('Scale must be greater than 0.')
    elif scale != 1 and (args.width or args.height):
        quit('If a scale is specified, then the width and height cannot be specified.')
    elif scale != 1:
        new_width, new_height = get_new_sizes_by_scale(scale, width, height)
    else:
        new_width, new_height = get_new_sizes(width, height, input_width, input_height)
        if new_width <= 0 or new_height <= 0:
            quit('Width and height must be greater than 0.')
        if not math.isclose(new_width/new_height, width/height, abs_tol=0.0004):
            print('Attention! The proportions do not match the original image.')
    return new_width, new_height


if __name__ == '__main__':
    args = get_args()
    image_path = args.input
    image = load_image(image_path)
    width, height = image.size
    input_width, input_height = args.width, args.height 
    scale = args.scale
    output = args.output
    if output and not os.path.isdir(output):
        quit('Enter the existing directory as output')

    new_width, new_height = initialize_new_sizes(scale, width, height, input_width, input_height)
    new_image = get_new_image(image, new_width, new_height)
    imagename, imageformat, imagedirpath = get_image_info(image_path)
    save_new_image(new_image, output, imagename, imageformat, imagedirpath, new_width, new_height)
