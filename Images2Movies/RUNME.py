# Import the necessary packages.
from Images2Movies_module import *

# Variables
create_all_videos = 0 #[bool] --> When 0, asks for the Well diirectory. When 1, asks for the directory containing the parents.

# A function to allow the user to select the folder contianing the subfolders of images.
# Function input arg 1: create_all_videos [bool] --> When 0, asks for the Well diirectory. When 1, asks for the directory containing the parents.
# Function input arg 2: test [bool] --> When 1, will change the gui title to that of the test gui.
# Function output 1: The path of the folder selected by the user. 
folder_selection_dialog(create_all_videos = create_all_videos,
                        test = 0)

# A function to take the list of image paths, load in said images, and convert them to a movie. 
# Function input arg 1: selected_directory [string] --> The well or village directory, as previously selected. 
# Function input arg 2: create_all_videos [bool] --> When 0, creates individual videos from the well directory. When 1, considers every well directory and makes videos for all of them.
# Function input arg 3: file_type [string] --> The image file type which is searched for to create the movies.
# Function input arg 4: frame_rate [int] --> Desired frame rate. !!!SET TO 0 IF YOU USE movie_time!!!
# Function input arg 5: movie_time [int] --> Desired movie length (min). !!!SET TO 0 IF YOU USE frame_rate!!!
# Function input arg 6: movie_extension [string] --> Your desired movie file extension. Tested for .avi and .mp4. 
# Function input arg 7: video_width [int] --> The desired video width (the height will be altered proportionally. 
# Function output 1: The movie will be saved to 'selected_directory'. 
create_movie(selected_directory,
             create_all_videos = 0,
             file_type = '.JPG',
             frame_rate = 0,
             movie_time = 1,
             movie_extension = '.mp4',
             video_width = 2560)