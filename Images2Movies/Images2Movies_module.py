from tkinter import *
from tkinter import filedialog
import os as os
from datetime import datetime
import datetime as dt
import shutil
from shutil import copyfile
import time as time 
import math
import ffmpeg 
import subprocess
import numpy as np

# A function to allow the user to select the folder contianing the subfolders of images.
# Function input arg 1: create_all_videos [bool] --> When 0, asks for the Well diirectory. When 1, asks for the parent directory (contains the village folder).
# Function input arg 2: test [bool] --> When 1, will change the gui title to that of the test gui.
# Function output 1: The path of the folder selected by the user. 
def folder_selection_dialog(create_all_videos = 0,
                            test = 0):
    root = Tk()
    if test:
        root.title('Please select the "Well-Building-Project-Images2Movies\\tests" folder within the downloaded package.')
        root.filename = filedialog.askdirectory(initialdir="/", title="Please select the 'Well-Building-Project-Images2Movies\\tests' folder within the downloaded package.")
    else:
        if create_all_videos == 0:
            root.title('Please select the well directory for which you want to make a video.')
            root.filename = filedialog.askdirectory(initialdir="/", title="Please select the well directory for which you want to make a video.")
        elif create_all_videos == 1:
            root.title('Please select the parent directory (the folder containing the village directories).')
            root.filename = filedialog.askdirectory(initialdir="/", title="Please select the parent directory (the folder containing the village directories).")
        else:
            raise Exception("Value of create_all_videos must be 0 or 1, and cannot be int type.")
    selected_directory = root.filename
    root.destroy()

    return selected_directory

selected_directory = folder_selection_dialog()

# A function to create a list of image paths, such that these images can later be used to make a movie. 
# Function input arg 1: selected_directory [string] --> The directory containing the subfolders of images. 
# Function input arg 2: file_type [string] --> The file extension that you want to detect. 
# Function output 1: txt_path [string] --> A string of the path of txt containing the image paths.
def make_image_list(selected_directory,
                    file_type = '.JPG'):
    
    # First, list the subfolders in the well directory in the correct date order.
    subfolders = [_ for _ in os.listdir(selected_directory) if ('.' not in _) and ('renamed_images' not in _) and ('ignore' not in _) and ('Videos' not in _)]
    subfolders_dates = [re.findall(r"\d{8}", _) for _ in subfolders]
    subfolders_dates = [_ for sublist in subfolders_dates for _ in sublist]
    subfolders_dates = [datetime(year=int(_[4:8]), month=int(_[2:4]), day=int(_[0:2])) for _ in subfolders_dates]
    zipped_lists = zip(subfolders_dates, subfolders) 
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    subfolder_dates, subfolders = [list(tuple) for tuple in tuples]
                 
    # Iterate through the list of subfolders and extract the images contained within them. 
    image_list = []
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
            images_in_EK_folder = [os.path.join(EK_folder_dir, image) for image in os.listdir(EK_folder_dir) if image.endswith(file_type) and ('._' not in image)]
            image_list.append(images_in_EK_folder)

    # Flatten list 
    image_list = [item for sublist in image_list for item in sublist]
    
    # Check that files are not corrupted. 
    for i in range(len(image_list)):
        if os.path.getsize(image_list[i]) == 0:
            print(f'This file is 0 bytes and may be corrupted: {image_list[i]}')
    
    return image_list

# A function to create a list of image paths, such that these images can later be used to make a movie. 
# Function input arg 1: selected_directory [string] --> The directory containing the subfolders of images. 
# Function input arg 2: image_list [list] --> List of image paths. 
# Function input arg 3: file_type [string] --> The file extension that you want to detect. 
# Function output 1: renamed_images_dir [string] --> A string of the path of the folder containing the image copies with ffmpeg compatible names.
def rename_images(selected_directory,
                  image_list,
                  file_type = '.JPG'):
    
    # Create a new folder to store the sequentially named images. 
    renamed_images_dir = os.path.join(selected_directory, 'renamed_images')
    if not os.path.exists(renamed_images_dir):
        os.makedirs(renamed_images_dir)
    
    # Iterate through each image path, copy it to a single folder with ffmpeg-compatible names. 
    with open(os.path.join(selected_directory, 'image_paths.txt'), 'w') as f:
        
        image_number = 1 
        for p in range(len(image_list)):

            # Copy the image to the new dir with the ffmpeg corrected name. 
            new_image_path = os.path.join(renamed_images_dir, f"{'{0:07}'.format(image_number)}{file_type}")
            copyfile(image_list[p], new_image_path)
            image_number += 1

            # Write our new file path to the txt.
            f.write(f"file '{new_image_path}'\n")

    # Close our txt file.
    f.close()
                            
    return renamed_images_dir

