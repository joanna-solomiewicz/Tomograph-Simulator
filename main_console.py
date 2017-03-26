import matplotlib.pyplot as plt
from tomograph import *
import argparse


def main():
    args = get_args()
    alpha = get_alpha(args)
    detectors_number = get_detectors_number(args)
    detectors_range = get_detectors_range(args)
    image_path = get_image_path(args)

    input = imread_square(image_path)
    plt.imshow(input, cmap='gray')
    plt.show()

    sinogram = radon_transform(alpha, detectors_number, detectors_range, input)
    plt.imshow(sinogram, cmap='gray')
    plt.show()

    output = image_reconstruction(alpha, detectors_number, detectors_range, sinogram, input.shape[0])
    plt.imshow(output, cmap='gray')
    plt.show()

    # print(filter([1,2,3,4,5]))



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


def get_detectors_number(args):
    detectors = int(args.get("detectors", False))
    if not detectors:
        print('You must specify number of detectors using --detectors option.')
        sys.exit()
    return detectors


def get_detectors_range(args):
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
