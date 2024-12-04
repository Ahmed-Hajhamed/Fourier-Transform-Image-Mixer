import cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog

class Image:
    def __init__(self):
        super().__init__()
        self.image = None
        self.path = None
        self.contrast = 1.0
        self.brightness = 0

    def load_image(self):
        """"Load Image and get Magnitude, Phase, Real and Imaginary parts of the Image FT"""
        self.path, _ = QFileDialog.getOpenFileName(
            None, 
            "Open File", 
            "", 
            "All Files (*.*);;Text Files (*.txt);;Images (*.png *.jpg)"
        )
        # self.path = ""
        
        self.image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

        # Normalize to [0, 1]
        # max_pixel_value = self.image.max() 
        # self.image = self.image / max_pixel_value

        self.ft = np.fft.fft2(self.image)
        # Shift the zero-frequency component to the center for better visualization
        self.ft_shifted = np.fft.fftshift(self.ft)

        self.magnitude_spectrum = np.abs(self.ft_shifted)
        self.magnitude_log = np.log1p(self.magnitude_spectrum)  # Use log for better visualization
        self.phase_spectrum = np.angle(self.ft_shifted)
        self.real_component = np.real(self.ft_shifted)
        self.imaginary_component = np.imag(self.ft_shifted)

    def resize_image(self, width, height):
        self.image = cv2.resize(self.image, (width, height))

    def adjust_brightness_contrast(self):
        self.image= cv2.convertScaleAbs(self.image, alpha=self.constrast, beta=self.brightness)  # Contrast (1.0 means no change)
                                                                                     # Brightness (0 means no change)

    def modify_magnitude(self, gain):
        self.magnitude_spectrum= self.magnitude_spectrum * gain 
        self.ft_shifted = self.magnitude_spectrum * np.exp(1j * self.phase_spectrum)

    def modify_phase(self, angle_in_degrees):
        shift_in_rad = angle_in_degrees * np.pi / 180.0
        self.phase_spectrum = self.phase_spectrum + shift_in_rad 
        self.ft_shifted = self.magnitude_spectrum * np.exp(1j * self.phase_spectrum)

    def modify_real_parts(self, gain):
        self.real_component *= gain
        self.ft_shifted = self.real_component + 1j * self.imaginary_component

    def modify_imaginary_parts(self, gain):
        self.imaginary_component *= gain
        self.ft_shifted = self.real_component + 1j * self.imaginary_component

    def modify_selected_part(compoent_to_modify, selected_row, selected_coloumn, gain, phase_to_modify = None):
        if phase_to_modify is None:
            row_start, row_end = selected_row[0], selected_row[-1]
            col_start, col_end = selected_coloumn[0], selected_coloumn[-1]

            compoent_to_modify[row_start:row_end, col_start:col_end] *= gain 
        else:
            angle_in_rad = gain * np.pi / 180.0
            phase_to_modify[row_start:row_end, col_start:col_end] += angle_in_rad

    def modify_low_frequencies(compoent_to_modify, gain, phase_to_modify = None):
        rows, cols = compoent_to_modify.shape
        center_x, center_y = rows // 2, cols // 2
        radius = 30 
        # Create a mask for high frequencies
        y, x = np.ogrid[:rows, :cols]
        mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2

        if phase_to_modify is None:
            compoent_to_modify[mask] *= gain  
        else:
            shift_in_rad = gain * np.pi / 180.0
            phase_to_modify[mask] += shift_in_rad


    def modify_high_frequencies(compoent_to_modify, gain, phase_to_modify = None):
        rows, cols = compoent_to_modify.shape
        center_x, center_y = rows // 2, cols // 2
        radius = 30 
        # Create a mask for high frequencies
        y, x = np.ogrid[:rows, :cols]
        mask = (x - center_x)**2 + (y - center_y)**2 >= radius**2

        if phase_to_modify is None:
            compoent_to_modify[mask] *= gain  

        else:
            shift_in_rad = gain * np.pi / 180.0
            phase_to_modify[mask] += shift_in_rad

    def reconstruct_image(self):
        ft_inverse_shift = np.fft.ifftshift(self.ft_shifted)

        self.reconstructed_image = np.fft.ifft2(ft_inverse_shift)
        self.reconstructed_image = np.abs(self.reconstructed_image)
        # self.reconstructed_image = np.clip(self.reconstructed_image, 0, 1)
        