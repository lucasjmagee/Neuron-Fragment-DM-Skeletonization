# Full Brain Neuron Fragment 2D Discrete Morse Graph Reconstruction Python Package
DiMo2d is a python package meant for executing the discrete Morse graph reconstruction algorithm on the DM++ likelihood outputs of 2D neuron images. The package includes functions which allows users to compute persistence diagrams, generate a discrete Morse graph reconstruction, postprocess the graph reconstruction to capture neuronal fragments, and output the graphs to different formats for each image.

* [Installation Intructions](#installation-instructions)
  * [System Requirements](#system-requirements)
  * [Required Python Libraries](#required-python-libraries)
  * [Compiling Code](#compiling-code)
* [DiMo2D Functions](#dimo2d-functions)

## Installation Instructions
### System Requirements
- Python 3.8.8 (or newer)
- g++ 9.4.0 (or newer)
- cmake 3.16.3 (or newer)

### Required Python Libraries
- cv2 - pip install opencv-python (https://pypi.org/project/opencv-python/)
- PIL - pip install pillow (https://pypi.org/project/Pillow/)
- geojson - pip install geojson (https://pypi.org/project/geojson/)
- vtk - pip install vtk (https://pypi.org/project/vtk/)

### Compiling Code

Dipha Persistence Module

    > cd ./DiMo2d/code/dipha-2d-thresh/
    > mkdir build
    > cd build
    > cmake ../
    > make

Discrete Morse Graph Reconstruction Module

    > cd ./DiMo2d/code/dipha-output-2d-ve-et-thresh/
    > g++ ComputeGraphReconstruction.cpp

## DiMo2d Functions



