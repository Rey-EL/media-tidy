# media-tidy

MediaTidy is a Python utility script that brings order to chaotic photo and video libraries. It automates the process of organizing your media by scanning a folder, intelligently renaming files based on their metadata, and moving them into a clean, standardized `Images` and `Videos` directory structure.

---

## Key Features

*   **Smart Date Recognition**: Uses EXIF metadata from photos (via the Pillow library) to find the exact "Date Taken." If EXIF data is missing, it falls back to the file's last modification time.
*   **Organizes by Type**: Automatically creates and sorts files into `Images` and `Videos` folders within your selected library.
*   **Standardized Renaming**: Renames all media files to a consistent `YYYY-MM-DD_HH-MM-SS` format for easy chronological sorting.
*   **Collision Handling**: If a file with the same name already exists, it intelligently appends a counter (e.g., `... (1)`, `... (2)`) to prevent accidental overwrites.
*   **Recursive Cleanup**: After organizing all media, the script performs a final pass to find and delete any empty subfolders left behind.
*   **User-Friendly Interface:**
    *   Integrates `tkinter` for a simple graphical dialog to select your media library.
    *   Displays a `tqdm` progress bar to show live progress during the organization process.

---

## Security Considerations

MediaTidy is a local utility script and does not interact with networks or external services, which means it is not directly susceptible to many common web-based vulnerabilities like those in the OWASP Top 10. However, users should always:

*   **Backup Important Data:** Before running any file management utility, ensure critical media files are backed up.
*   **Understand File Operations:** Be aware of the files being processed and how they are being renamed and moved.
*   **Keep System Updated:** Ensure your operating system and Python environment are kept up-to-date with the latest security patches.

---

## Installation & Setup

To use MediaTidy, you need Python 3.

1.  **Navigate to the project directory:**
    ```bash
    cd media-tidy
    ```

2.  **Install dependencies:**
    It's highly recommended to use a virtual environment.
    ```bash
    # Create and activate a virtual environment (optional but recommended)
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install the required packages
    pip install -r requirements.txt
    ```

---

## Usage

1.  **Run the script from your terminal:**
    ```bash
    python3 media_tidy.py
    ```

2.  **Select Your Media Library:** A graphical dialog box will appear. Navigate to and select the root folder of your photo/video library.

3.  **Let it Run:** The script will automatically scan for all media files, organize them into the `Images` and `Videos` subdirectories, and clean up empty folders. You can monitor the progress in the terminal.

---

## Creating a Standalone Executable (Optional)

You can bundle this script and its dependencies into a single standalone `.exe` file for Windows using **PyInstaller**. This allows the script to be run on machines that do not have Python installed.

To build the executable:

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the build command from the project directory:**
    This command will create a `.spec` file and a `dist` folder containing the final `MediaTidy.exe`.
    ```bash
    pyinstaller --onefile --windowed media_tidy.py
    ```

3.  The final `media_tidy.exe` will be located in the `dist` folder.

---

## License

This project is licensed under the [MIT License](./LICENSE.md) - see the LICENSE.md file for details.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements, bug reports, or want to add new features, please feel free to open an issue or submit a pull request.
