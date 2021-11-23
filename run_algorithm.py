"""This module is the commandline interface to the algorithm.

It handles the commandline interface, the files and the extraction of images from
the videos. If a reference file is found, the reference is also shown in the video."""

import plac
import numpy as np
import cv2
import os
from algorithm import motion_detection, get_algorithm_version, get_intensity
import pickle


RED = (0, 0, 255)
WHITE = (255, 255, 255)

@plac.pos('file', 'The video file path to run the algorithm on.')
@plac.flg('show', 'Show the algorithm output live')
def run_algorithm(file: str, show: bool=False) -> None:
	"""Run the motion detection algorithm on the given file.

	It can show the processing happening live. The current motion detection
	output is shown as a colored circle on top of the video in WHITE (calm) or 
	red (motion detected).
	The output is saved in the folder output.
	The execution can be quit by pressing q, when focusing the output window."""

	filename = os.path.basename(file)
	print('Run algorithm on file: {}'.format(filename))

	video = cv2.VideoCapture(file)
	framerate = video.get(cv2.CAP_PROP_FPS)
	frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	print('framerate: {}, frame count: {}'.format(framerate, frame_count))

	# try to find reference file
	reference_available = False
	reference = None
	try:
		reference_filename = 'reference/{}.pkl'.format(filename.split('.')[0])
		print(reference_filename)
		with open(reference_filename, 'rb') as ref_file:
			reference = pickle.load(ref_file)
			print('Reference loaded.')
			reference_available = True
	except FileNotFoundError:
		print('Reference file not found.')

	result = np.zeros(frame_count ,dtype=bool)
	intensity = np.zeros(frame_count)
	# processing loop
	for n in range(frame_count-1):
		_, frame = video.read()
		# check if frame was read
		if frame is None:
			print('End of video! frame {} of {}'.format(n, frame_count))
			frame_count = n
			print('Frame count set to actual amount: {}'.format(frame_count))
			break

		# pass image to run_algorithm and save the result
		result[n] = motion_detection(frame)
		intensity[n] = get_intensity(frame)

		if show:
			# add indicator for reference
			if reference_available:
				col = RED if reference['reference'][n] else WHITE
				cv2.circle(frame, center=(10, 10), radius=10, 
					color=col, thickness=-1)
			# add indicator for algorithm
			col = RED if result[n] else WHITE
			cv2.circle(frame, center=(20, 10), radius=10, 
				color=col, thickness=-1)
			# show image
			cv2.imshow('Doggy Cam', frame)

		key = cv2.waitKey(1)
		if key & 0xFF == ord('q'):
			# allow quitting by pressing q
			print('Quitting...')
			exit()

	# shorten result & intensity array to actual length
	result = result[:frame_count]
	intensity = intensity[:frame_count]

	# 2-D array with intensity and the annotated values for 
	# clean up, if wrong frame_count can be fixed
	diff = len(reference['reference'])-len(intensity)
	intensity = np.insert(intensity,len(intensity),np.zeros(diff))
	temp = np.vstack((reference['reference'],intensity))
	temp = temp.T

	# export temp to csv 
	np.savetxt('output/intensity.csv', temp, delimiter=',')

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