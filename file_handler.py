import pickle

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
