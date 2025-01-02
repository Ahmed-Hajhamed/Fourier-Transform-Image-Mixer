from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np


class ImageMixingWorker(QThread):
    progress = pyqtSignal(int)  
    result_ready = pyqtSignal(np.ndarray)

    def __init__(self, image_labels, reconstruction_pair, band_mask):
        super().__init__()
        self.image_labels = image_labels
        self.reconstruction_pair = reconstruction_pair
        self.band_mask = band_mask
        self.is_canceled = False 
        self.log_scaled_output = False 

        self.number_of_images = 0.0
        for image_label in self.image_labels:
            if image_label.image.image is not None:
                self.number_of_images += 1.0

        self.magnitude_spectrum = np.zeros_like(self.image_labels[0].image.magnitude_spectrum, dtype=np.float64)
        self.phase_spectrum_real = np.zeros_like(self.image_labels[0].image.phase_spectrum, dtype=np.float64)
        self.phase_spectrum_imaginary = np.zeros_like(self.image_labels[0].image.phase_spectrum, dtype=np.float64)
        self.real_component = np.zeros_like(self.image_labels[0].image.real_component, dtype=np.float64)
        self.imaginary_component = np.zeros_like(self.image_labels[0].image.imaginary_component, dtype=np.float64)

    def run(self):
        if self.reconstruction_pair == "Magnitude and Phase":
            for idx, image_label in enumerate(self.image_labels):
                if self.is_canceled:
                    return  
                if image_label.image.image is None:
                    continue

                if image_label.ft_combobox.currentText() == "Magnitude":
                    self.magnitude_spectrum +=  (image_label.image.magnitude_spectrum\
                                                            * image_label.weight_slider.value() / 100)
                    
                elif image_label.ft_combobox.currentText() == "Phase":
                    weight =  image_label.weight_slider.value() / (100.0 * self.number_of_images)
                    self.phase_spectrum_real += weight * np.cos(image_label.image.phase_spectrum)
                    self.phase_spectrum_imaginary += weight * np.sin(image_label.image.phase_spectrum)

                self.progress.emit((idx + 1) * 100 // (self.number_of_images + 1))

            self.phase_spectrum = np.arctan2(self.phase_spectrum_imaginary, self.phase_spectrum_real)
            self.log_scaled_output = not np.any(self.phase_spectrum)

            if not np.any(self.magnitude_spectrum): 
                self.magnitude_spectrum = np.ones_like(self.image_labels[0].image.magnitude_spectrum, dtype=np.float64)\
                                                                * self.number_of_images
            ft_shifted = (self.magnitude_spectrum / self.number_of_images) * np.exp(1j * self.phase_spectrum)

        elif self.reconstruction_pair == "Real and Imaginary":
            for idx, image_label in enumerate(self.image_labels):
                if self.is_canceled:
                    return  
                if image_label.image.image is None:
                    continue

                if image_label.ft_combobox.currentText() == "Real":
                    self.real_component+= (image_label.image.real_component\
                                                            * image_label.weight_slider.value() / 100)
                    
                elif image_label.ft_combobox.currentText() == "Imaginary":
                    self.imaginary_component += (image_label.image.imaginary_component\
                                                            * image_label.weight_slider.value() / 100)
                    
                self.progress.emit((idx + 1) * 100 // (self.number_of_images + 1))
                
            ft_shifted = (self.real_component / self.number_of_images) + 1j * (self.imaginary_component / self.number_of_images)
    
        if self.band_mask is not None:
            ft_shifted = ft_shifted * self.band_mask

        ft_inverse_shift = np.fft.ifftshift(ft_shifted)
        mixed_image = np.fft.ifft2(ft_inverse_shift)
        mixed_image = np.abs(mixed_image)
        self.progress.emit(100)

        if self.log_scaled_output:
            self.result_ready.emit(np.log1p(mixed_image))
        else:
            self.result_ready.emit(mixed_image)

    def cancel(self):
        self.is_canceled = True
