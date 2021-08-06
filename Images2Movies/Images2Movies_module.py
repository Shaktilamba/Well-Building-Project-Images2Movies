from tkinter import *
from tkinter import filedialog

# A function to allow the user to select the folder contianing the subfolders of images.
# Function inputs args: test [bool] --> When 1, will change the gui title to that of the test gui. 
# Function output 1: The path of the folder selected by the user. 
def folder_selection_dialog(test = 0):
    root = Tk()
    if test:
        root.title('Please select the "test" folder within the downloaded package.')
        root.filename = filedialog.askdirectory(initialdir="/", title="Please select the "test" folder within the downloaded package.")
    else: 
        root.title('Please select the directory containing the subfolders of image data')
        root.filename = filedialog.askdirectory(initialdir="/", title="Please select the directory containing the subfolders of image data")
    simulation_directory = root.filename
    root.destroy()

    return simulation_directory