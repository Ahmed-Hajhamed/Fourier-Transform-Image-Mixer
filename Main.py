from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from qt_material import apply_stylesheet
from UI import Ui_MainWindow
from ImageMixingWorker import ImageMixingWorker
from ImageProcessor import normalize_to_8bit, array_to_pixmap
FT_PAIRS = [["Magnitude", "Phase"], ["Real", "Imaginary"]]

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.output_label = self.output_1_label
        self.reconstruction_pair = "Magnitude and Phase"

    def change_ft_component(self, current_text_on_combobox, image, ft_label):
        if current_text_on_combobox == "Magnitude":
            magnitude_8bit = normalize_to_8bit(image.magnitude_log)
            mag_pixmap = array_to_pixmap(magnitude_8bit)
            ft_label.setPixmap(mag_pixmap)

        if current_text_on_combobox == "Phase":
            phase_8bit = normalize_to_8bit(image.phase_spectrum)
            phase_pixmap = array_to_pixmap(phase_8bit)
            ft_label.setPixmap(phase_pixmap)

        if current_text_on_combobox == "Real":
            real_8bit = normalize_to_8bit(image.real_component)
            real_pixmap = array_to_pixmap(real_8bit)
            ft_label.setPixmap(real_pixmap)

        if current_text_on_combobox == "Imaginary":
            imaginary_8bit = normalize_to_8bit(image.imaginary_component)
            imaginary_pixmap = array_to_pixmap(imaginary_8bit)
            ft_label.setPixmap(imaginary_pixmap)

    def mix_images(self):
        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()
        if self.inner_region_radio_button.isChecked():
            band_mask = self.image_1_label.ft_label.inner_indices
        elif self.outer_region_radio_button.isChecked():
            band_mask = self.image_1_label.ft_label.outer_indices
        else:
            band_mask = None

        self.worker = ImageMixingWorker(self.image_labels, self.reconstruction_pair, band_mask)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.result_ready.connect(self.display_mixed_image)
        self.worker.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value) 

    def display_mixed_image(self, mixed_image):
        mixed_image_8bit = normalize_to_8bit(mixed_image)
        mixed_image_pixmap = array_to_pixmap(mixed_image_8bit)
        self.output_label.setPixmap(mixed_image_pixmap)
        self.progress_bar.setValue(0)

    def change_reconstruction_pairs(self):
        self.reconstruction_pair = self.ft_pairs_combobox.currentText()
        for image_label in self.image_labels:
            image_label.magnitude_real_label.setText(FT_PAIRS[self.ft_pairs_combobox.currentIndex()][0])
            image_label.phase_imaginary_label.setText(FT_PAIRS[self.ft_pairs_combobox.currentIndex()][1])
            image_label.magnitude_real_slider.setValue(100)
            image_label.phase_imaginary_slider.setValue(100)

    def switch_output_label(self):
        if self.output_1_radiobutton.isChecked():
            self.output_label = self.output_1_label
        else:
            self.output_label = self.output_2_label

    def resize_images(self):
        for image_label in self.image_labels: #checks minimum size
            self.minimum_height = min(image_label.image.image.shape[0])
            self.minimum_width = min(image_label.image.image.shape[1])

        for image_label in self.image_labels: #resizes images
            image_label.image.resize_image(self.minimum_width, self.minimum_height)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "dark_purple.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
