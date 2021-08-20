# Import the necessary packages and modules.
import os
current_directory = os.getcwd()
module_directory = current_directory.replace('tests', 'Images2Movies')
import sys
sys.path.insert(0, module_directory)
from Images2Movies_module import *

# Test the function 'folder_selection_dialog()'. 
# Function input args: None. 
# Function output 1: When no errors are detected, a statement confirming this is printed. When errors are detected, assertion errors are raised. 
def test_folder_selection_dialog():
    test_directory = folder_selection_dialog(test = 1)
    test_folder = os.path.basename(os.path.normpath(test_directory))
    assert test_folder == 'tests', "Test 1 has failed. The folder selection dialog box did not return the 'tests' folder name'."
    print('Test 1 complete. folder_selection_dialog() is working as expected.\n')

test_folder_selection_dialog()  
    
# Test the function 'rename_images()'.
# Function input arg 1: test_directory [string] --> the test directory. 
# Function output 1: When no errors are detected, a statement confirming this is printed.
def test_rename_images(current_directory):
    well_directory = os.path.join(current_directory, 'test_folder', 'test_village_1', 'Well_1')
    
    # Get the image paths. 
    renamed_images_dir, txt_path = rename_images(well_directory,
                                                 file_type = '.png')
    # Test 2. 
    assert os.path.isdir(renamed_images_dir) == True, "Test 1 has failed. test_rename_images did not create a new folder for the coppied (and renamed) images."
    print('Test 2 complete. rename_images made renamed_images_dir as expected.\n')
    
    # Get the image names in renamed_images_dir. 
    image_names = [_ for _ in os.listdir(renamed_images_dir)]
    true_names = ['0000001.png', '0000002.png', '0000003.png', '0000004.png']
    
    # Test 3.
    assert image_names == true_names, "Test 2 has failed. There are either the wrong number of images in renamed_images_dir, or they are named incorrectly."
    print('Test 3 complete. rename_images copied the right number of images and gave then the right names.\n')
          
    # Test 4.
    assert os.path.exists(txt_path) == True, "Test 3 has failed. The txt file containing the image paths has not been made."
    print('Test 4 complete. rename_images made the txt file (image_paths).\n')
    
    # Test 5. 
    # Read from the .txt file.
    with open(txt_path, 'r') as f:
        content = f.read()
        txt_content = content.split(",")
    f.close()
    truth_txt_content = ["file 'C:\\Users\\Samuel Huguet\\OneDrive\\Documents\\GitHub\\Well-Building-Project-Images2Movies\\tests\\test_folder\\test_village_1\\Well_1\\renamed_images\\0000001.png'\nfile 'C:\\Users\\Samuel Huguet\\OneDrive\\Documents\\GitHub\\Well-Building-Project-Images2Movies\\tests\\test_folder\\test_village_1\\Well_1\\renamed_images\\0000002.png'\nfile 'C:\\Users\\Samuel Huguet\\OneDrive\\Documents\\GitHub\\Well-Building-Project-Images2Movies\\tests\\test_folder\\test_village_1\\Well_1\\renamed_images\\0000003.png'\nfile 'C:\\Users\\Samuel Huguet\\OneDrive\\Documents\\GitHub\\Well-Building-Project-Images2Movies\\tests\\test_folder\\test_village_1\\Well_1\\renamed_images\\0000004.png'\n"]
    assert txt_content == truth_txt_content, "Test 5 has failed, the contents of the image_paths.txt is incorrect."
    print('Test 5 complete. The contents of image_paths.txt is correct.\n')
    
test_rename_images(current_directory)