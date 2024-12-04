import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QPoint
import cv2


class ClickableLabel(QLabel):
    def __init__(self, index, main_window, parent=None):
        super().__init__(parent)
        self.index = index
        self.main_window = main_window
        self.original_image = None
        self.brightness = 0
        self.contrast = 1.0
        self.last_mouse_pos = QPoint()  # Track the last mouse position

    def set_image(self, image):

        self.original_image = image
        self.update_image()

    def update_image(self):

        if self.original_image is None:
            return

        # Apply brightness and contrast adjustments
        adjusted = cv2.convertScaleAbs(
            self.original_image,
            alpha=self.contrast,
            beta=self.brightness
        )


        height, width = adjusted.shape
        bytes_per_line = width
        q_image = QImage(adjusted.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.main_window.replace_image(self.index)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.original_image is not None and event.buttons() & Qt.LeftButton:

            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()


            self.brightness += delta.y()
            self.contrast = max(0.1, self.contrast + delta.x() * 0.01)  # Prevent zero or negative contrast


            self.update_image()


class FFTImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FFT Image Mixer")
        self.setGeometry(100, 100, 800, 600)

        self.images = [None] * 4
        self.image_labels = []
        self.result_label = QLabel("Mixed Image will appear here", self)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()


        for i in range(4):
            button = QPushButton(f"Load Image {i + 1}")
            button.clicked.connect(lambda _, idx=i: self.load_image(idx))
            layout.addWidget(button)

            label = ClickableLabel(index=i, main_window=self)
            label.setText(f"Image {i + 1} not loaded")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 1px solid black;")
            layout.addWidget(label)
            self.image_labels.append(label)


        mix_button = QPushButton("Mix Images with FFT")
        mix_button.clicked.connect(self.mix_images)
        layout.addWidget(mix_button)


        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self, index):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options
        )
        if file_path:
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                self.image_labels[index].setText("Error loading image")
                return

            self.images[index] = image


            self.image_labels[index].set_image(image)

    def replace_image(self, index):

        self.load_image(index)

    def mix_images(self):
        if any(image is None for image in self.images):
            self.result_label.setText("Please load 4 images first!")
            return


        fft_images = [np.fft.fft2(image) for image in self.images]


        combined_magnitude = np.abs(fft_images[0])
        combined_phase = np.angle(fft_images[1])

        for i in range(2, 4):
            combined_magnitude += np.abs(fft_images[i])
            combined_phase += np.angle(fft_images[i])


        combined_fft = combined_magnitude * np.exp(1j * combined_phase)


        mixed_image = np.fft.ifft2(combined_fft).real
        mixed_image = np.clip(mixed_image, 0, 255).astype(np.uint8)


        self.display_result(mixed_image)

    def display_result(self, image):
        height, width = image.shape
        bytes_per_line = width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)

        self.result_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FFTImageViewer()
    viewer.show()
    sys.exit(app.exec_())
