from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from qt_material import apply_stylesheet
from UI import Ui_MainWindow
from ImageMixingWorker import ImageMixingWorker
import Image

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.output_label = self.output_1_label
        self.reconstruction_pair = "Magnitude and Phase"

    def change_ft_component(self, text, image, ft_label):
        if text == "Magnitude":
            magnitude_8bit = Image.normalize_to_8bit(image.magnitude_log)
            mag_pixmap = Image.array_to_pixmap(magnitude_8bit)
            ft_label.setPixmap(mag_pixmap)

        if text == "Phase":
            phase_8bit = Image.normalize_to_8bit(image.phase_spectrum)
            phase_pixmap = Image.array_to_pixmap(phase_8bit)
            ft_label.setPixmap(phase_pixmap)

        if text == "Real":
            real_8bit = Image.normalize_to_8bit(image.real_component)
            real_pixmap = Image.array_to_pixmap(real_8bit)
            ft_label.setPixmap(real_pixmap)

        if text == "Imaginary":
            imaginary_8bit = Image.normalize_to_8bit(image.imaginary_component)
            imaginary_pixmap = Image.array_to_pixmap(imaginary_8bit)
            ft_label.setPixmap(imaginary_pixmap)
        # ft_label.get_outer_region()

    def mix_images(self, images):
        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()
        if self.inner_region_checkbox.isCkecked():
            indices = self.image_1_label.ft_label.inner_indices
        elif self.outer_region_checkbox.isCkecked():
            indices = self.image_1_label.ft_label.outer_indices
        else:
            indices = None

        self.worker = ImageMixingWorker(images, self.reconstruction_pair, indices)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.result_ready.connect(self.display_mixed_image)
        self.worker.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value) 

    def display_mixed_image(self, mixed_image):
        mixed_image_8bit = Image.normalize_to_8bit(mixed_image)
        mixed_image_pixmap = Image.array_to_pixmap(mixed_image_8bit)
        self.output_label.setPixmap(mixed_image_pixmap)
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
    
    def switch_inner_outer(self):
        # if self.inner_region_radio_button.isChecked():
        #     self.inner_region_radio_button
        # else:
        #     self.inner
        return

    def resize_images(self):
        self.minimum_height = min(image.image.image.shape[0] for image in self.images)
        self.minimum_width = min(image.image.image.shape[1] for image in self.images)
        for image in self.images:
            image.image.resize_image(self.minimum_width, self.minimum_height)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "dark_purple.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
