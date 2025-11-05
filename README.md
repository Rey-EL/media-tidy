# MediaTidy

## Overview

MediaTidy is a powerful Python utility script designed to bring order to even the most chaotic media libraries. It automates the process of organizing your photos and videos by scanning a designated folder, intelligently renaming files, and moving them into a clean, standardized directory structure.

## Features

*   **Smart Date Recognition**: Utilizes EXIF metadata from photos (via the Pillow library) to accurately determine the "Date Taken." If EXIF data is unavailable, it gracefully falls back to using the file's last modification time.
*   **Organizes by Type**: Automatically creates dedicated `Images` and `Videos` folders at the root of your media library, ensuring clear separation and easy access.
*   **Automatic Renaming**: Renames all media files to a consistent and readable format: `YYYY-MM-DD_HH-MM-SS`.
*   **Collision Handling**: Prevents accidental overwrites by intelligently appending a counter (e.g., `... (1)`, `... (2)`) to filenames if a duplicate name is encountered.
*   **Recursive Cleanup**: After all media files have been processed and moved, the script performs a thorough scan to identify and delete any empty subfolders left behind, maintaining a tidy directory structure.
*   **User-Friendly Interface**: Integrates `tkinter` for an intuitive graphical folder selection dialog, making it easy to choose your media library.
*   **Live Progress Tracking**: Incorporates `tqdm` to display a real-time progress bar, keeping you informed during the organization process.

## Deployment / Executable

This repository includes a `MediaTidy.spec` file, which serves as a "recipe" for PyInstaller. PyInstaller compiles the Python script into a standalone `MediaTidy.exe` for Windows. This allows the tool to be run on any Windows machine, even those without Python installed. The final `.exe` executable is generated in the `dist` folder after running PyInstaller.

## How to Use (Script)

1.  **Run the script**: Open your terminal or command prompt, navigate to the project directory, and execute the script using Python:
    ```bash
    python3 MediaTidy.py
    ```
2.  **Select Folder**: A graphical dialog box will appear. Use it to select the main media library folder you wish to organize.
3.  **Process**: The script will then automatically scan, move, rename, and clean up your entire media library, providing a progress bar for visibility.