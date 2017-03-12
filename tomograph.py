import argparse


def main():
    args = get_args()


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--alpha", help="")
    ap.add_argument("-n", "--detectors", help="")
    ap.add_argument("-l", "--range", help="")
    ap.add_argument("-i", "--image_path", help="")
    return vars(ap.parse_args())


if __name__ == '__main__':
    main()