# A function to return the list of well folders, such that images with can later be used to make a movie. 
# Function input arg 1: selected_directory [string] --> The parent directory containing the vollage folders. 
# Function output 1: well_paths [list] --> A list of the well_folder paths, where each path is a string. 
def list_well_paths(parent_directory):
    
    # First, list the subfolders in the well directory.
    subfolders = [_ for _ in os.listdir(selected_directory) if ('.' not in _) and ('renamed_images' not in _)]

    # Iterate through the list of village_directories and extract the well_directories contained within them. 
    well_paths = []
    for i in range(len(subfolders)):
        
        subfolder_dir = os.path.join(selected_directory, subfolders[i])
        well_directories = [os.path.join(subfolder_dir, _) for _ in os.listdir(subfolder_dir) if ('.' not in _) and ('ignore' not in _) and ('IndexerVolumeGuid' not in _)]
        well_paths.append(well_directories)
        
    well_paths = [path for sublist in well_paths for path in sublist]
    
    return well_paths

# A function to take the list of image paths, load in said images, and convert them to a movie. 
# Function input arg 1: well_directory [string] --> The well directory. 
# Function input arg 2: image_list [list] --> List of image paths to consider. 
# Function input arg 3: frame_rate [int] --> Desired frame rate. !!!SET TO 0 IF YOU USE movie_time!!!
# Function input arg 4: movie_time [int] --> Desired movie length (min). !!!SET TO 0 IF YOU USE frame_rate!!!
# Function input arg 5: movie_extension [string] --> Your desired movie file extension. Tested for .avi and .mp4. 
# Function input arg 6: video_width [int] --> The desired video width (the height will be altered proportionally. 
# Function input arg 8: subsampling_rate [float] --> A variable to be used when you want the biggest movie to be of a particular length, and all other videos to be subsampled proportionally. !!!SET TO 0 WHEN USING frame_rate or movie_time!!!. Wen set to above 0, ensure frame_rate=0 and movie_time=0. Calculated with: (50 * desired time for biggest movie in seconds) / number of images in biggest movie.
# Function output 1: The movie will be saved to 'well_directory'. 
def fmpeg_movie(well_directory,
                image_list,
                frame_rate,
                movie_time,
                movie_extension,
                video_width,
                subsampling_rate):
        
        # Start recording the processing duration.
        t = time.time() 

        # Determine the correct frame rate (or correct sampling of images) to create a video of movie_time in length.         
        if (frame_rate == 0 and movie_time > 0) and subsampling_rate == 0:
            movie_time_sec = movie_time * 60 # Convert to seconds. 
            
            # Construct the movie name. 
            path_components = os.path.normpath(well_directory).split(os.path.sep)
            n = len(path_components)
            movie_name = (f"{path_components[n-2]}_{path_components[n-1]}_fixedLength_w{video_width}{movie_extension}")

            # Get the total number of images. 
            total_frames = len(image_list)

            if (total_frames / 50) > movie_time_sec and subsampling_rate == 0: # Here, we use a frame rate of 50, but simulate a greater frame rate by subsampling images.  
                    subsampled_number_frames = int(50 * movie_time_sec)
                    arr = np.arange(total_frames)
                    idx = np.round(np.linspace(0, (total_frames - 1), subsampled_number_frames)).astype(int)
                    
                    # Remove the image paths we don't need.
                    subsampled_image_paths = [image_list[i] for i in idx]
                    frame_rate = 50
                    
                    # Create our directory of renamed images. 
                    renamed_images_dir = rename_images(well_directory, subsampled_image_paths, file_type = '.JPG')
                    
            else: # Here, we lower the frame rate below 50. 
                time_per_frame = movie_time_sec / total_frames
                frame_rate = 1 / time_per_frame
                
                # Create our directory of renamed images. 
                renamed_images_dir = rename_images(well_directory, image_list, file_type = '.JPG')
                
        elif (frame_rate > 0 and movie_time == 0) and subsampling_rate == 0: # If we're going for a fixed frame_rate. 
            
            # Construct the movie name. 
            path_components = os.path.normpath(well_directory).split(os.path.sep)
            n = len(path_components)
            movie_name = (f"{path_components[n-2]}_{path_components[n-1]}_fps{frame_rate}_w{video_width}{movie_extension}")
            
            # Create our directory of renamed images. 
            renamed_images_dir = rename_images(well_directory, image_list, file_type = '.JPG')
        
        elif (frame_rate == 0 and movie_time == 0) and subsampling_rate > 0: # If we're going for a rate of subsampling equal to the longest video. 

            # Construct the movie name. 
            path_components = os.path.normpath(well_directory).split(os.path.sep)
            n = len(path_components)
            movie_name = (f"{path_components[n-2]}_{path_components[n-1]}_PSR_w{video_width}{movie_extension}") # PSR means 'proportional subsampling rate'. 
            
            subsampled_number_frames = math.floor(subsampling_rate * len(image_list))
            total_frames = len(image_list)
            arr = np.arange(total_frames)
            idx = np.round(np.linspace(0, (total_frames - 1), subsampled_number_frames)).astype(int)

            # Remove the image paths we don't need.
            subsampled_image_paths = [image_list[i] for i in idx]
            frame_rate = 50

            # Create our directory of renamed images. 
            renamed_images_dir = rename_images(well_directory, subsampled_image_paths, file_type = '.JPG')

        # Create the video.
        frame_rate = str(frame_rate)
        (ffmpeg
            .input('image_paths.txt', r=frame_rate, f='concat', safe='0')
            .filter('scale', video_width, -1)
            .output(movie_name, r=frame_rate, vcodec='libx264', pix_fmt='yuv420p') # video_bitrate=1000k
            .run())
   
        # Remove the image_paths.txt file. 
        os.remove('image_paths.txt')
        shutil.rmtree(renamed_images_dir)
        
        # Calculate the processing duration.
        elapsed = time.time() - t 
        
        # Print the completion statement.
        print(f"------------\nYour video, '{movie_name}' (FPS = {frame_rate}), has been saved to:\n\n{well_directory}\nTime taken = {elapsed/60} min\n------------\n\n")

