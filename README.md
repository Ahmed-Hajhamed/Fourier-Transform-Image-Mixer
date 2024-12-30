## Fourier Transform Image Mixer
![Python 3 11 12_30_2024 9_11_18 PM](https://github.com/user-attachments/assets/8b1972e3-dbb5-4b61-b948-53d254fb2543)

A Python desktop application that allows users to mix Fourier transform components (magnitude/phase or real/imaginary) components from up to four images into one, offering a powerful tool for creative and technical image manipulation.

---

## Features

- **Fourier Component Mixing**: Mix components (magnitude/phase or real/imaginary) from multiple images.
- **Interactive Image Management**:
  - Double-click to load images.
  - Double right-click to remove images.
- **Fourier Transform Display**: View Fourier transform components of each image based on a combobox selection.
- **Adjustable Weights**: Use sliders to control the weight of each image in the mixing operation.
- **Region Selector**: Select inner (low frequencies) or outer (high frequencies) regions of the Fourier transform for the output.
- **Real-Time Feedback**:
  - Two output viewports to display results.
  - Progress bar indicating the mixing process.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ahmed-Hajhamed/Task-4-DSP
2. Install required dependencies::
  ```bash
  pip install -r requirements.txt
-Usage
Run the application:
    ```bash
    python Main.py

Load images by double-clicking the corresponding labels.
Use the combobox to select Fourier transform components to display.
Adjust sliders to set weights for each image in the mixing operation.
Use the region selector to refine the Fourier component regions.
View the mixed result in the output viewports.
## Requirements
Python: Version 3.8 or higher
## Libraries:
OpenCV (cv2)
PyQt5
QThread
NumPy
## Screenshots
-Double-click to Load and Image and use either Magnitude/Phase or Real/Imaginary Components:
![Python 3 11 12_30_2024 9_18_58 PM](https://github.com/user-attachments/assets/0119b4a4-4137-4b90-9433-b07fb30b87f6)
-Mixing Images using Low Frequency Components:
![Python 3 11 12_30_2024 9_09_57 PM](https://github.com/user-attachments/assets/ac46f140-4164-4fb5-8a8e-3702584066a0)
-Mixing Using High Frequency Components:
![Python 3 11 12_30_2024 9_10_15 PM](https://github.com/user-attachments/assets/6289be71-e8f9-4f34-a41f-aa56f51e6677)
-Mixing can also be done using Real and Imaginary Components:
![Python 3 11 12_30_2024 9_11_32 PM](https://github.com/user-attachments/assets/d129fbc7-bffd-425e-bb3d-6d305699ec27)
-Right Double-click To remove an Image:
![Python 3 11 12_30_2024 9_12_27 PM](https://github.com/user-attachments/assets/6caf66d9-d0b3-4554-b4dd-68ce99e0e5ab)

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## Contact
For questions or issues, please reach out via email: ahmed.hajhamed03@eng-st.cu.edu.eg

Let us know if you'd like any adjustments or additions!
