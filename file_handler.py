import os
import pickle

def find_algorithm_output(algorithm: str):
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

	return (algorithm_files, algorithm_data, video_files)