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

<figure>
    <img src="https://github.com/SamHSoftware/Well-Building-Project-Images2Movies/blob/main/img/file_structure.png?raw=true" alt="The heirarchy of folders needed for the code to work" width="700"/>  
    <figcaption>Fig.1 - The heirarchy of folders needed for the code to work.</figcaption>
</figure>
<br>
- It does not matter what the parent directories, wells or image folders are called, *providing* that they order correctly when you observe the folders when sorting by name. 
- The DCIM folders *must* be named 'DCIM'. 
- Your images can be ```.jpg``` or ```.png```. You will simply need to chnage a input arg in the code (explained below). 

## If you want, you can test that the code works before using it:
It is often common practice to test that functions are working as exected. This is because software changes over time, and commands which might have done one thing, might be edited and to do another several years later. Thus, I have included additional 'test' code which checks that the primary functions are working as ecpected. Here's how to use the 'test' code:  

(1) Within the ```tests``` folder, open ```test_Images2Movies_module.ipynb```. You can use the ```.py``` file instead if you'd like to.

(2) Run ```test_Images2Movies_module.ipynb```. A popup dialog box will appear (see example below), with which you should select the following folder: ```\Well-Building-Project-Images2Movies\tests\test_parent_dir\Well_1```. The script will consider each of the primary functions, and will check that they output the expected values. If assertion errors are raised, then you will need to debug the code, and may contact me for help. 

<figure>
    <img src="https://github.com/SamHSoftware/Well-Building-Project-Images2Movies/blob/main/img/folder_selection.PNG?raw=true" alt="A folder selection dialog box" width="500"/>
    <figcaption>Fig.2 - A folder selection dialog box.</figcaption>
</figure>
<br>
## How to use the code: 

(1) Open the ```RUNME.ipynb``` script. By highlighting individual functions, you will be able to run the code sequentially. This is what we're going to do now. 

(2) First, select and run the following code: 
```
# Import the necessary packages.
from Images2Movies_module import *
```

This line imports the functions I wrote for this application. You can think of it as loading up the scientific protocols for an experiment. 

(3) Select and run the following code (you do not need to change any of the input args): 
```
# A function to allow the user to select the folder contianing the subfolders of images.
# Function inputs args: test [bool] --> When 1, will change the gui title to that of the test gui. 
# Function output 1: The path of the folder selected by the user. 
well_directory = folder_selection_dialog(test = 0)
```

A popup dialog box will appear (see Fig.2). With this, you need to select the ```well_folder``` for which you want to create videos. The ```well_folders``` can be seen in Fig.1 as ```Well_1``` and ```Well_n```. 

(4) Select and run the following code: 
```
# A function to create a list of image paths, such that these images can later be used to make a movie. 
# Function input args: well_directory [string] --> The directory containing the subfolders of images. 
# Function output arg 1: image_paths [list] --> A list of the image paths, where each path is a string. 
image_paths = list_image_paths(well_directory)
```
This will fetch all the image paths to be used to make the video. 

(5) Finally, select and run the final function:
```
# A function to take the list of image paths, load in said images, and convert them to a movie. 
# Function input arg 1:image_paths [list] --> A list of string directories for each image to be stiched into the video. The list represents the correct order of stiching.
# Function input arg 2: well_directory [string] --> The well directory, as previously selected. 
# Function input arg 3: frame_rate [int] --> The desired frame rate. 
# Function input arg 4: movie_name [string] --> Your desired file name, including the file extension. Tested for .avi and .mp4. 
# Function output 1: The movie will be saved to 'well_directory'. 
create_movie(image_paths = image_paths,
             well_directory = well_directory,
             frame_rate = 1,
             movie_name = 'my_movie_name.avi'):
```

You will notice that there are four input args. You don't need to change the first two. However, you can alter the frame rate, video name, and video file type in the final two functions.  

The video will be saved to your well directory. 