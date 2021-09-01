# Import the necessary packages.
from Images2Movies_module import *

# Variables
create_all_videos = 0 # [bool] --> When 0, asks for the Well diirectory. When 1, asks for the directory containing the parents.

# A function to allow the user to select the folder contianing the subfolders of images.
# Function input arg 1: create_all_videos [bool] --> When 0, asks for the Well diirectory. When 1, asks for the parent directory (contains the village folder).
# Function input arg 2: test [bool] --> When 1, will change the gui title to that of the test gui.
# Function output 1: The path of the folder selected by the user. 
folder_selection_dialog(create_all_videos = 0,
                        test = 0)

# A function to organise the creation of movies. 
# Function input arg 1: selected_directory [string] --> The well or village directory, as previously selected. 
# Function input arg 2: create_all_videos [bool] --> When 0, creates individual videos from the well directory. When 1, considers every well directory and makes videos for all of them.
# Function input arg 3: file_type [string] --> The image file type which is searched for to create the movies.
# Function input arg 4: frame_rate [int] --> Desired frame rate. !!!SET TO 0 IF YOU USE movie_time or subsampling_rate!!!
# Function input arg 5: movie_time [int] --> Desired movie length (min). !!!SET TO 0 IF YOU USE frame_rate or subsampling_rate!!!
# Function input arg 6: movie_extension [string] --> Your desired movie file extension. Tested for .avi and .mp4. 
# Function input arg 7: video_width [int] --> The desired video width (the height will be altered proportionally. 
# Function input arg 8: subsampling_rate [float] --> A variable to be used when you want the biggest movie to be of a particular length, and all other videos to be subsampled proportionally. !!!SET TO 0 WHEN USING frame_rate or movie_time!!!. Wen set to above 0, ensure frame_rate=0 and movie_time=0. Calculated with: (50 * desired time for biggest movie in seconds) / number of images in biggest movie.
# Function output 1: The movie will be saved to 'selected_directory'. 
create_movie(selected_directory,
             create_all_videos = 1,
             file_type = '.JPG',
             frame_rate = 0,
             movie_time = 5,
             movie_extension = '.mp4',
             video_width = 1920,
             subsampling_rate = 0)