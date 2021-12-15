"""Dog motion detection algorithm.

This contains the implementation of the computer vision algorithm for the 
project Doggy Cam. This module does no file handling and receives as input
images and returns the algorithm output of whether dog motion was detected."""

import numpy as np
import cv2 as cv

ALGORITHM_NAME = 'intensity'
ALGORITHM_VERSION = 'v5'

back_sub = cv.createBackgroundSubtractorMOG2(detectShadows=False)

threshold = 500000
max_intens = 640 * 480 * 3 * 127        # frame_width x frame_height x number of cahnnels x max value per channel
max_valid_intens = max_intens * .045
# TODO soft code max intensity

old_results = np.zeros(int(7.5 * 4))
old_results_idx = 0
def motion_detection(img: np.array) -> bool:
    """This function is called for every image in a video and returns whether 
    dog motion and activity was detected for that frame."""

    img_motion = back_sub.apply(img, learningRate=-1)

    # filter noise 
    kernel = np.ones((4,4),np.uint8)
    img_opening = cv.morphologyEx(img_motion, cv.MORPH_OPEN, kernel)
    img_opening = cv.cvtColor(img_opening, cv.COLOR_GRAY2BGR) # only for the red dots

    # background subtraction
    # sum all motion pixels
    sum = img_motion.sum()

    result = False
    if(sum > threshold and sum < max_valid_intens):
        result = True
    #result = sum >= threshold
    # TODO: logging module might be better, so output for every frame can be turned off
    # print('threshold = ' + str(threshold))
    # print('intensity = ' + str(intensity))
    # print('above threshold? ' + str(check_threshold(intensity,threshold)))

    # save old results for averaging
    global old_results, old_results_idx
    old_results[old_results_idx] = result
    old_results_idx += 1
    if old_results_idx >= len(old_results):
        old_results_idx = 0

    result = np.average(old_results) >= 0.5

    return result, sum, img_opening


def get_algorithm_version() -> str:
    """A string identifiying the current algorithm is returned. 

    The string contains the algorithm kind and a version, for example:
    dummy_v1 or simple_threshold_v2."""
    return '{}_{}'.format(ALGORITHM_NAME, ALGORITHM_VERSION)
