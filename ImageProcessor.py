import cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage


class ImageProcessor:
    def __init__(self, image_label, label_size = (300, 400)):
        super().__init__()
        self.image = None
        self.ft = None
        self.ft_shifted = None
        self.magnitude_spectrum = None
        self.magnitude_log = None
        self.phase_spectrum = None
        self.real_component = None
        self.imaginary_component = None
        self.contrast = 1.0
        self.brightness = 0
        self.image_label = image_label
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(*label_size)

    def update_display(self):
        if self.image is None:
            self.image_label.clear()
        else:
            set_array_to_pixmap(self.image, self.image_label, normalize= False)

    def load_image(self, image_path= None):
        if image_path is None:
            image_path, _ = QFileDialog.getOpenFileName(
                None, 
                "Open File", "Images", 
                "Images (*.png *.xpm *.jpg *.jpeg *.jpe *.jp2 *.bmp *.gif *.webp *.dib *.avif\
                  *.pic *.hdr *.pbm *.pgm *.ppm *.pxm *.pnm *.pfm *.sr *.ras *.tiff *.tif *.exr)")
        if image_path:
            self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            self.adjust_brightness_contrast(reset= True)
            self.update_display()

    def resize_image(self, width = None, height = None):
        if self.image is not None:
            if width and height:
                self.image = cv2.resize(self.image, (width, height))
            self.compute_ft_components()
            self.update_display()

    def compute_ft_components(self):
        if self.image is not None:
            self.ft = np.fft.fft2(self.image)
            self.ft_shifted = np.fft.fftshift(self.ft)
            self.magnitude_spectrum = np.abs(self.ft_shifted)
            self.magnitude_log = np.log1p(self.magnitude_spectrum) 
            self.phase_spectrum = np.angle(self.ft_shifted)
            self.real_component = np.real(self.ft_shifted)
            self.imaginary_component = np.imag(self.ft_shifted)

    def adjust_brightness_contrast(self, reset= False):
        if reset:
            self.brightness, self.contrast = 0, 1.0
        if self.image is not None:
            self.image= cv2.convertScaleAbs(self.image, alpha=self.contrast, beta=self.brightness)                                                                   
            self.update_display()


def set_array_to_pixmap(array, label, normalize = True):
    if normalize:
        array = normalize_to_8bit(array)
    height, width = array.shape
    bytes_per_line = width
    image_data = array.tobytes()
    qimage = QImage(image_data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(qimage)
    label.setPixmap(pixmap)

def normalize_to_8bit(array):
    norm = (255 * (array - array.min()) / (array.max() - array.min() + 1e-12)).astype(np.uint8)
    return norm
