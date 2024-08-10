from email.mime import image
import os
import json
import shutil
from subprocess import PIPE, run
import sys
import datetime

# sort by date created of the photo and create folders based on the month/year they were created


# steps
#   1   go through all the directory paths
#   2   filter for image
#   4   extract modification date 
#   5   organize images based on date for these small subdirectories   
#   6   sort by month
#   7   handle duplicates
#   8   copy them all over and create file directory based off month and year


image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic'}

def find_all_images(source):
    image_paths = []
    
    for root, dirs, files in os.walk(source): 
        for file in files: 
           if any(file.lower().endswith(ext) for ext in image_extensions):
                path = os.path.join(root, file)
                image_paths.append(path)
                
    return image_paths

def get_image_modification_date(image_path):
    mod_time = os.path.getmtime(image_path)
    mod_time_readable = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
    return mod_time_readable

def group_images_by_date(image_paths):
    date_groups = {}
    for path in image_paths:
        mod_date = get_image_modification_date(path)
        date_key = datetime.datetime.strptime(mod_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
        if date_key not in date_groups:
            date_groups[date_key] = []
        date_groups[date_key].append(path)
    return date_groups

def move_images_to_group(image_paths_grouped, target_path):
    for date_group, paths in image_paths_grouped.items():
        group_path = os.path.join(target_path, date_group)
        create_dir(group_path)
        for path in paths:
            shutil.move(path,group_path)

def create_dir(path): 
    if not os.path.exists(path):
        os.mkdir(path)      


def main(source):
    cwd = os.getcwd()  #current working directory
    source_path = os.path.join(cwd, source) # got the source path

    image_paths = find_all_images(source_path) # now have all image paths
    groupofimages = group_images_by_date(image_paths)

    create_dir(source_path) #create a new directory to copy all items
    move_images_to_group(groupofimages,source_path)

    print("Image organization complete.")

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("You must pass the source directory as the only argument.")

    source = args[1]
    main(source)



