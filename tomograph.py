import math
import sys

import matplotlib.image as img
import numpy as np
from scipy.spatial import distance
from scipy import signal as sg


def radon_transform(alpha, detectors_number, detectors_range, image, percentage=100):
    image_width = image.shape[0]
    sinogram_length = np.arange(0, 360, alpha).__len__()
    sinogram_width = int(detectors_number)
    sinogram = np.zeros((sinogram_length, sinogram_width))
    iterations = sinogram_length * percentage / 100

    for i, emitter_angle in enumerate(np.arange(0, 360, alpha)):
        if i >= iterations:
            break
        emitter_x = image_width / 2 + math.cos(math.radians(emitter_angle)) * (image_width / 2)
        emitter_y = image_width / 2 - math.sin(math.radians(emitter_angle)) * (image_width / 2)
        sinogram_line = []
        for detector_angle in np.linspace(emitter_angle + math.degrees(math.pi) - detectors_range / 2,
                                          emitter_angle + math.degrees(math.pi) + detectors_range / 2,
                                          detectors_number):
            detector_x = image_width / 2 + math.cos(math.radians(detector_angle)) * (image_width / 2)
            detector_y = image_width / 2 - math.sin(math.radians(detector_angle)) * (image_width / 2)
            line_points = get_bresenham_line((int(emitter_x), int(emitter_y)), (int(detector_x), int(detector_y)))

            normalization_factor = distance.euclidean((emitter_x, emitter_y), (detector_x, detector_y)) \
                                   / len(line_points) / image_width
            pixel_sum = sum([image[point[0] - 1, point[1] - 1] for point in line_points]) * normalization_factor
            sinogram_line.append(pixel_sum)
        sinogram[i] = filter(sinogram_line)
    return np.array(sinogram)


def image_reconstruction(alpha, detectors_number, detectors_range, sinogram, image_width, percentage=100):
    image = np.zeros((image_width, image_width))
    i = 0
    j = 0
    sinogram_length = np.arange(0, 360, alpha).__len__()
    iterations = sinogram_length * percentage / 100

    for emitter_angle in np.arange(0, 360, alpha):
        if i >= iterations:
            break
        emitter_x = image_width / 2 + math.cos(math.radians(emitter_angle)) * (image_width / 2)
        emitter_y = image_width / 2 - math.sin(math.radians(emitter_angle)) * (image_width / 2)
        for detector_angle in np.linspace(emitter_angle + math.degrees(math.pi) - detectors_range / 2,
                                          emitter_angle + math.degrees(math.pi) + detectors_range / 2,
                                          detectors_number):
            detector_x = image_width / 2 + math.cos(math.radians(detector_angle)) * (image_width / 2)
            detector_y = image_width / 2 - math.sin(math.radians(detector_angle)) * (image_width / 2)
            line_points = get_bresenham_line((int(emitter_x), int(emitter_y)), (int(detector_x), int(detector_y)))
            for point in line_points:
                image[point[0] - 1][point[1] - 1] += sinogram[i][j]
            j += 1
        j = 0
        i += 1

    if image.max() != 0:
        image = image / image.max() * 255
    return image


def get_bresenham_line(point_start, point_end):
    points = []
    x_start, y_start = point_start
    x_end, y_end = point_end
    dx = x_end - x_start
    dy = y_end - y_start
    x, y = x_start, y_start
    sx = -1 if x_start > x_end else 1
    sy = -1 if y_start > y_end else 1

    if abs(dx) > abs(dy):  # lower half
        a = dy / dx
        b = y_start - a * x_start
        while x != x_end:
            points.append((x, y))
            x += sx
            y_real = a * x + b
            y_middle = y + sy / 2
            if sy == 1:
                if y_real >= y_middle:
                    y += sy
            else:
                if y_real < y_middle:
                    y += sy

    else:  # higher half
        a = dx / dy
        b = x_start - a * y_start
        while y != y_end:
            points.append((x, y))
            y += sy
            x_real = a * y + b
            x_middle = x + sx / 2
            if sx == 1:
                if x_real >= x_middle:
                    x += sx
            else:
                if x_real < x_middle:
                    x += sx

    points.append((x, y))
    return points


def filter(row):
    f = create_kernel(len(row))
    convolve = sg.convolve(row, f, "same")
    return convolve


def create_kernel(size):
    f = []
    middle = size // 2
    for i in range(0, size):
        if i == middle:
            f.append(1)
        elif i % 2 == 0:
            f.append(0)
        else:
            f.append((-4 / math.pow(math.pi, 2)) / math.pow((i - middle), 2))
    return f


def imread_square(image_path):
    image = img.imread(image_path)
    if len(image.shape) == 3:
        image = image[:, :, 0]
    if image is None:
        print('Unable to open image.')
        sys.exit()
    width, height = image.shape
    if width != height:
        print('Image must be a square.')
        sys.exit()
    return image
