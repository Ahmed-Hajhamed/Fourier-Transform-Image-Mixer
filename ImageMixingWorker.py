from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

class ImageMixingWorker(QThread):
    progress = pyqtSignal(int)  
    result_ready = pyqtSignal(np.ndarray)

    def __init__(self, images, reconstruction_pair, indices):
        super().__init__()
        self.images = images
        self.reconstruction_pair = reconstruction_pair
        self.indices = indices
        self.is_canceled = False  

    def run(self):
        num_images = len(self.images)
        magnitude_spectrum = np.zeros_like(self.images[0].image.magnitude_spectrum, dtype=np.float64)
        phase_spectrum_real = np.zeros_like(self.images[0].image.phase_spectrum, dtype=np.float64)
        phase_spectrum_imag = np.zeros_like(self.images[0].image.phase_spectrum, dtype=np.float64)
        real_component = np.zeros_like(self.images[0].image.real_component, dtype=np.float64)
        imaginary_component = np.zeros_like(self.images[0].image.imaginary_component, dtype=np.float64)

        if self.indices is not None:
            for idx, image in enumerate(self.images):
                if self.is_canceled:
                    return  

                magnitude_spectrum[self.indices] +=  image.image.magnitude_spectrum[self.indices]


                weight = 0.25
                phase_spectrum_real[self.indices] += weight * np.cos(image.image.phase_spectrum[self.indices])
                phase_spectrum_imag[self.indices] += weight * np.sin(image.image.phase_spectrum[self.indices])

                real_component[self.indices] += image.image.real_component[self.indices]
                
                imaginary_component[self.indices] += image.image.imaginary_component[self.indices]

                self.progress.emit((idx + 1) * 100 // num_images)

            if self.reconstruction_pair == "Magnitude and Phase":
                # Apply mask to magnitude and phase spectra
                phase_spectrum = np.arctan2(phase_spectrum_imag, phase_spectrum_real)
                masked_magnitude_spectrum = magnitude_spectrum * self.indices  # Apply mask
                masked_phase_spectrum = phase_spectrum * self.indices  # Optional: phase spectrum may need no masking if global phase is desired
                ft_shifted = (masked_magnitude_spectrum / num_images) * np.exp(1j * masked_phase_spectrum)

            elif self.reconstruction_pair == "Real and Imaginary":
                # Apply mask to real and imaginary components
                masked_real_component = real_component * self.indices
                masked_imaginary_component = imaginary_component * self.indices
                ft_shifted = (masked_real_component / num_images) + 1j * (masked_imaginary_component / num_images)

        else:
            for idx, image in enumerate(self.images):
                if self.is_canceled:
                    return  

                magnitude_spectrum += (
                    image.image.magnitude_spectrum * image.magnitude_real_slider.value() / 100
                )
                weight = image.phase_imaginary_slider.value() / (100.0 * num_images)
                phase_spectrum_real += weight * np.cos(image.image.phase_spectrum)
                phase_spectrum_imag += weight * np.sin(image.image.phase_spectrum)

                real_component += (
                    image.image.real_component * image.magnitude_real_slider.value() / 100
                )
                
                imaginary_component += (
                    image.image.imaginary_component * image.phase_imaginary_slider.value() / 100
                )

                self.progress.emit((idx + 1) * 100 // num_images)

            if self.reconstruction_pair == "Magnitude and Phase":
                phase_spectrum = np.arctan2(phase_spectrum_imag, phase_spectrum_real)
                ft_shifted = (magnitude_spectrum / num_images) * np.exp(1j * phase_spectrum)

            elif self.reconstruction_pair == "Real and Imaginary":
                ft_shifted = (real_component / num_images) + 1j * (imaginary_component / num_images)

        ft_inverse_shift = np.fft.ifftshift(ft_shifted)
        mixed_image = np.fft.ifft2(ft_inverse_shift)
        mixed_image = np.abs(mixed_image)

        self.result_ready.emit(mixed_image)

    def cancel(self):
        self.is_canceled = True
