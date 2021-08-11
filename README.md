# README for package: Well-Building-Project-Images2Movies

## Author details: 
Name: Sam Huguet  
E-mail: samhuguet1@gmail.com  
Date created: 11<sup>th</sup> August 2021

## Description: 
- This code has been deisgned to consider several directories full of images, then 'stitch' them together to create a video. 
- This code was written for Dr. Shakti Lamba, to help process image data captured as part of the [well building project](http://shaktilamba.com/research-2/well-building-project/).
- At this time of writing, Dr. Lamba is a researcher at The University of Exeter, Penryn campus. Her interest lies in "how people cooperate to solve public goods dilemmas", and in how this cooperation has evolved. 
- The video output of this code is

## Software requirements to run the code: 
- You can run this code on your own computer for free, providing you download and install the following software:  
(1) Anaconda: This is an immensely useful platform from which you can download the correct version of many languages with their respective packages. Anaconda also allows you to create specific environments for specific projects. You can manage packages and environments outside of Anaconda should you wish.  
(2) Python 3.7. This can be installed through Anaconda.  
(3) An IDE (Integrated development environment). This is the software which allows you to easily interact with the code. I would recommend JupyterLab, for which I have included many ```.ipynb``` files. JupyterLab can be installed through Anaconda.   
(4) The packages required to create the correct environment. The package list will be stored in XXX.   

## The code expects your data to be organised in the following way: 
- This code expects there to be multiple 'parent' folders (a.k.a. directories), each of which contains the images for an individual village. Within this parent directory, there needs to be a specific hierarchy of folders. 
- This image gives a visual explanation of how to organise the data:

<img src="https://github.com/SamHSoftware/Well-Building-Project-Images2Movies/blob/main/img/file_structure.png?raw=true" alt="The heirarchy of folders needed for the code to work" width="500"/>  

- It does not matter what the parent directories, wells or image folders are called, *providing* that they order correctly when you observe the folders when sorting by name. 
- The DCIM folders *must* be named 'DCIM'. 
- Your images can be ```.jpg``` or ```.png```. You will simply need to chnage a input arg in the code (explained below). 

## 

## How to use the code: 

(1) Open the ```create_histogram.R``` script. 
