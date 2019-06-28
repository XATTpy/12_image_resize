# Image Resizer

This script resizes incoming image.

# How to use

For reference, run the script with the -h flag:

```bash
$ python3 image_resize.py -h
usage: image_resize.py [-h] [--width WIDTH] [--height HEIGHT] [--scale SCALE]
                       [--output OUTPUT]
                       input

Resize image.

positional arguments:
  input            Input path to imagefile.

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Width of the resulting image.
  --height HEIGHT  Height of the resulting image.
  --scale SCALE    How many times to enlarge the image (maybe less than 1).
                   Cannot be used if width or height is specified.
  --output OUTPUT  Where to put the resulting file.
```

# Quickstart

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

Then run the script:

```bash
$ python3 image_resize.py /path/to/file.jpg --width 320 --height 400 --output /path/to/dir
Attention! The proportions do not match the original image.
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
