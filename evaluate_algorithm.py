"""This module evaluates the output of the algorithm against the reference."""

import plac
import os
import numpy as np
import pickle
import sys

@plac.pos('algorithm', 'Algorithm name, for example dummy_v1', type=str)
def evaluate_algorithm(algorithm: str) -> None:
	"""Evaluate the output of the given algorithm against the reference data.
	
	Finds the algorithm output data automatically from the output folder and
	loads the corresponding reference data. It outputs the evaluation on the 
	terminal.

	TODO: save the data"""
	
	# find all algorithm output files
	algorithm_files = []
	algorithm_data = []
	video_files = []
	for file in os.scandir('output'):
		if algorithm in file.name:
			algorithm_files.append('output/{}'.format(file.name))
			video_files.append(file.name.split('.')[0][:file.name.find(algorithm)-1])
	print('Algorithm data files found: {}'.format(algorithm_files))
	for file in algorithm_files:
		with open(file, 'rb') as alg_file: 
			algorithm_data.append(pickle.load(alg_file))

	# find the corresponding reference files
	ref_files = []
	ref_data = []
	for file in video_files:
		ref_file = 'reference/{}.pkl'.format(file)
		if not os.path.exists(ref_file):
			print('reference for file {}.mp4 not found!'.format(file))
			# TODO: remove algorithm file
		else:
			ref_files.append(ref_file)
	print('Reference data files found: {}'.format(ref_files))
	for file in ref_files:
		with open(file, 'rb') as ref_file:
			ref_data.append(pickle.load(ref_file))

	# compare algorithm vs reference
	for i in range(len(ref_data)):
		print('File: {}'.format(video_files[i]))

		frame_count = algorithm_data[i].get('frame_count') 				# get corrected frame count from algortihm output
		ref_data[i] = update_frame_count(frame_count, ref_data[i])		# slice reference data to correct frame count

		t, a, tf, af, p = analyse_true_positives(ref_data[i], algorithm_data[i])
		print('  True positives: ', end='')
		print('  {:.1f}s of {:.1f}s ({:.1f}%), {} of {} frames.'.format(a, t, p, af, tf))


		false_positives_seconds, false_positives_frames = analyse_false_positives(ref_data[i], algorithm_data[i])
		print('  False positives:', end='')
		print('  {:.1f}s ({} frames).'.format(false_positives_seconds, false_positives_frames))

	# save evaluation data

def analyse_true_positives(reference, algorithm) -> (int, int, int, int, float):
	ref_frames = np.where(reference['reference'] == True)[0]
	total_positives = len(ref_frames)

	try:
		alg_positives = np.sum(algorithm['result'][ref_frames])
	except:
		print('Frame ' + str(max(ref_frames)) + ' not in results of algorithm.')
		print('Last available frame: ' + str(len(algorithm['result'])))
		sys.exit()

	framerate = reference['framerate']
	return (total_positives/framerate, alg_positives/framerate,
	total_positives, alg_positives, alg_positives/total_positives*100)


def analyse_false_positives(reference, algorithm) -> (int, int):
	alg_positives = np.where(algorithm['result'] == True)[0]
	false_positives = np.sum(np.where(
		reference['reference'][alg_positives] == False))

	framerate = reference['framerate']
	return (false_positives/framerate, false_positives)


def update_frame_count(frame_count, thisdict):
	tmp = thisdict.get('reference')
	tmp = tmp[:frame_count]
	thisdict.update({'reference':tmp})
	thisdict.update({'frame_count':frame_count})
	return thisdict

# TODO: function/module for getting all evaluation data and comparing, plotting

if __name__ == '__main__':
	plac.call(evaluate_algorithm)