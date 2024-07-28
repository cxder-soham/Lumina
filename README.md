
# Lumina - A Python-based Photoshop lightweight alternative


## Overview

**Lumina** is a Python-based image editing application designed to offer a range of basic image manipulation tools through an intuitive graphical user interface (GUI) built with Tkinter and ttkbootstrap. Lumina is perfect for users seeking a lightweight and accessible tool for everyday image editing tasks without the complexity of professional-grade software.

## Features

### Basic Image Editing

- **Open and Save Images**: Supports opening image files in various formats (JPEG, PNG, BMP) and saving edited images.
- **Crop**: Select and crop a specific area of the image.
- **Resize**: Adjust the dimensions of the image to desired specifications.
- **Rotate**: Rotate images by a specified angle.

### Drawing Tools

- **Brush**: Draw freeform lines with customizable brush size and color.
- **Eraser**: Erase parts of the image with a configurable eraser size.

### Filters and Adjustments

- **Blur**: Apply a Gaussian blur to the image with an adjustable slider for dynamic control.
- **Sharpen**: Enhance the sharpness of the image using a slider for real-time adjustments.
- **Brightness**: Adjust the brightness of the image through a simple input dialog.
- **Contrast**: Modify the contrast of the image via an input dialog for precise control.

### User Interface Enhancements

- **Theme Toggle**: Switch between light and dark themes for a comfortable editing experience in various lighting conditions.
- **Responsive Layout**: The Tkinter canvas dynamically adjusts to window resizing, providing a seamless user experience.

### Performance and Usability

- **Real-Time Updates**: Sliders for blur and sharpen filters provide immediate visual feedback, enhancing the editing workflow.

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
### Download the Executable
 Download the latest version of `Lumina` from the [releases page](https://github.com/cxder-soham/Lumina/releases).
### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cxder-soham/Lumina.git  
   cd Lumina
   ```
2. **Install and Run the Application**
### Install the Required Packages
```bash
pip install -r requirements.txt
```
### Run the Application
```bash
python main.py
```
**Usage**
* **Open an Image**: Use the "File" menu to open an image file.
* **Edit the Image**: Use the tools and filters available in the "Edit" and "Filters" menus to manipulate the image.
* **Save the Image**: Use the "File" menu to save the edited image.
### Toolbar and Menus
* **Tools Menu**: Access drawing tools like Brush and Eraser.
* **Filters Menu**: Apply filters such as Blur, Sharpen, Brightness, and Contrast.
* **View Menu**: Toggle between light and dark themes.
**Building an Executable**
To convert the project into an executable file, use PyInstaller:
1. **Install PyInstaller**:
```bash
pip install pyinstaller
```
2. **Create the Executable**:
```bash
pyinstaller --name PixelPro --onefile --windowed main.py
```
The executable will be located in the `dist` directory.

**Contributing**
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.
**License**
This project is licensed under the MIT License - see the LICENSE file for details.
**Acknowledgements**
* **Python**: The programming language used for this project.
* **Tkinter**: The GUI framework used for building the application interface.
* **Pillow**: The Python Imaging Library used for image processing.
* **ttkbootstrap**: For modern and stylish UI elements.

