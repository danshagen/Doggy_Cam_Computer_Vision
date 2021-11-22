"""Convert the video annotation output to reference data for algorithm evaluation.

Most simple extraction used: only timestamps, always assume it is motion between
the timestamps."""

import plac
import os
import numpy as np
import cv2
import pickle

def convert_annotation(file: str) -> None:
	filename = os.path.basename(file)
	print('Converting annotations from file: {}'.format(filename))

	# get timestamps from file
	pairs = []
	with open(file, 'r') as in_file:
		# discard first two comment lines
		in_file.readline()
		in_file.readline()
		for line in in_file:
			_, _, t1, t2, _ = line.strip().split(',')
			t1 = float(t1)
			t2 = float(t2)
			print('t1: {}, t2: {}'.format(t1, t2))
			pairs.append((t1, t2))

	# get framerate and frame_count
	framerate, frame_count = get_video_info('video/{}.mp4'.format(filename.split('.')[0]))

	# for each timestamp calculate frames
	frame_pairs = []
	for t1, t2 in pairs:
		frame_pairs.append((timestamp_to_sample(t1, framerate), 
							timestamp_to_sample(t2, framerate)))

	# create numpy array with length of frames
	reference = np.zeros(frame_count, dtype=bool)

	# change elements between timestamps to True
	for f1, f2 in frame_pairs:
		for i in range(f1, f2):
			reference[i] = True

	# save in reference file
	data = {}
	data['framerate'] = framerate
	data['frame_count'] = frame_count
	data['reference'] = reference

	write_filename = 'reference/{}.pkl'.format(filename.split('.')[0])
	with open(write_filename, 'wb') as write_file:
		pickle.dump(data, write_file)

	# exit
	print('Done')


def timestamp_to_sample(timestamp, framerate) -> int:
	return int(timestamp * framerate)

def get_video_info(filename) -> (float, int):
	video = cv2.VideoCapture(filename)
	framerate = video.get(cv2.CAP_PROP_FPS)
	frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	return (framerate, frame_count)


if __name__ == '__main__':
	plac.call(convert_annotation)