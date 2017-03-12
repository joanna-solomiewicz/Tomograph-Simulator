import argparse

import sys


def main():
    args = get_args()


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--alpha", help="")
    ap.add_argument("-n", "--detectors", help="")
    ap.add_argument("-l", "--range", help="")
    ap.add_argument("-i", "--image_path", help="")
    return vars(ap.parse_args())


def get_alpha(args):
    alpha = args.get("alpha", False)
    if not alpha:
        print('You must specify alpha angle using --alpha option.')
        sys.exit()
    return alpha


def get_detectors(args):
    detectors = args.get("detectors", False)
    if not detectors:
        print('You must specify number of detectors using --detectors option.')
        sys.exit()
    return detectors


def get_range(args):
    range = args.get("detectors", False)
    if not range:
        print('You must specify range using --range option.')
        sys.exit()
    return range


def get_image(args):
    image = args.get("detectors", False)
    if not image:
        print('You must specify image path using --image_path option.')
        sys.exit()
    return image


if __name__ == '__main__':
    main()
