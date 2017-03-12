import argparse
import cv2
import sys
import math
import numpy as np


def main():
    args = get_args()
    alpha = get_alpha(args)
    detectors_number = get_detectors_number(args)
    detectors_range = get_detectors_range(args)
    image_path = get_image_path(args)
    image = imread_square(image_path)

    image_sinogram = radon_transform(alpha, detectors_number, detectors_range, image)
    cv2.imshow("Sinogram", np.array(image_sinogram))
    cv2.waitKey(0)
    cv2.destroyAllWindows()




def radon_transform(alpha, detectors_number, detectors_range, image):
    image_width = image.shape[0]
    sinogram = []
    for emitter_angle in np.arange(0, 360, alpha):
        emitter_x = image_width/2 + math.cos(emitter_angle) * (image_width / 2)
        emitter_y = image_width/2 + math.sin(emitter_angle) * (image_width / 2)
        sinogram_line = []
        for detector_angle in np.linspace(alpha + math.pi - detectors_range / 2,
                                          alpha + math.pi + detectors_range / 2,
                                          detectors_number):
            detector_x = image_width/2 + math.cos(detector_angle) * (image_width / 2)
            detector_y = image_width/2 + math.cos(detector_angle) * (image_width / 2)
            line_points = get_bresenham_line((int(emitter_x), int(emitter_y)),
                                             (int(detector_x), int(detector_y)))
            sinogram_line.append(sum([image[point[0]-1, point[1]-1] for point in line_points]))
        sinogram.append(sinogram_line)
    return sinogram


def get_bresenham_line(point_start, point_end):
    points = []
    x_start, y_start = point_start
    x_end, y_end = point_end
    dx = abs(x_end - x_start)
    dy = abs(y_end - y_start)
    x, y = x_start, y_start
    sx = -1 if x_start > x_end else 1
    sy = -1 if y_start > y_end else 1

    if dx > dy:  # lower half
        a = dy / dx
        b = y_start - a * x_start
        while x != x_end:
            points.append((x, y))
            x += sx
            y_real = a * x + b
            y_middle = y + sy / 2
            if y_real >= y_middle:
                y += sy
    else:  # higher half
        a = dx / dy
        b = x_start - a * y_start
        while y != y_end:
            points.append((x, y))
            y += sy
            x_real = a * x + b
            x_middle = x + sx / 2
            if x_real >= x_middle:
                x += sx
    points.append((x, y))
    return points


def imread_square(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print('Unable to open image.')
        sys.exit()
    width, height, _ = image.shape
    if width != height:
        print('Image must be a square.')
        sys.exit()
    return image


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--alpha", help="")
    ap.add_argument("-n", "--detectors", help="")
    ap.add_argument("-l", "--range", help="")
    ap.add_argument("-i", "--image_path", help="")
    return vars(ap.parse_args())


def get_alpha(args):
    alpha = int(args.get("alpha", False))
    if not alpha:
        print('You must specify alpha angle using --alpha option.')
        sys.exit()
    return alpha


def get_detectors_number(args):
    detectors = float(args.get("detectors", False))
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
