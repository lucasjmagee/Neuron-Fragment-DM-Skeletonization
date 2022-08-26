# Full Brain Neuron Fragment 2D Discrete Morse Graph Reconstruction Python Package
DiMo2d is a python package meant for executing the discrete Morse graph reconstruction algorithm on the DM++ likelihood outputs of 2D neuron images. The package includes functions which allows users to compute persistence diagrams, generate a discrete Morse graph reconstruction, postprocess the graph reconstruction to capture neuronal fragments, and output the graphs to different formats for each image.

* [Introduction](#introduction)
* [Installation Intructions](#installation-instructions)
  * [System Requirements](#system-requirements)
  * [Required Python Libraries](#required-python-libraries)
  * [Compiling Code](#compiling-code)
  * [MATLAB Scripts](#matlab-scripts)
* [DiMo2D Functions](#dimo2d-functions)
* [Separate Programs](#separate-programs)
* [MATLAB Scripts](#matlab-scripts)
* [Example Use of Pipeline](#example-use-of-pipeline)
* [Test Data](#test-data)

## Introduction

DiMo2d is a python package (with underlying matlab functions and c++ libraries) that can be extract in-plane neuronal fragments for process detection outputs of mouse brain image stacks.  There are functions for computing persistence computing persistence diagram for each process detection likelihood output image (required for computing DM graph reconstruction, but could also be of independent interest), computing DM graph reconstruction for image, postprocessing graph of each image to extract fragments, and writing graphs to various formats, such as geojson to be posted to CSHL brain viewer or .vtp format to be visualize by applications such as paraview (https://www.paraview.org/).

DM graph reconstruction is a methodology used to extract true underlying graph structure behind noisy input data. The input for the algorithm is a density function defined on a triangulation, and the output graph is the mountain ridges of the input density function. For mouse brain process detection images, the density function used is simply the pixel values. The mountain ridges of the density function do an excellent job of capturing the neuronal branches in each image. After some postprocessing, the graph is able to extract individual neuron fragments in an image.  Applying to a full mouse brain image stack allows to capture all fragments in mouse brain projected into 2D planes.

This package was designed to be an intergral part of the pipeline to extract individual neurons from sparse mouse brain image stacks (images are very far apart compared to inplane pixels). While the pipeline will output a graph capture all neuronal fragments in each plane, further methodology for tying together fragments across planes is required.

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
    
### MATLAB Scripts

    > cp ./DiMo2d/code/matlab/* ./

## DiMo2d Functions

### DiMo2d.compute_persistence_single_channel(input_dir, output_dir, threads=1)

#### Description

For each likelihood image, compute persistence using DIPHA program. Persistence is only computed on edges with vertice function values greater than 31, DM++ minimum likelihood pixel value

#### Input
- input_dir - Directory containing stack of DM++ likelihood output tifs
- output_dir - Directory where results will be stored.  
- threads - number of threads used to run in parallel

####	Output
Each 2D slice will have its own subdirectory in output_dir named by slice name.  All files required for input be discrete Morse graph reconstruction program will be found in the subdirectories.

#### Example:

    > import DiMo2d as dm
	
    > likelihood_dir = “data/likelihood/”
    > morse_dir = “results/likelihood-morse/”
    > dm.compute_persistence_single_channel(likelihood_dir, morse_dir)
    
![DiMo2d.compute_persistence_single_channel](images/compute-persistence-single-channel.png)

### DiMo2d.generate_morse_graphs(input_path, binary_dir, ve_persistence_threshold=0, et_persistence_threshold=64,  threads=1)

#### Description

Compute discrete Morse graph reconstruction for each 2D slice.  Graphs are intersected with the DM++ binary outputs to remove false positives.

#### Input
- input_path - directory containing results for each slice.  This should be the same as output_dir in a DiMo2d.compute_persistence_single_channel call
binary_dir - path to directory containing the DM++ binary outputs for each slice
- ve_persistence_threshold - negative critical edge persistence threshold
- et_persistence_threshold - positive critical edge persistence threshold.  This must be greater than or equal to ve_persistence_threshold
- threads - number of threads used to run in parallel


#### Output
Morse Graph for each image with specified persistence thresholds

#### Example:

    > import DiMo2d as dm
	
    > likelihood_dir = “data/likelihood/”
    > morse_dir = “results/likelihood-morse/”
    > dm.compute_persistence_single_channel(likelihood_dir, morse_dir)
    > dm.generate_morse_graphs(morse_dir, binary_dir, 0, 64)
    
![DiMo2d.generate_morse_graphs](images/generate-morse-graphs.png)

### DiMo2d.postprocess_graphs(input_path, ve_persistence_threshold=0, et_persistence_threshold=64, threads=1)

#### Description

Apply haircut to remove non-degree 2 paths with a node of degree 1 that change direction at most once

#### Input
- input_path - directory containing results for each slice.  This should be the same as input_path in a DiMo2d.generate_morse_graphs call.
- ve_persistence_threshold - negative critical edge persistence threshold
- et_persistence_threshold - positive critical edge persistence threshold
threads - number of threads used to run in parallel

####	Output
Perform postprocessing of graph at specified thresholds of each image.

#### Example:

    > import DiMo2d as dm
	
    > likelihood_dir = “data/likelihood/”
    > morse_dir = “results/likelihood-morse/”
    > dm.compute_persistence_single_channel(likelihood_dir, morse_dir)
    > dm.generate_morse_graphs(morse_dir, binary_dir, 0, 64)
    > dm.postprocess_graphs(morse_dir, 0, 64)
    
![DiMo2d.postprocess_graphs](images/postprocess-graphs.png)

### DiMo2d.cshl_post_results(input_path, output_dir, ve_persistence_threshold=0, et_persistence_threshold=64, threads=1)

#### Description

Format graphs of each slice to geojson and ready to post to CSHL webviewer

####	Input

- input_path - directory containing results for each slice.  This should be the same as input_path in a previous DiMo2d.postprocess_graphs call.
- output_dir - directory results will be stored
- ve_persistence_threshold - negative critical edge persistence threshold
- et_persistence_threshold - positive critical edge persistence threshold
- threads - number of threads used to run in parallel

####	Output

Geojson ready to be posted to CSHL webviewer is written for each slice

#### Example:
    
    >import DiMo2d as dm

    >likelihood_dir = “data/likelihood/”
    >binary_dir = “data/binary/”
    >morse_dir = “results/likelihood-morse/”
    >json_dir = “results/post_to_web/”
    >dm.compute_persistence_single_channel(likelihood_dir, morse_dir)
    >dm.generate_morse_graphs(morse_dir, binary_dir, 0, 64)
    >dm.postprocess_graphs(morse_dir, 0, 64)
    >dm.cshl_post_results(morse_dir, json_dir, 0, 64)
    
![DiMo2d.cshl_post_results](images/post-results.png)

### DiMo2d.write_vtp_graph(input_dir, output_filename, ve_persistence_threshold=0, et_persistence_threshold=64)

#### Description

Output single vtp file containing morse graphs of all slices

#### Input

- input_dir - directory containing results for each slice.  This should be the same as input_path in a previous DiMo2d.postprocess_graphs call
- output_filename - name of vtp file output will be written to
- ve_persistence_threshold - negative critical edge persistence threshold
- et_persistence_threshold - positive critical edge persistence threshold

#### Output

A single file (output_filename) written in .vtp format containing graphs of each slice

Example:

    >import DiMo2d as dm

    >likelihood_dir = “data/likelihood/”
    >binary_dir = “data/binary/”
    >morse_dir = “results/likelihood-morse/”
    >vtp_filename = “results/full_brain.vtp”
    >dm.compute_persistence_single_channel(likelihood_dir, morse_dir)
    >dm.generate_morse_graphs(morse_dir, binary_dir, 0, 64)
    >dm.postprocess_graphs(morse_dir, 0, 64)
    >dm.write_vtp_graph(morse_dir, vtp_filename, 0, 64)
    

![VTP](images/vtp.png)

## Separate Programs

### Dipha Persistence Program (code/dipha-2d-thresh/build/dipha)

#### Description

Compute persistence diagram of likelihood image (only on regions with greater pixel value than 31, the likelihood minimum).  The program is a modified version of the code found at (https://github.com/DIPHA/dipha).

#### Python Function

DiMo2d.compute_persistence_single_channel

#### Input
- input_filename - path to DIPHA input file
- output_filename - filename for traditional DIPHA program persistence diagram
- edge_filename - filename for edge information - vertices, edge type (negative or positive), and persistence value
- nx - x axis size of image
- ny - y axis size of image

#### Output:

Binary file (edge_filename) contained persistence information for all edges

![DIPHA](images/dipha-2d.png)

### Discrete Morse Graph Reconstruction Program (code/dipha-output-2d-ve-et-thresh/a.out)

#### Description

Executes discrete Morse graph reconstruction algorithm

#### Python Function

DiMo2d.generate_morse_graphs

#### Input

- vert_filename - file contain verts in domain
- dipha_edge_filename - .txt format of edge persistence information
- ve_persistence threshold - persistence threshold for negative edges
- et_persistence threshold - persistence threshold for positive edges
- output_dir - directory where output graph will be written

#### Output

Graph (dimo_vert.txt and dimo_edge.txt) written to output_dir

![DM Graph Reconstruction](images/morse-2d.png)

## MATLAB Scripts

The following matlab scripts were taken from (https://github.com/DIPHA/dipha).

### save_image_data.m

#### Description

Creates DIPHA input file for all likelihood images

#### Python Function

DiMo2d.compute_persistence_single_channel

#### Input

- input_filename - input path to image
- filename - path dipha input file will be written to

#### Output
DIPHA input file for an image

![Save Image Data](images/save-image-data.png)

### load_persistence_diagram.m

#### Description

Converts DIPHA persistence diagram to .txt format for use by Discrete Morse Graph Reconstruction program

#### Python Function
		
DiMo2d.compute_persistence_single_channel

#### Input
- input_filename - Persistence diagram output directly from DIPHA program (.bin format)
- output_filename - filename for .txt format of persistence diagram

#### Output

Persistence Diagram in .txt format for each likelihood image

![Load Persistence Diagram](images/load-persistence-diagram.png)

## Example Use of Pipeline

    > import DiMo2d as dm

    >likelihood_dir = “data/likelihood/”
    >binary_dir = “data/binary/”
    >morse_dir = “results/likelihood-morse/”
    >json_dir = “results/post_to_web/”
    >ve_thresh = 0
    >et_thresh = 64
    >threads = 4
    >dm.compute_persistence_single_channel(likelihood_dir, morse_dir, threads)
    >dm.generate_morse_graphs(morse_dir, binary_dir, 0, 64, threads)
    >dm.postprocess_graphs(morse_dir, 0, 64, threads)
    >dm.cshl_post_results(morse_dir, json_dir, 0, 64, threads)

![Full Workflow](images/2d-full-workflow.png)

## Test Data

Included in the data folder is are two directorys - one containing the likelihood images and the other containing the binary segmentation images of DM++ on two PMD 1229 slice.  Results can be viewed here (http://www.braincircuits.org/viewer4/mouse/map/2293).  The slices included are 0156 and 0156.
