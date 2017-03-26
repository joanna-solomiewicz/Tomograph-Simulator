import matplotlib.pyplot as plt
from tomograph import *


def main():
    args = get_args()
    alpha = get_alpha(args)
    detectors_number = get_detectors_number(args)
    detectors_range = get_detectors_range(args)
    image_path = get_image_path(args)

    image = imread_square(image_path)
    plt.imshow(image, cmap='gray')
    plt.savefig('image.jpg')

    image_sinogram = radon_transform(alpha, detectors_number, detectors_range, image)
    plt.imshow(image_sinogram, cmap='gray')
    plt.savefig('sinogram.jpg')

    sinogram_image = image_reconstruction(alpha, detectors_number, detectors_range, image_sinogram, image.shape[0])
    plt.imshow(sinogram_image, cmap='gray')
    plt.savefig('image_reconstructed.jpg')


if __name__ == '__main__':
    main()
