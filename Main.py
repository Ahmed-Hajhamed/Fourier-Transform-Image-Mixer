from PyQt5.QtWidgets import (
    QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap, QImage
import sys
from qt_material import apply_stylesheet
from UI import Ui_MainWindow
import numpy as np
from ImageMixingWorker import ImageMixingWorker

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.output_label = self.output_1_label
        self.reconstruction_pair = "Magnitude and Phase"

    def change_ft_component(self, image, ft_label):
        combo_box = self.sender()
        if combo_box is not None:
            if combo_box.currentText() == "Magnitude":
                magnitude_8bit = self.normalize_to_8bit(image.magnitude_log)
                mag_pixmap = self.array_to_pixmap(magnitude_8bit)
                ft_label.setPixmap(mag_pixmap)

            if combo_box.currentText() == "Phase":
                phase_8bit = self.normalize_to_8bit(image.phase_spectrum)
                phase_pixmap = self.array_to_pixmap(phase_8bit)
                ft_label.setPixmap(phase_pixmap)

            if combo_box.currentText() == "Real":
                real_8bit = self.normalize_to_8bit(image.real_component)
                real_pixmap = self.array_to_pixmap(real_8bit)
                ft_label.setPixmap(real_pixmap)

            if combo_box.currentText() == "Imaginary":
                imaginary_8bit = self.normalize_to_8bit(image.imaginary_component)
                imaginary_pixmap = self.array_to_pixmap(imaginary_8bit)
                ft_label.setPixmap(imaginary_pixmap)

    def mix_images(self, images):

        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()

        self.worker = ImageMixingWorker(images, self.reconstruction_pair)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.result_ready.connect(self.display_mixed_image)

        self.worker.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value) 

    def display_mixed_image(self, mixed_image):
        mixed_8bit = self.normalize_to_8bit(mixed_image)
        mixed_pixmap = self.array_to_pixmap(mixed_8bit)
        self.output_label.setPixmap(mixed_pixmap)
        self.progress_bar.setValue(0)

    def change_reconstruction_pairs(self, images):
        self.reconstruction_pair = self.ft_pairs_combobox.currentText()
        pairs = [["Magnitude", "Phase"], ["Real", "Imaginary"]]
        for image in images:
            image.magnitude_real_label.setText(pairs[self.ft_pairs_combobox.currentIndex()][0])
            image.phase_imaginary_label.setText(pairs[self.ft_pairs_combobox.currentIndex()][1])
            image.magnitude_real_slider.setValue(100)
            image.phase_imaginary_slider.setValue(100)

    def switch_output_label(self):
        if self.output_1_radiobutton.isChecked():
            self.output_label = self.output_1_label
        else:
            self.output_label = self.output_2_label

    def normalize_to_8bit(self, array):
        norm = (255 * (array - array.min()) / (array.max() - array.min())).astype(np.uint8)
        return norm
    
    def array_to_pixmap(self, array):
        if array.dtype != np.uint8:
            raise ValueError("Array must be of type uint8.")
        height, width = array.shape
        bytes_per_line = width
        image_data = array.tobytes()
        qimage = QImage(image_data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimage)
    
def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, "dark_purple.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
