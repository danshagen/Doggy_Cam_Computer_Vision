"""Dog motion detection algorithm.

This contains the implementation of the computer vision algorithm for the 
project Doggy Cam. This module does no file handling and receives as input
images and returns the algorithm output of whether dog motion was detected."""

import numpy as np
import cv2 as cv

ALGORITHM_NAME = 'dummy'
ALGORITHM_VERSION = 'v2'

def motion_detection(image: np.array) -> bool:
    """This function is called for every image in a video and returns whether 
    dog motion and activity was detected for that frame."""

    # background subtraction
    # sum all motion pixels
    sum = image.sum()

    threshold = 5
    result = sum >= threshold
    # TODO: logging module might be better, so output for every frame can be turned off
    # print('threshold = ' + str(threshold))
    # print('intensity = ' + str(intensity))
    # print('above threshold? ' + str(check_threshold(intensity,threshold)))

    # dummy value: always return false
    return True

def motion_detection_reset() -> None:
    """This functions resets the algorithm to be ready for a new video stream."""
    pass

def get_algorithm_version() -> str:
    """A string identifiying the current algorithm is returned. 

    The string contains the algorithm kind and a version, for example:
    dummy_v1 or simple_threshold_v2."""
    return '{}_{}'.format(ALGORITHM_NAME, ALGORITHM_VERSION)

