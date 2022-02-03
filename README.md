# Project: Doggy Cam
## Abstract
A monitoring system for dogs being left alone at home is developed using a Raspberry Pi, a webcam and computer vision algorithms. The system can monitor a room with a dog and evaluates whether the dog is in a calm or stressed state. It sends a notification to the owner when stress is detected.

## Paper
Is available in the root folder: <https://github.com/3dani33/Kamerabasierte_Anwendungen/blob/main/Raab%20Ueltzen%20%26%20Creutzburg%202022%20Monitoring%20Dog%20Movement%20When%20Left%20Alone.pdf>

# Workflow
For developing and improving the algorithm, the following workflow was used:

 1. Change algorithm in algorithm.py
 2. Run algorithm on a video or all videos with run_algorithm.py
 3. Evaluate algorithm with evaluate_algorithm.py and see if result is better than before

# Running the algorithm
For running the algorithm, the module `run_algorithm.py` was created, that has a
commandline interface. Here a version of the commandline interface help is shown:

```
> python3 run_algorithm.py -h
usage: run_algorithm.py [-h] [-s] file

Run the motion detection algorithm on the given file.

	It can show the processing happening live. The current motion detection
	output is shown as a colored circle on top of the video in WHITE (calm) or 
	red (motion detected).
	The output is saved in the folder output.
	The execution can be quit by pressing q, when focusing the output window.

positional arguments:
  file        The video file path to run the algorithm on.

optional arguments:
  -h, --help  show this help message and exit
  -s, --show  Show the algorithm output live
```

For running the algorithm on more than one video file, a Makefile can be used. 
The Makefile can detect all video files and then run the script for each 
video file in the video folder.

When running with the flag `--show`, an overlay is shown for the algorithm 
output and the reference data (if available). It looks like this:

![](img/run_algorithm_ref.png)

The circle in front (WHITE) is the output of the algorithm and the circle half 
shown (red) is the reference. Red means motion and WHITE calm.

# Evaluating the algorithm
The evaluation script is started like this:

```
> python3 evaluate_algorithm.py dummy_v1
```
It takes a string describing the algorithm version and finds the output and 
reference data automatically. The help menu is shown here:
```
> python3 evaluate_algorithm.py -h
usage: evaluate_algorithm.py [-h] algorithm

Evaluate the output of the given algorithm against the reference data.

  Finds the algorithm output data automatically from the output folder and
  loads the corresponding reference data. It outputs the evaluation on the 
  terminal.

  TODO: save the data

positional arguments:
  algorithm   Algorithm name, for example dummy_v1

optional arguments:
  -h, --help  show this help message and exit
```

The output for the dummy_v1 algorithm (never detect motion) for the first video
with annotation:

```
> python3 evaluate_algorithm.py dummy_v1
Algorithm data files found: ['output/John_1-dummy_v1.pkl']
Reference data files found: ['reference/John_1.pkl']
File: John_1
  True positives:   0.0s of 180.0s (0.0%), 0 of 1351 frames.
  False positives:  0.0s (0 frames).
```
