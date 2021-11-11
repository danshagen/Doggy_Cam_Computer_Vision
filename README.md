# Project: Doggy Cam
## Project structure
The project has the following folders and files (not complete):
```
.
├── README.md
├── algorithm.py            - implementation of the doggy cam algorithm
├── evaluate_algorithm.py   - script to analyse the algorithm output with the 
│                             reference
├── convert_annotation.py   - convert the video annotation .csv files for the 
│                             evaluate_algorithm script
├── requirements.txt        - specifies the needed python modules for pip
├── Makefile                - Makefile for converting annotations, running the 
│                             algorithm and evaluating the algorithm output
├── video                   - contains the video files, the annotation configuration
│   ├── John_1.json           - video annotation tool project file
│   ├── John_1.mp4            - video file
│   ├── John_2_1.mp4
│   ├── John_2_2.mp4
│   ├── John_3.mp4
│   ├── ...
│   └── Makefile            - Makefile for converting .mov files to .mp4 video
├── output        
│   └── John_1-dummy_v1.pkl - algorithm output with version string
└── reference
    ├── John_1.csv          - video annotation output for video
    └── John_1.pkl          - converted video annotation reference
```

All python modules and scripts are put in the project root folder. The input and output files are in subfolders, as shown above.

