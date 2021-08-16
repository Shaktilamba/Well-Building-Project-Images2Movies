from tkinter import *
from tkinter import filedialog
import os as os
import cv2
import time as time 
import math

# A function to allow the user to select the folder contianing the subfolders of images.
# Function input arg 1: create_all_videos [bool] --> When 0, asks for the Well diirectory. When 1, asks for the directory containing the parents.
# Function input arg 2: test [bool] --> When 1, will change the gui title to that of the test gui.
# Function output 1: The path of the folder selected by the user. 
def folder_selection_dialog(create_all_videos = 0,
                            test = 0):
    root = Tk()
    if test:
        root.title('Please select the "test" folder within the downloaded package.')
        root.filename = filedialog.askdirectory(initialdir="/", title="Please select the 'test' folder within the downloaded package.")
    else:
        if create_all_videos == 0:
            root.title('Please select the well directory for which you want to make a video')
            root.filename = filedialog.askdirectory(initialdir="/", title="Please select the directory containing the subfolders of image data")
        elif create_all_videos == 1:
            root.title('Please select the folder containing the parent directories')
            root.filename = filedialog.askdirectory(initialdir="/", title="Please select the directory containing the subfolders of image data")
        else:
            raise Exception("Value of create_all_videos must be 0 or 1, and cannot be int type.")
    selected_directory = root.filename
    root.destroy()

    return selected_directory

# A function to create a list of image paths, such that these images can later be used to make a movie. 
# Function input arg 1: selected_directory [string] --> The directory containing the subfolders of images. 
# Function input arg 2: file_type [string] --> The file extension that you want to detect. 
# Function output 1: image_paths [list] --> A list of the image paths, where each path is a string. 
def list_image_paths(selected_directory,
                     file_type = '.jpg'):
    
    # First, list the subfolders in the well directory.
    subfolders = [_ for _ in os.listdir(selected_directory) if '.' not in _]

    # Iterate through the list of subfolders and extract the images contained within them. 
    image_paths = []
    for i in range(len(subfolders)):
        
        current_subfolder = subfolders[i]
        subfolder_dir = os.path.join(selected_directory, current_subfolder, 'DCIM')
        images_in_subfolder = [os.path.join(subfolder_dir, image) for image in os.listdir(subfolder_dir) if image.endswith(file_type)]
        image_paths.append(images_in_subfolder)
        
    image_paths = [image for sublist in image_paths for image in sublist]
    
    return image_paths

# A function to return the list of well folders, such that images with can later be used to make a movie. 
# Function input arg 1: selected_directory [string] --> The directory containing the well folders of images. 
# Function output 1: well_paths [list] --> A list of the well_folder paths, where each path is a string. 
def list_well_paths(selected_directory):
    
    # First, list the subfolders in the well directory.
    subfolders = [_ for _ in os.listdir(selected_directory) if '.' not in _]

    # Iterate through the list of village_directories and extract the well_directories contained within them. 
    well_paths = []
    for i in range(len(subfolders)):
        
        subfolder_dir = os.path.join(selected_directory, subfolders[i])
        well_directories = [os.path.join(subfolder_dir, _) for _ in os.listdir(subfolder_dir) if '.' not in _]
        well_paths.append(well_directories)
        
    well_paths = [path for sublist in well_paths for path in sublist]
    
    return well_paths

# A function to take the list of image paths, load in said images, and convert them to a movie. 
# Function input arg 1: selected_directory [string] --> The well directory, as previously selected. 
# Function input arg 1: create_all_videos [bool] --> When 0, asks for the Well diirectory. When 1, asks for the directory containing the parents.
# Function input arg 3: frame_rate [int] --> The desired frame rate. 
# Function input arg 4: movie_extension [string] --> Your desired movie file extension. Tested for .avi and .mp4. 
# Function input arg 5: movie_resolution [int] --> A percentage value Between 100 and 1. When 100, the original resolution is preserved. When at 50, the width and height will be halved.
# Function output 1: The movie will be saved to 'selected_directory'. 
def create_movie(selected_directory,
                 create_all_videos = 0,
                 file_type = '.jpg',
                 frame_rate = 1,
                 movie_extension = '.avi',
                 movie_resolution = 100):
    
    if create_all_videos == 0:
    
        # Construct the movie name. 
        path_components = os.path.normpath(selected_folder).split(os.path.sep)
        n = len(path_components)
        movie_name = (f"{path_components[n-2]}_{path_components[n-1]}_fps{frame_rate}{movie_extension}")

        # Get the image paths. 
        image_paths = list_image_paths(selected_directory,
                                       file_type = file_type)
    
        # Change the current working directory to the well folder. 
        os.chdir(selected_directory)

        # Create the video. 
        frame = cv2.imread(image_paths[0])
        height, width, layers = frame.shape
        height = math.ceil((height/100)*movie_resolution)
        width = math.ceil((width/100)*movie_resolution)
        video = cv2.VideoWriter(movie_name, 0, frame_rate, (width,height))
        
        # Start recording the processing duration.
        t = time.time() 
        
        for i in range(len(image_paths)):
            t = time.time() # Start recording the processing duration.

            # Print the progress as images are 'stiched' together over time. 
            if i%100 == 0:
                percentage = (i / len(image_paths))*100
                print(f"Progress = {percentage}%")
                
            # Stitch the next image into our video.
            video.write(cv2.imread(image_paths[i]))

        cv2.destroyAllWindows()
        video.release()
        
        elapsed = time.time() - t # Calculate the processing duration.
        print(f"------------\nYour video, '{movie_name}' (FPS = {frame_rate}), has been saved to:\n\n{selected_directory}\nTime taken = {elapsed/60} min\n------------\n\n")
        
    if  create_all_videos == 1: 
        
        # Get the well directories. 
        well_paths = list_well_paths(selected_directory)
        
        for v in range(len(well_paths)):
            
            # Construct the movie name. 
            path_components = os.path.normpath(well_paths[v]).split(os.path.sep)
            n = len(path_components)
            movie_name = (f"{path_components[n-2]}_{path_components[n-1]}_fps{frame_rate}{movie_extension}")
            
            # Get the image paths. 
            image_paths = list_image_paths(well_paths[v],
                                          file_type = file_type)

            # Change the current working directory to the well folder. 
            os.chdir(well_paths[v])

            # Create the video. 
            frame = cv2.imread(image_paths[0])
            height, width, layers = frame.shape
            height = math.ceil((height/100)*movie_resolution)
            width = math.ceil((width/100)*movie_resolution)
            video = cv2.VideoWriter(movie_name, 0, frame_rate, (width,height))

            # Start recording the processing duration.
            t = time.time() 

            for i in range(len(image_paths)):
                t = time.time() # Start recording the processing duration.

                # Print the progress as images are 'stiched' together over time. 
                if i%100 == 0:
                    percentage = (i / len(image_paths))*100
                    print(f"Progress = {percentage}%")
                
                # Stitch the next image into our video.
                video.write(cv2.imread(image_paths[i]))

            cv2.destroyAllWindows()
            video.release()
            
            elapsed = time.time() - t # Calculate the processing duration.
            print(f"------------\nYour video, '{movie_name}' (FPS = {frame_rate}), has been saved to:\n\n{selected_directory}\nTime taken = {elapsed/60} min\n------------\n\n")