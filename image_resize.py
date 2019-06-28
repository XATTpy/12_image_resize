from __future__ import print_function
import PIL
from PIL import Image
import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description='Resize image.')
    parser.add_argument('input', type=str, help='Input path to imagefile.')
    parser.add_argument('--width', type=int, default=False, help='Width of the resulting image.')
    parser.add_argument('--height', type=int, default=False, help='Height of the resulting image.')
    parser.add_argument(
        '--scale', 
        type=float, 
        default=False, 
        help='How many times to enlarge the image (maybe less than 1). Cannot be used if width or height is specified.'
    )
    parser.add_argument('--output', type=str, default=False, help='Where to put the resulting file.')
    args = parser.parse_args()
    return args

def get_imgpath(args):
    return args.input


def load_img(img_path):
    img = Image.open(img_path)
    return img


def get_sizes(img):
    width, height = img.size 
    return width, height


def get_ratio(width, height):
    if height > width:
        ratio = height / width
        sign = 1
    else:
        ratio = width / height
        sign = 0
    return ratio, sign


def get_new_sizes(args, ratio, sign, width, height):
    if args.width and args.height:
        new_width, new_height = args.width, args.height
        if new_width / new_height != width / height:
            print('Attention! The proportions do not match the original image.')
    elif args.width and not args.height:
        new_width = args.width
        new_height = new_width * ratio if sign else new_width / ratio
        new_height = round(new_height)
    elif not args.width and args.height:
        new_height = args.height
        new_width = new_height / ratio if sign else new_height * ratio
        new_width = round(new_width)
    else:
        new_width, new_height = width, height
    return new_width, new_height


def get_scale(args):
    scale = args.scale
    return scale


def get_new_sizes_by_scale(scale, width, height):
    new_width = round(width*scale)
    new_height = round(height*scale)
    return new_width, new_height


def get_new_img(img, new_width, new_height):
    new_img = img.resize((new_width, new_height), PIL.Image.ANTIALIAS)
    return new_img


def get_img_info(img_path):
    imgdirpath = os.path.split(img_path)[0]
    imgname, imgformat = os.path.split(img_path)[1].split('.')
    return imgname, imgformat, imgdirpath


def save_new_img(new_img, output, imgname, imgformat, imgdirpath, new_width, new_height):
    if output:
        imgname = imgname + '.{}'.format(imgformat)
        path = os.path.join(output, imgname)
        new_img.save(path)
    else:
        imgname = imgname + "__{}x{}.{}".format(new_width, new_height, imgformat)
        path = os.path.join(imgdirpath, imgname)
        new_img.save(path)


if __name__ == '__main__':
    args = get_args()
    img_path = get_imgpath(args)
    img = load_img(img_path)
    width, height = get_sizes(img)
    output = args.output

    scale = get_scale(args)
    if scale and (args.width or args.height):
        quit('If a scale is specified, then the width and height cannot be specified.')
    elif scale >= 1:
        quit('Scale must be less than 1')
    elif scale:
        new_width, new_height = get_new_sizes_by_scale(scale, width, height)
    else:
        ratio, sign = get_ratio(width, height)
        new_width, new_height = get_new_sizes(args, ratio, sign, width, height)

    new_img = get_new_img(img, new_width, new_height)
    imgname, imgformat, imgdirpath = get_img_info(img_path)
    save_new_img(new_img, output, imgname, imgformat, imgdirpath, new_width, new_height)
