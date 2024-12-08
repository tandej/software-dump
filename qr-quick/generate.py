import argparse

import qrcode
import qrcode.image.svg

parser = argparse.ArgumentParser()
parser.add_argument("data")

img = qrcode.make(
    parser.parse_args().data,
    image_factory=qrcode.image.svg.SvgPathImage,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
)

img.save("output.svg")
