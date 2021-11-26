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

def load_reference_data(filename):
    try:
        reference_filename = 'reference/{}.pkl'.format(filename.split('.')[0])
        print(reference_filename)
        with open(reference_filename, 'rb') as ref_file:
            reference = pickle.load(ref_file)
            print('Reference loaded.')
            return (True, reference)
    except FileNotFoundError:
        print('Reference file not found.')
        return (False, None)
