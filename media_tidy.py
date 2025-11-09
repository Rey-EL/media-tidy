# Copyright (c) 2025 Elvis Reyes
#
# This software is licensed under the MIT License.
# See the LICENSE.md file in the project root for full license terms.

import os
import shutil
import tkinter as tk
from tkinter import filedialog
import re
from PIL import Image
from datetime import datetime
from tqdm import tqdm

# --- Configuration ---
IMAGE_EXTENSIONS = (
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif',
    '.arw', '.cr2', '.cr3', '.nef', '.orf', '.rw2', '.dng', '.pef', '.srw',
    '.psd', '.svg', '.ico'
)
VIDEO_EXTENSIONS = (
    '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.mts', '.m2ts',
    '.webm', '.flv', '.3gp', '.mpg', '.mpeg', '.vob'
)
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS

def get_date_taken(file_path):
    """Tries to get the 'Date Taken' from a photo's EXIF metadata."""
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:
                date_str = exif_data[36867]
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception:
        return None
    return None

def get_file_date(file_path):
    """Gets the best possible date for a file, falling back to modification time."""
    if file_path.lower().endswith(IMAGE_EXTENSIONS):
        date = get_date_taken(file_path)
        if date:
            return date
    mod_time = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mod_time)

def process_media_file(file_path, destination_folder, date_info):
    """
    Renames the file by date and moves it into the final destination folder.
    """
    _, original_ext = os.path.splitext(os.path.basename(file_path))
    new_name = date_info.strftime('%Y-%m-%d_%H-%M-%S')
    dest_path = os.path.join(destination_folder, f"{new_name}{original_ext}")
    
    counter = 1
    while os.path.exists(dest_path):
        new_name_with_counter = f"{new_name} ({counter})"
        dest_path = os.path.join(destination_folder, f"{new_name_with_counter}{original_ext}")
        counter += 1

    shutil.move(file_path, dest_path)
    print(f"  -> Renamed & Moved to: {os.path.basename(destination_folder)}")

def cleanup_empty_folders(folder_to_clean, protected_folders):
    """Deletes ALL empty subdirectories within a given folder, ignoring protected ones."""
    print("\n--- Cleaning up all empty folders ---")
    for dirpath, dirnames, filenames in os.walk(folder_to_clean, topdown=False):
        # Do not delete the main protected folders, even if they start empty
        if os.path.normcase(dirpath) in protected_folders:
            continue
        if not filenames and not dirnames:
            try:
                os.rmdir(dirpath)
                print(f"  🗑️ Deleted empty folder: {dirpath}")
            except OSError as e:
                print(f"  ⚠️ Error deleting folder {dirpath}: {e}")

def main():
    """Main function to organize a single media library in-place."""
    root = tk.Tk()
    root.withdraw()

    print("Please select your main Media Library folder to organize.")
    library_folder = filedialog.askdirectory(title="Select Media Library to Organize")
    if not library_folder: return
        
    print("-" * 30)
    print(f"✅ Organizing Library: {library_folder}")
    print("-" * 30)
    
    images_root_folder = os.path.join(library_folder, 'Images')
    videos_root_folder = os.path.join(library_folder, 'Videos')
    os.makedirs(images_root_folder, exist_ok=True)
    os.makedirs(videos_root_folder, exist_ok=True)
    
    # --- Pass 1: Find all misplaced media files ---
    print("\nPre-scanning to find misplaced files...")
    files_to_process = []
    
    # Normalize paths for reliable comparison
    protected_paths = {os.path.normcase(images_root_folder), os.path.normcase(videos_root_folder)}

    for current_folder, dirnames, file_names in os.walk(library_folder):
        # UPDATED RULE: Smartly skip the final destination folders
        dirnames[:] = [d for d in dirnames if os.path.normcase(os.path.join(current_folder, d)) not in protected_paths]

        for file_name in file_names:
            if file_name.lower().endswith(MEDIA_EXTENSIONS):
                files_to_process.append(os.path.join(current_folder, file_name))

    if not files_to_process:
        print("\n✅ Library is already perfectly organized. No files to move.")
    else:
        # --- Pass 2: Process the misplaced files with a progress bar ---
        print(f"\nFound {len(files_to_process)} misplaced files. Starting organization...")
        for file_path in tqdm(files_to_process, desc="Organizing Media", unit="file"):
            date_to_use = get_file_date(file_path)
            file_name = os.path.basename(file_path)
            
            if file_name.lower().endswith(IMAGE_EXTENSIONS):
                process_media_file(file_path, images_root_folder, date_to_use)
            elif file_name.lower().endswith(VIDEO_EXTENSIONS):
                process_media_file(file_path, videos_root_folder, date_to_use)

    # After everything has been moved, run the full cleanup process
    cleanup_empty_folders(library_folder, protected_paths)
    print("\n\nMission accomplished! Your media library is organized. 🎉")

if __name__ == "__main__":
    main()
