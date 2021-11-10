import numpy as np
import cv2 as cv

def sum_intensity(img):
    h = img.shape[0]
    w = img.shape[1]
    sum = 0

    for y in range(0,h):
        for x in range(0,w):
            sum += img[y,x]

    return sum

def check_threshold(x, threshold):
    if x >= threshold:
        return True
    return False

def main():
    import os
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'image/test_image.jpg')
    img = cv.imread(filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    threshold = 5
    intensity = sum_intensity(img)
    
    print('threshold = ' + str(threshold))
    print('intensity = ' + str(intensity))
    print('above threshold? ' + str(check_threshold(intensity,threshold)))
    cv.imshow('Image',img)
    cv.waitKey(0)


if __name__ == '__main__':
    main()