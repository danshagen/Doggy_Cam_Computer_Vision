"""This module is the commandline interface to the algorithm.

It handles the commandline interface, the files and the extraction of images from
the videos. If a reference file is found, the reference is also shown in the video."""

import plac
import numpy as np
import cv2
import os
from algorithm import motion_detection, get_algorithm_version
import file_handler

RED = (0, 0, 255)
GREEN = (0, 255, 0)

def load_video(file):
	video = cv2.VideoCapture(file)
	framerate = video.get(cv2.CAP_PROP_FPS)
	frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	print('framerate: {}, frame count: {}'.format(framerate, frame_count))
	return (video, framerate, frame_count)

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
	
	# load video
	video, framerate, frame_count = load_video(file)

	# try to find reference file
	reference_available, reference = file_handler.load_reference_data(filename)

	result = np.zeros(frame_count ,dtype=bool)
	# processing loop
	for n in range(frame_count):
		_, frame = video.read()
		# check if frame was read
		if frame is None:
			print('End of video! frame {} of {}'.format(n, frame_count))
			frame_count = n
			print('Frame count set to actual amount: {}'.format(frame_count))
			break

		# pass image to run_algorithm and save the result
		result[n] = motion_detection(frame)

		if show:
			# add indicator for reference
			if reference_available:
				col = RED if reference['reference'][n] else GREEN
				cv2.circle(frame, center=(10, 10), radius=10, 
					color=col, thickness=-1)
			# add indicator for algorithm
			col = RED if result[n] else GREEN
			cv2.circle(frame, center=(20, 10), radius=10, 
				color=col, thickness=-1)
			# show image
			cv2.imshow('Doggy Cam', frame)

		key = cv2.waitKey(1)
		if key & 0xFF == ord('q'):
			# allow quitting by pressing q
			print('Quitting...')
			exit()

	# TODO: shorten result array to actual length?
	result = result[:frame_count]

	# save result with framerate and frame count in pickle file
	file_handler.save_algorithm_result(filename, framerate, frame_count, result, get_algorithm_version())

if __name__ == '__main__':
	plac.call(run_algorithm)