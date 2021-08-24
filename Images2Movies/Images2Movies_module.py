from tkinter import *
from tkinter import filedialog
import os as os
from shutil import copyfile
import time as time 
import math
import ffmpeg 
import subprocess
import datetime as dt
import numpy as np

# A function to allow the user to select the folder contianing the subfolders of images.
# Function input arg 1: create_all_videos [bool] --> When 0, asks for the Well diirectory. When 1, asks for the directory containing the village folders.
# Function input arg 2: test [bool] --> When 1, will change the gui title to that of the test gui.
# Function output 1: The path of the folder selected by the user. 
def folder_selection_dialog(create_all_videos = 0,
                            test = 0):
    root = Tk()
    if test:
        root.title('Please select the "Well-Building-Project-Images2Movies\tests" folder within the downloaded package.')
        root.filename = filedialog.askdirectory(initialdir="/", title="Please select the 'Well-Building-Project-Images2Movies\tests' folder within the downloaded package.")
    else:
        if create_all_videos == 0:
            root.title('Please select the well directory for which you want to make a video')
            root.filename = filedialog.askdirectory(initialdir="/", title="Please select the directory containing the subfolders of image data")
        elif create_all_videos == 1:
            root.title('Please select the folder containing the village directories')
            root.filename = filedialog.askdirectory(initialdir="/", title="Please select the directory containing the subfolders of image data")
        else:
            raise Exception("Value of create_all_videos must be 0 or 1, and cannot be int type.")
    selected_directory = root.filename
    root.destroy()

    return selected_directory

# A function to create a list of image paths, such that these images can later be used to make a movie. 
# Function input arg 1: selected_directory [string] --> The directory containing the subfolders of images. 
# Function input arg 2: file_type [string] --> The file extension that you want to detect. 
# Function output 1: renamed_images_dir [string] --> A string of the path of the folder containing the image copies with ffmpeg compatible names.
# Function output 1: txt_path [string] --> A string of the path of txt containing the image paths.
def rename_images(selected_directory,
                  file_type = '.JPG'):
    
    # Create a new folder to store the sequentially named images. 
    renamed_images_dir = os.path.join(selected_directory, 'renamed_images')
    if not os.path.exists(renamed_images_dir):
        os.makedirs(renamed_images_dir)
    
    # First, list the subfolders in the well directory in the correct date order.
    subfolders = [_ for _ in os.listdir(selected_directory) if ('.' not in _) and ('renamed_images' not in _)]
    subfolders_dates = [re.findall(r"\d{8}", _) for _ in subfolders]
    subfolders_dates = [_ for sublist in subfolders_dates for _ in sublist]
    subfolders_dates = [datetime(year=int(_[4:8]), month=int(_[2:4]), day=int(_[0:2])) for _ in subfolders_dates]
    zipped_lists = zip(subfolders_dates, subfolders) 
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    subfolder_dates, subfolders = [list(tuple) for tuple in tuples]
    
    # Create our txt file to store file names. 
    txt_path = os.path.join(selected_directory, "image_paths.txt")
    
    with open(txt_path, 'w') as f:
                            
        # Iterate through the list of subfolders and extract the images contained within them. 
        image_number = 1 
        for i in range(len(subfolders)):

            # Build the path to the DCIM folder for this iteration.
            current_subfolder = subfolders[i]
            subfolder_dir = os.path.join(selected_directory, current_subfolder, 'DCIM')

            # Detect the EK folders which contain the images. 
            EK_folders = [_ for _ in os.listdir(subfolder_dir) if '.' not in _]

            for u in range(len(EK_folders)):

                # Build the path to the current EK folder. 
                current_EK_folder = EK_folders[u]
                EK_folder_dir = os.path.join(subfolder_dir, current_EK_folder)

                # Collect the image paths from that EK folder. 
                images_in_EK_folder = [os.path.join(EK_folder_dir, image) for image in os.listdir(EK_folder_dir) if image.endswith(file_type)]

                # Iterate through each image, copy it to a single folder with ffmpeg-compatible names. 
                for p in range(len(images_in_EK_folder)):

                    # Copy the image to the new dir with the ffmpeg corrected name. 
                    new_image_path = os.path.join(renamed_images_dir, f"{'{0:07}'.format(image_number)}{file_type}")
                    copyfile(images_in_EK_folder[p], new_image_path)
                    image_number += 1
                    
                    # Write our new file path to the txt.
                    f.write(f"file '{new_image_path}'\n")
                            
    # Close our txt file.
    f.close()
                            
    return renamed_images_dir, txt_path

