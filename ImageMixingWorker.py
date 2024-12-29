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
        number_of_images = 0
        for image_label in self.image_labels:
            if image_label.image.image is not None:
                number_of_images += 1
        complete_phase = False
        complete_magnitude = False
        complete_real = False
        complete_imaginary = False
        magnitude_spectrum = np.zeros_like(self.image_labels[0].image.magnitude_spectrum, dtype=np.float64)
        phase_spectrum = np.zeros_like(self.image_labels[0].image.phase_spectrum, dtype=np.float64)
        phase_spectrum_real = np.zeros_like(self.image_labels[0].image.phase_spectrum, dtype=np.float64)
        phase_spectrum_imag = np.zeros_like(self.image_labels[0].image.phase_spectrum, dtype=np.float64)
        real_component = np.zeros_like(self.image_labels[0].image.real_component, dtype=np.float64)
        imaginary_component = np.zeros_like(self.image_labels[0].image.imaginary_component, dtype=np.float64)

        if self.reconstruction_pair == "Magnitude and Phase" and self.band_mask is not None:
            for idx, image_label in enumerate(self.image_labels):
                if self.is_canceled:
                    return  
                if image_label.image.image is None:
                    continue
                if image_label.ft_combobox.currentText() == "Magnitude":
                    complete_magnitude=True
                    magnitude_spectrum[self.band_mask] +=  (image_label.image.magnitude_spectrum[self.band_mask]\
                                                            * image_label.weight_slider.value() / 100)
                elif image_label.ft_combobox.currentText() == "Phase":
                    complete_phase = True
                    weight =  image_label.weight_slider.value() / (100.0 * number_of_images)
                    phase_spectrum_real[self.band_mask] += weight * np.cos(image_label.image.phase_spectrum[self.band_mask])
                    phase_spectrum_imag[self.band_mask] += weight * np.sin(image_label.image.phase_spectrum[self.band_mask])
                self.progress.emit((idx + 1) * 100 // (number_of_images + 1))

            phase_spectrum = np.arctan2(phase_spectrum_imag, phase_spectrum_real)
            masked_magnitude_spectrum = magnitude_spectrum * self.band_mask 
            masked_phase_spectrum = phase_spectrum * self.band_mask
            if not complete_magnitude: magnitude_spectrum = np.ones_like(self.image_labels[0].image.magnitude_spectrum, dtype=np.float64)
            complete_magnitude = True
            ft_shifted = (masked_magnitude_spectrum / number_of_images) * np.exp(1j * masked_phase_spectrum)

        elif self.reconstruction_pair == "Real and Imaginary" and self.band_mask is not None:
            for idx, image_label in enumerate(self.image_labels):
                if self.is_canceled:
                    return  
                if image_label.image.image is None:
                    continue
                if image_label.ft_combobox.currentText() == "Real":
                    complete_real = True
                    real_component[self.band_mask] += (image_label.image.real_component[self.band_mask]\
                                                            * image_label.weight_slider.value() / 100)
                elif image_label.ft_combobox.currentText() == "Imaginary":
                    complete_imaginary = True
                    imaginary_component[self.band_mask] += (image_label.image.imaginary_component[self.band_mask]\
                                                            *image_label.weight_slider.value() / 100)
                self.progress.emit((idx + 1) * 100 // (number_of_images + 1))

            masked_real_component = real_component * self.band_mask
            masked_imaginary_component = imaginary_component * self.band_mask
            ft_shifted = (masked_real_component / number_of_images) + 1j * (masked_imaginary_component / number_of_images)

        elif self.reconstruction_pair == "Magnitude and Phase" and self.band_mask is None:
            for idx, image_label in enumerate(self.image_labels):
                if self.is_canceled:
                    return  
                if image_label.image.image is None:
                    continue
                if image_label.ft_combobox.currentText() == "Magnitude":
                    complete_magnitude = True
                    magnitude_spectrum += (
                        image_label.image.magnitude_spectrum * image_label.weight_slider.value() / 100
                    )
                elif image_label.ft_combobox.currentText() == "Phase":
                    complete_phase = True
                    weight = image_label.weight_slider.value() / (100.0 * number_of_images)
                    phase_spectrum_real += weight * np.cos(image_label.image.phase_spectrum)
                    phase_spectrum_imag += weight * np.sin(image_label.image.phase_spectrum)

                self.progress.emit((idx + 1) * 100 // (number_of_images + 1))
            phase_spectrum = np.arctan2(phase_spectrum_imag, phase_spectrum_real)
            if not complete_magnitude: magnitude_spectrum = np.ones_like(self.image_labels[0].image.magnitude_spectrum, dtype=np.float64)
            complete_magnitude = True
            ft_shifted = (magnitude_spectrum / number_of_images) * np.exp(1j * phase_spectrum)   

        elif self.reconstruction_pair == "Real and Imaginary" and self.band_mask is None:
            for idx, image_label in enumerate(self.image_labels):
                if self.is_canceled:
                    return  
                if image_label.image.image is None:
                    continue
                if image_label.ft_combobox.currentText() == "Real":
                    complete_real = True
                    real_component += (
                        image_label.image.real_component * image_label.weight_slider.value() / 100
                    )
                elif image_label.ft_combobox.currentText() == "Imaginary":
                    complete_imaginary = True
                    imaginary_component += (
                        image_label.image.imaginary_component * image_label.weight_slider.value()/ 100
                    )
                self.progress.emit((idx + 1) * 100 // (number_of_images + 1))

            ft_shifted = (real_component / number_of_images) + 1j * (imaginary_component / number_of_images)

        ft_inverse_shift = np.fft.ifftshift(ft_shifted)
        mixed_image = np.fft.ifft2(ft_inverse_shift)
        self.progress.emit(100)
        mixed_image = np.abs(mixed_image)
        if (complete_magnitude and complete_phase) or (complete_real or complete_imaginary):
            self.result_ready.emit(mixed_image)
        elif not complete_phase and self.reconstruction_pair == "Magnitude and Phase":
            self.result_ready.emit(np.log1p(mixed_image))

    def cancel(self):
        self.is_canceled = True
