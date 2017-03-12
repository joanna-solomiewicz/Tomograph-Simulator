import argparse
import cv2
import sys
import math


def main():
    args = get_args()
    alpha = get_alpha(args)
    detectors = get_detectors(args)
    range = get_range(args)
    image_path = get_image_path(args)
    image = imread_square(image_path)


def radon_transform(alpha, detectors, range, image):
    image_width = image.shape[0]
    for emitter_angle in range(0, 360, alpha):
        emitter_x = math.cos(emitter_angle) * (image_width / 2)
        emitter_y = math.sin(emitter_angle) * (image_width / 2)
        step = range / detectors
        for detector_angle in range(alpha + math.pi - range / 2, alpha + math.pi + range / 2, step):
            detector_x = math.cos(detector_angle) * (image_width / 2)
            detector_y = math.cos(detector_angle) * (image_width / 2)


def imread_square(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print('Unable to open image.')
        sys.exit()
    width, height, _ = image.shape
    if width != height:
        print('Image must be a square.')
        sys.exit()


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--alpha", help="")
    ap.add_argument("-n", "--detectors", help="")
    ap.add_argument("-l", "--range", help="")
    ap.add_argument("-i", "--image_path", help="")
    return vars(ap.parse_args())


def get_alpha(args):
    alpha = float(args.get("alpha", False))
    if not alpha:
        print('You must specify alpha angle using --alpha option.')
        sys.exit()
    return alpha


def get_detectors(args):
    detectors = int(args.get("detectors", False))
    if not detectors:
        print('You must specify number of detectors using --detectors option.')
        sys.exit()
    return detectors


def get_range(args):
    range = float(args.get("range", False))
    if not range:
        print('You must specify range using --range option.')
        sys.exit()
    if not (0 <= range <= 360):
        print('Range must be angle between 0 and 360.')
        sys.exit()
    return range


def get_image_path(args):
    image_path = args.get("image_path", False)
    if not image_path:
        print('You must specify image path using --image_path option.')
        sys.exit()
    return image_path


if __name__ == '__main__':
    main()
