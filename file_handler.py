import os
import pickle
import numpy as np

def save_algorithm_result(filename, frame_rate, frame_count, result, algorithm_version):
    data = {}
    data['framerate'] = frame_rate
    data['frame_count'] = frame_count
    data['result'] = result
    data['version'] = algorithm_version

    save_filename = '{}-{}.pkl'.format(filename.split('.')[0], data['version'])

    with open('output/{}'.format(save_filename), 'wb') as save_file:
        pickle.dump(data, save_file)
    print('Saved to {}.'.format(save_filename))

def scan_algortihm_files(algorithm_version):
	algorithm_files = []
	video_files = []
	for file in os.scandir('output'):
		if algorithm_version in file.name:
			algorithm_files.append('output/{}'.format(file.name))
			video_files.append(file.name.split('.')[0][:file.name.find(algorithm_version)-1])
	print('Algorithm data files found: {}'.format(algorithm_files))
	return (algorithm_files, video_files)

def scan_reference_files(video_files):
	reference_files = []
	for file in video_files:
		reference_file = '{}.pkl'.format(file)
		if not os.path.exists('reference/{}'.format(reference_file)):
			print('reference for file {}.mp4 not found!'.format(file))
			# TODO: remove algorithm file
		else:
			reference_files.append(reference_file)
	print('Reference data files found: {}'.format(reference_files))
	return reference_files


def load_algorithm_data(algorithm_files):
	algorithm_data = []
	for file in algorithm_files:
		with open(file, 'rb') as alg_file: 
			algorithm_data.append(pickle.load(alg_file))
	return algorithm_data

def load_reference_data(filename):
    try:
        reference_filename = 'reference/{}.pkl'.format(filename.split('.')[0])
        with open(reference_filename, 'rb') as ref_file:
            reference = pickle.load(ref_file)
            print('Reference {} loaded.'.format(reference_filename))
            return (True, reference)
    except FileNotFoundError:
        print('Reference file not found.')
        return (False, None)

def save_csv(intensities):
	np.savetxt('output/intensity.csv', intensities, delimiter=',')
