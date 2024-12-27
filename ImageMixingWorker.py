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

    def run(self):
        num_images = len(self.image_labels)
        magnitude_spectrum = np.zeros_like(self.image_labels[0].image.magnitude_spectrum, dtype=np.float64)
        phase_spectrum_real = np.zeros_like(self.image_labels[0].image.phase_spectrum, dtype=np.float64)
        phase_spectrum_imag = np.zeros_like(self.image_labels[0].image.phase_spectrum, dtype=np.float64)
        real_component = np.zeros_like(self.image_labels[0].image.real_component, dtype=np.float64)
        imaginary_component = np.zeros_like(self.image_labels[0].image.imaginary_component, dtype=np.float64)

        if self.reconstruction_pair == "Magnitude and Phase" and self.band_mask is not None:
            for idx, image in enumerate(self.image_labels):
                if self.is_canceled:
                    return  

                magnitude_spectrum[self.band_mask] +=  image.image.magnitude_spectrum[self.band_mask]

                weight = 0.25
                phase_spectrum_real[self.band_mask] += weight * np.cos(image.image.phase_spectrum[self.band_mask])
                phase_spectrum_imag[self.band_mask] += weight * np.sin(image.image.phase_spectrum[self.band_mask])
                self.progress.emit((idx + 1) * 100 // num_images)

            phase_spectrum = np.arctan2(phase_spectrum_imag, phase_spectrum_real)
            masked_magnitude_spectrum = magnitude_spectrum * self.band_mask 
            masked_phase_spectrum = phase_spectrum * self.band_mask
            ft_shifted = (masked_magnitude_spectrum / num_images) * np.exp(1j * masked_phase_spectrum)

        elif self.reconstruction_pair == "Real and Imaginary" and self.band_mask is not None:
            for idx, image in enumerate(self.image_labels):
                if self.is_canceled:
                    return  
        
                real_component[self.band_mask] += image.image.real_component[self.band_mask]
                imaginary_component[self.band_mask] += image.image.imaginary_component[self.band_mask]
                self.progress.emit((idx + 1) * 100 // num_images)

            masked_real_component = real_component * self.band_mask
            masked_imaginary_component = imaginary_component * self.band_mask
            ft_shifted = (masked_real_component / num_images) + 1j * (masked_imaginary_component / num_images)

        elif self.reconstruction_pair == "Magnitude and Phase" and self.band_mask is None:
            for idx, image in enumerate(self.image_labels):
                if self.is_canceled:
                    return  

                magnitude_spectrum += (
                    image.image.magnitude_spectrum * image.magnitude_real_slider.value() / 100
                )
                weight = image.phase_imaginary_slider.value() / (100.0 * num_images)
                phase_spectrum_real += weight * np.cos(image.image.phase_spectrum)
                phase_spectrum_imag += weight * np.sin(image.image.phase_spectrum)
                self.progress.emit((idx + 1) * 100 // num_images)

            phase_spectrum = np.arctan2(phase_spectrum_imag, phase_spectrum_real)
            ft_shifted = (magnitude_spectrum / num_images) * np.exp(1j * phase_spectrum)   

        elif self.reconstruction_pair == "Real and Imaginary" and self.band_mask is None:
            for idx, image in enumerate(self.image_labels):
                if self.is_canceled:
                    return  

                real_component += (
                    image.image.real_component * image.magnitude_real_slider.value() / 100
                )
                
                imaginary_component += (
                    image.image.imaginary_component * image.phase_imaginary_slider.value() / 100
                )
                self.progress.emit((idx + 1) * 100 // num_images)

            ft_shifted = (real_component / num_images) + 1j * (imaginary_component / num_images)

        ft_inverse_shift = np.fft.ifftshift(ft_shifted)
        mixed_image = np.fft.ifft2(ft_inverse_shift)
        mixed_image = np.abs(mixed_image)
        self.result_ready.emit(mixed_image)

    def cancel(self):
        self.is_canceled = True
