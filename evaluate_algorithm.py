"""This module evaluates the output of the algorithm against the reference."""

import plac
import numpy as np
import sys
import file_handler

@plac.pos('algorithm', 'Algorithm name, for example dummy_v1', type=str)
def evaluate_algorithm(algorithm_version: str) -> None:
	"""Evaluate the output of the given algorithm against the reference data.
	
	Finds the algorithm output data automatically from the output folder and
	loads the corresponding reference data. It outputs the evaluation on the 
	terminal.

	TODO: save the data"""
	
	# find and load all algorithm output files
	algorithm_files, video_files = file_handler.scan_algortihm_files(algorithm_version)
	algorithm_data = file_handler.load_algorithm_data(algorithm_files)
	
	# find and load the corresponding reference files
	ref_data = []
	ref_files = file_handler.scan_reference_files(video_files)
	for file in ref_files:
		_, tmp = file_handler.load_reference_data(file)
		ref_data.append(tmp)

	e_tp = 0
	e_tp_tot = 0
	e_fp = 0 
	e_fp_tot = 0
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

		event_tp, event_tot = events_true_positives(ref_data[i]['reference'], algorithm_data[i]['result'])
		print('Events:\n  True positives: {} of {}'.format(event_tp, event_tot))
		e_tp += event_tp
		e_tp_tot += event_tot

		event_fp, event_tot = events_false_positives(ref_data[i]['reference'], algorithm_data[i]['result'])
		print('  False positives: {} of {}'.format(event_fp, event_tot))
		e_fp += event_fp
		e_fp_tot += event_tot

	print('\n\nEvents all videos:\n  True positives: {} of {} ({:.1f}%)\n  False positives: {} of {} ({:.1f}%)'.format(
		e_tp, e_tp_tot, 100*e_tp/e_tp_tot,
		e_fp, e_fp_tot, 100*e_fp/e_fp_tot))

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
	false_positives = len(np.where(reference['reference'][alg_positives] == False)[0])

	framerate = reference['framerate']
	return (false_positives/framerate, false_positives)


def update_frame_count(frame_count, thisdict):
	tmp = thisdict.get('reference')
	tmp = tmp[:frame_count]
	thisdict.update({'reference':tmp})
	thisdict.update({'frame_count':frame_count})
	return thisdict

def get_events(array):
	events = []
	# get events from reference data (start and end sample index)
	diff = np.diff(array)
	rising_edge = np.where(diff > 0)[0]
	falling_edge = np.where(diff < 0)[0]
	# if first edge is a falling edge, add 0 as a rising edge
	if falling_edge[0] < rising_edge[0]:
		rising_edge = np.insert(rising_edge, 0, 0) # insert 0 at index 0
	# if last edge is a rising edge, add last sample index as falling edge
	if rising_edge[-1] > falling_edge[-1]:
		falling_edge = np.append(falling_edge, [len(array)-1])

	assert(len(falling_edge) == len(rising_edge))

	for i in range(len(falling_edge)):
		events.append((rising_edge[i], falling_edge[i]))
	return events


def events_true_positives(reference, algorithm):
	"""Detect how many annotated motion events were detected."""
	reference = reference.astype(int)
	algorithm = algorithm.astype(int)

	true_positives = 0
	events = get_events(reference)

	# for each event, get overlap (in percent), if higher than 50% the event
	# is evaluated as detected
	for start, stop in events:
		overlap = np.average(algorithm[start:stop])
		if overlap >= 0.5:
			true_positives += 1
	 
	# calculate total result
	return true_positives, len(events)

def events_false_positives(reference, algorithm):
	"""Detect how many annotated motion events were detected."""
	reference = reference.astype(int)
	algorithm = algorithm.astype(int)

	false_positives = 0
	events = get_events(algorithm)

	# for each event, get overlap (in percent), if higher than 50% the event
	# is evaluated as detected
	for start, stop in events:
		overlap = np.average(reference[start:stop])
		if overlap == 0:
			false_positives += 1
	 
	# calculate total result
	return false_positives, len(events)


if __name__ == '__main__':
	plac.call(evaluate_algorithm)