import numpy as np
import cv2 as cv

def check_threshold(x, threshold):
    return x >= threshold

def main():
    import os
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'image/test_image.jpg')
    img = cv.imread(filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    threshold = 5
    intensity = img.sum() # image is just numpy array
    
    print('threshold = ' + str(threshold))
    print('intensity = ' + str(intensity))
    print('above threshold? ' + str(check_threshold(intensity,threshold)))
    cv.imshow('Image',img)
    cv.waitKey(0)


if __name__ == '__main__':
    main()
