import cv2 as cv

background_substractor = cv.createBackgroundSubtractorMOG2()

def get_background_substracted_img(img):
    img = background_substractor.apply(img, learningRate=-1)
    return img

def convert2color(img):
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    return img