# A function to organise the creation of movies. 
# Function input arg 1: selected_directory [string] --> The well or village directory, as previously selected. 
# Function input arg 2: create_all_videos [bool] --> When 0, creates individual videos from the well directory. When 1, considers every well directory and makes videos for all of them.
# Function input arg 3: file_type [string] --> The image file type which is searched for to create the movies.
# Function input arg 4: frame_rate [int] --> Desired frame rate. !!!SET TO 0 IF YOU USE movie_time!!!
# Function input arg 5: movie_time [int] --> Desired movie length (min). !!!SET TO 0 IF YOU USE frame_rate!!!
# Function input arg 6: movie_extension [string] --> Your desired movie file extension. Tested for .avi and .mp4. 
# Function input arg 7: video_width [int] --> The desired video width (the height will be altered proportionally. 
# Function input arg 8: subsampling_rate [float] --> A variable to be used when you want the biggest movie to be of a particular length, and all other videos to be subsampled proportionally. !!!SET TO 0 WHEN USING frame_rate or movie_time!!!. Wen set to above 0, ensure frame_rate=0 and movie_time=0. Calculated with: (50 * desired time for biggest movie in seconds) / number of images in biggest movie.
# Function output 1: The movie will be saved to 'selected_directory'. 
def create_movie(selected_directory,
                 create_all_videos = 1,
                 file_type = '.JPG',
                 frame_rate = 0,
                 movie_time = 5,
                 movie_extension = '.mp4',
                 video_width = 1920,
                 subsampling_rate = 0):
    
    # Create an error to make sure variables are as they should be.
    assert (frame_rate == 0 and movie_time == 0 and subsampling_rate > 0) or (frame_rate == 0 and movie_time > 0 and subsampling_rate == 0) or (frame_rate > 0 and movie_time == 0 and subsampling_rate == 0), "Of frame_rate, movie_time and subsampling_rate, only one can be greater than 0."
    
    if create_all_videos == 0:

        # Get the image paths. 
        image_list = make_image_list(selected_directory, file_type = file_type)
    
        # Change the current working directory to the well folder. 
        os.chdir(selected_directory)

        # Make the movie. 
        fmpeg_movie(selected_directory,
                    image_list,
                    frame_rate,
                    movie_time,
                    movie_extension,
                    video_width,
                    subsampling_rate)
        
    if  create_all_videos == 1: 
        
        # Get the well directories. 
        well_paths = list_well_paths(selected_directory)
        
        for v in range(len(well_paths)):

            # Get the image paths. 
            image_list = make_image_list(well_paths[v], file_type = file_type)

            # Change the current working directory to the well folder. 
            os.chdir(well_paths[v])
           
            # Make the movie. 
            fmpeg_movie(well_paths[v],
                        image_list,
                        frame_rate,
                        movie_time,
                        movie_extension,
                        video_width,
                        subsampling_rate)