"""This module runs the dog unrest detection algorithm and saves the video and
result as files."""

import plac
# import numpy as np
import cv2
# import os
from algorithm import motion_detection, get_algorithm_version
# import file_handler
# from evaluate_algorithm import update_frame_count

def run():
	"""Press Ctrl-C to terminate."""

	print('Opening webcam stream...')
	video = cv2.VideoCapture(0)

	frame_width = int(video.get(3))
	frame_height = int(video.get(4))
	size = (frame_width, frame_height)
	webcam = cv2.VideoWriter('webcam.avi', 
	                         cv2.VideoWriter_fourcc(*'MJPG'),
	                         10, size)

	print('Starting doggy cam.')
	events = 0 
	unrest = False
	temp = None

	try:
		while True:
			ret, frame = video.read()
			if frame is None:
				break

			# detect motion
			result, _, _ = motion_detection(frame)
			cv2.imshow('Doggy Cam: Standard View', frame) # DEBUG

			# save video to file
			webcam.write(frame)

			# detect event times and save video
			if result and not unrest:
				events += 1
				temp = cv2.VideoWriter('temp_{}.avi'.format(events), 
			                         	cv2.VideoWriter_fourcc(*'MJPG'),
			                         	10, size)
			if result:
				temp.write(frame)
			unrest = result

			cv2.waitKey(1) # DEBUG
	except KeyboardInterrupt:
		pass

	print('Exiting doggy cam.')
	video.release()

	print('{} events detected.'.format(events))


if __name__ == '__main__':
	plac.call(run)