"""This module is the commandline interface to the algorithm.

It handles the commandline interface, the files and the extraction of images from
the videos."""

import plac
import numpy as np
import cv2
import os
from algorithm import motion_detection, get_algorithm_version
import pickle

RED = (255, 0, 0)
GREEN = (0, 255, 0)

@plac.pos('file', 'The video file path to run the algorithm on.')
@plac.flg('show', 'Show the algorithm output live')
def run_algorithm(file: str, show: bool=False) -> None:
	"""Run the motion detection algorithm on the given file.

	It can show the processing happening live. The current motion detection
	output is shown as a colored circle on top of the video in green (calm) or 
	red (motion detected).
	The output is saved in the folder output.
	The execution can be quit by pressing q, when focusing the output window."""

	filename = os.path.basename(file)
	print('Run algorithm on file: {}'.format(filename))

	video = cv2.VideoCapture(file)
	framerate = video.get(cv2.CAP_PROP_FPS)
	frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	print('framerate: {}, frame count: {}'.format(framerate, frame_count))

	result = np.zeros(frame_count ,dtype=bool)
	# processing loop
	for n in range(frame_count-1):
		_, frame = video.read()
		# check if frame was read
		if frame is None:
			print('End of video! frame {} of {}'.format(n, frame_count))
			break

		# pass image to run_algorithm and save the result
		result[n] = motion_detection(frame)

		if show:
			# TODO: add indicator of result
			col = RED if result[n] else GREEN
			cv2.circle(frame, center=(10, 10), radius=10, color=col, thickness=-1)
			cv2.imshow('Doggy Cam', frame)

		key = cv2.waitKey(1)
		if key & 0xFF == ord('q'):
			# allow quitting by pressing q
			print('Quitting...')
			exit()

	# TODO: shorten result array to actual length?

	# save result with framerate and frame count in pickle file
	data = {}
	data['framerate'] = framerate
	data['frame_count'] = frame_count
	data['result'] = result
	data['version'] = get_algorithm_version()

	save_filename = '{}-{}.pkl'.format(filename.split('.')[0], data['version'])

	with open('output/{}'.format(save_filename), 'wb') as save_file:
		pickle.dump(data, save_file)

	print('Saved to {}.'.format(save_filename))

if __name__ == '__main__':
	plac.call(run_algorithm)