# A function to return the list of well folders, such that images with can later be used to make a movie. 
# Function input arg 1: selected_directory [string] --> The directory containing the well folders of images. 
# Function output 1: well_paths [list] --> A list of the well_folder paths, where each path is a string. 
def list_well_paths(parent_directory):
    
    # First, list the subfolders in the well directory.
    subfolders = [_ for _ in os.listdir(selected_directory) if ('.' not in _) and ('renamed_images' not in _)]

    # Iterate through the list of village_directories and extract the well_directories contained within them. 
    well_paths = []
    for i in range(len(subfolders)):
        
        subfolder_dir = os.path.join(selected_directory, subfolders[i])
        well_directories = [os.path.join(subfolder_dir, _) for _ in os.listdir(subfolder_dir) if ('.' not in _) and ('ignore' not in _)]
        well_paths.append(well_directories)
        
    well_paths = [path for sublist in well_paths for path in sublist]
    
    return well_paths

# A function to take the list of image paths, load in said images, and convert them to a movie. 
# Function input arg 1: selected_directory [string] --> The well or village directory, as previously selected. 
# Function input arg 2: create_all_videos [bool] --> When 0, creates individual videos from the well directory. When 1, considers every well directory and makes videos for all of them.
# Function input arg 3: file_type [string] --> The image file type which is searched for to create the movies.
# Function input arg 4: frame_rate [int] --> Desired frame rate. !!!SET TO 0 IF YOU USE movie_time!!!
# Function input arg 5: movie_time [int] --> Desired movie length (min). !!!SET TO 0 IF YOU USE frame_rate!!!
# Function input arg 6: movie_extension [string] --> Your desired movie file extension. Tested for .avi and .mp4. 
# Function input arg 7: video_width [int] --> The desired video width (the height will be altered proportionally. 
# Function output 1: The movie will be saved to 'selected_directory'. 
def create_movie(selected_directory,
                 create_all_videos = 0,
                 file_type = '.JPG',
                 frame_rate = 0,
                 movie_time = 1,
                 movie_extension = '.mp4',
                 video_width = 2560):
    
    # Create an error to make sure variables are as they should be.
    assert (frame_rate == 0 and movie_time > 0) or (frame_rate > 0 and movie_time == 0), "One of frame_rate and movie_time need to equal 0, which the other needs to be greater than 0."
    
    if create_all_videos == 0:

        # Construct the movie name. 
        path_components = os.path.normpath(selected_directory).split(os.path.sep)
        n = len(path_components)
        movie_name = (f"{path_components[n-2]}_{path_components[n-1]}_fps{frame_rate}_w{video_width}{movie_extension}")

        # Get the image paths. 
        renamed_images_dir, txt_path = rename_images(selected_directory,
                                                     file_type = file_type)
    
        # Change the current working directory to the well folder. 
        os.chdir(selected_directory)

        # Start recording the processing duration.
        t = time.time() 

        # Determine the correct frame rate (or correct sampling of images) to create a video of movie_time in length.         
        if (frame_rate == 0 and movie_time > 0):
            movie_time = movie_time *60 # Convert to seconds. 

            with open(txt_path, 'r') as f:
                nonempty_lines = [line.strip("\n") for line in f if line != "\n"]
                total_frames = len(nonempty_lines)
            f.close()   

            if (total_frames / 50) > movie_time: # Here, we use a frame rate of 50, but simulate a greater frame rate by subsampling images.  
                subsampled_number_frames = 50 * movie_time
                arr = np.arange(total_frames)
                idx = np.round(np.linspace(0, len(arr) - 1, subsampled_number_frames)).astype(int)
                with open(txt_path, 'w') as f:
                    lines = f.readlines()
                    del lines[idx]
                f.close() 
                frame_rate = 50
            else: # Here, we lower the frame rate below 50. 
                time_per_frame = movie_time / total_frames
                frame_rate = 1 / time_per_frame
            
        # Create the video.
        frame_rate = str(frame_rate)
        (ffmpeg
            .input('image_paths.txt', r=frame_rate, f='concat', safe='0')
            .filter('scale', video_width, -1)
            .output(movie_name, vcodec='libx264', pix_fmt='yuv420p')
            .run())
   
        # Remove the image_paths.txt file. 
        os.remove(txt_path)
        shutil.rmtree(renamed_images_dir)
        
        # Calculate the processing duration.
        elapsed = time.time() - t 
        
        # Print the completion statement.
        print(f"------------\nYour video, '{movie_name}' (FPS = {frame_rate}), has been saved to:\n\n{selected_directory}\nTime taken = {elapsed/60} min\n------------\n\n")
        
    if  create_all_videos == 1: 
        
        # Get the well directories. 
        well_paths = list_well_paths(selected_directory)
        
        for v in range(len(well_paths)):
            
            # Construct the movie name. 
            path_components = os.path.normpath(well_paths[v]).split(os.path.sep)
            n = len(path_components)
            movie_name = (f"{path_components[n-2]}_{path_components[n-1]}_fps{frame_rate}_w{video_width}{movie_extension}")
            
            # Get the image paths. 
            renamed_images_dir, txt_path = rename_images(well_paths[v],
                                                         file_type = file_type)

            # Change the current working directory to the well folder. 
            os.chdir(well_paths[v])
            
            # Start recording the processing duration.
            t = time.time() 
            
            # Determine the correct frame rate (or correct sampling of images) to create a video of movie_time in length. 
            if (frame_rate == 0 and movie_time > 0):
                movie_time = movie_time *60 # Convert to seconds. 

                with open(txt_path, 'r') as f:
                    nonempty_lines = [line.strip("\n") for line in f if line != "\n"]
                    total_frames = len(nonempty_lines)
                f.close()   

                if (total_frames / 50) > movie_time: # Here, we use a frame rate of 50, but simulate a greater frame rate by subsampling images.  
                    subsampled_number_frames = 50 * movie_time
                    arr = np.arange(total_frames)
                    idx = np.round(np.linspace(0, len(arr) - 1, subsampled_number_frames)).astype(int)
                    with open(txt_path, 'w') as f:
                        lines = f.readlines()
                        del lines[idx]
                    f.close() 
                    frame_rate = 50
                else: # Here, we lower the frame rate below 50. 
                    time_per_frame = movie_time / total_frames
                    frame_rate = 1 / time_per_frame
            
            # Create the movie.
            frame_rate = str(frame_rate)
            (ffmpeg
                .input('image_paths.txt', r=frame_rate, f='concat', safe='0')
                .filter('scale', video_width, -1)
                .output(movie_name, vcodec='libx264', pix_fmt='yuv420p')
                .run())
            
            # Remove the image_paths.txt file. 
            os.remove(txt_path)
            shutil.rmtree(renamed_images_dir)

            # Calculate the processing duration.
            elapsed = time.time() - t 

            # Print the completion statement.
            print(f"------------\nYour video, '{movie_name}' (FPS = {frame_rate}), has been saved to:\n\n{selected_directory}\nTime taken = {elapsed/60} min\n------------\n\n")