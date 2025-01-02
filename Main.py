from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from qt_material import apply_stylesheet
import UI 
from ImageMixingWorker import ImageMixingWorker
from ImageProcessor import set_array_to_pixmap
import logging
logging.basicConfig(level=logging.INFO, filename="Logging\\logging_file.log",
                     format='%(asctime)s:%(levelname)s:%(message)s', filemode='w') 


class MainWindow(QMainWindow, UI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.output_label = self.output_1_label
        self.reconstruction_pair = "Magnitude and Phase"
        self.image_2_label.image.load_image("Images\\Nikola-Tesla.jpg")
        self.image_3_label.image.load_image("Images\\Bill-Gates.jpg")
        self.image_4_label.image.load_image("Images\\Elon-Musk.jpg")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.resize_images()

    def change_ft_component(self, current_text_on_combobox, image, ft_label):
        if image.image is None:
            ft_label.clear()

        elif current_text_on_combobox == "Magnitude":
            set_array_to_pixmap(image.magnitude_log, ft_label)

        elif current_text_on_combobox == "Phase":
            set_array_to_pixmap(image.phase_spectrum, ft_label)

        elif current_text_on_combobox == "Real":
            set_array_to_pixmap(image.real_component, ft_label)

        elif current_text_on_combobox == "Imaginary":
            set_array_to_pixmap(image.imaginary_component, ft_label)

    def mix_images(self):
        self.logger.debug("Mixing Images Started")
        if hasattr(self, "worker") and self.worker.isRunning():
            self.logger.debug("Cancelled running mixing operation")
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
        set_array_to_pixmap(mixed_image, self.output_label)
        self.progress_bar.setValue(0)

    def change_reconstruction_pairs(self):
        self.reconstruction_pair = self.ft_pairs_combobox.currentText()
        for image_label in self.image_labels:
            image_label.weight_slider.setValue(100)
            image_label.ft_combobox.clear()
            image_label.ft_combobox.addItems(UI.InputImageLabel.FT_COMPONENTS[self.ft_pairs_combobox.currentIndex()])

    def switch_output_label(self):
        if self.output_1_radiobutton.isChecked():
            self.output_label = self.output_1_label
        else:
            self.output_label = self.output_2_label

    def resize_images(self):
        self.logger.debug("New Image Loaded, finding smallest dimensions")
        heights, widths = [], []
        for image_label in self.image_labels: # Checks minimum size
            if image_label.image.image is None:
                continue
            heights.append(image_label.image.image.shape[0])
            widths.append(image_label.image.image.shape[1])

        self.minimum_height = min(heights)
        self.minimum_width = min(widths)

        self.logger.debug(f"Minimum Height = {self.minimum_height}")
        self.logger.debug(f"Minimum Width = {self.minimum_width}")
        for image_label in self.image_labels: # Resizes images
            image_label.image.resize_image(self.minimum_width, self.minimum_height)
            self.change_ft_component(image_label.ft_combobox.currentText(), image_label.image, image_label.ft_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "dark_purple.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
