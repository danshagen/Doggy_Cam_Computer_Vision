"""Dog motion detection algorithm.

This contains the implementation of the computer vision algorithm for the 
project Doggy Cam. This module does no file handling and receives as input
images and returns the algorithm output of whether dog motion was detected."""

import numpy as np
import cv2 as cv
import collections

ALGORITHM_NAME = 'intensity'
ALGORITHM_VERSION = 'v2'

back_sub = cv.createBackgroundSubtractorMOG2()

def motion_detection(frame: np.array) -> bool:
    """This function is called for every image in a video and returns whether 
    dog motion and activity was detected for that frame."""

    #back_sub = cv.createBackgroundSubtractorMOG2()

    #back_sub_frame = back_sub.apply(frame, learningRate=-1)

    # background subtraction
    # sum all motion pixels
    sum = get_intensity(frame)

    threshold = 1385203
    result = False
    if(sum > threshold):
        result = True
    #result = sum >= threshold
    # TODO: logging module might be better, so output for every frame can be turned off
    # print('threshold = ' + str(threshold))
    # print('intensity = ' + str(intensity))
    # print('above threshold? ' + str(check_threshold(intensity,threshold)))

    # return true
    return result

def identify_short_movements(algortihm_data):
    
    # shortest possible movement: n number of frames = 1 sec * 7 frames/sec
    # 7 frames plus one more on each side to identify a sequence of 7
    de = collections.deque(np.zeros(9, dtype=bool))
    idx_list = []
    for i, frame in enumerate(algortihm_data):
        de.popleft()
        de.append(frame)
        if de.count(False) is len(de): continue
        if de[-8] and not de[-9]:   
            if de[-7]:
                if de[-6]:
                    if de[-5]:
                        if de[-4]:
                            if de[-3]:
                                if de[-2]:
                                    if de[-1]: continue
                                    idx_list.append(get_new_idx(i-7, 7))
                                    continue
                                idx_list.append(get_new_idx(i-7, 6))
                                continue
                            idx_list.append(get_new_idx(i-7, 5))
                            continue
                        idx_list.append(get_new_idx(i-7, 4))
                        continue
                    idx_list.append(get_new_idx(i-7, 3))
                    continue
                idx_list.append(get_new_idx(i-7, 2))
                continue
            idx_list.append(get_new_idx(i-7, 1))
            continue
    return idx_list

def get_new_idx(frame_number, count):
    idx_list = []
    for j in range(count):
        idx_list.append(frame_number + j)
    idx_list.sort()
    return idx_list

def get_intensity(image: np.array):
    back_sub_frame = back_sub.apply(image, learningRate=-1)
    sum = back_sub_frame.sum()
    return sum

def motion_detection_reset() -> None:
    """This functions resets the algorithm to be ready for a new video stream."""
    pass

def get_algorithm_version() -> str:
    """A string identifiying the current algorithm is returned. 

    The string contains the algorithm kind and a version, for example:
    dummy_v1 or simple_threshold_v2."""
    return '{}_{}'.format(ALGORITHM_NAME, ALGORITHM_VERSION)

