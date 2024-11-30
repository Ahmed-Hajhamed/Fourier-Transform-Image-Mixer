import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QPushButton, QComboBox, QSlider, QFileDialog, QProgressBar, QGraphicsView, QGraphicsScene
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage



def creat_separator(type:str):
    separator = QFrame()
    if type == "h":
        separator.setFrameShape(QFrame.HLine)
    elif type == "v":
        separator.setFrameShape(QFrame.VLine)
    else : 
        return
    separator.setFrameShadow(QFrame.Sunken)
    separator.setStyleSheet("padding: 0px;")
    return separator

class InputImageUi:
    def __init__(self):

        self.image_path = None
        self.image = None

        label_stylee_sheet = """
                            Qlable{
                            color:#878dfa;
                            background-color:#92f28d;
                            font-style:italic;
                            font-weight:bold;
                            text-decoration: underline;
                             }
                             """
        
        self.h_layout_of_original_and_changed_of_the_image = QHBoxLayout()
        self.h_layout_of_buttons_and_combo_box = QHBoxLayout()
        self.v_layout_container = QVBoxLayout()

        self.label_of_original_image = QLabel("test")
        # self.label_of_original_image.setScaledContents(True)
        self.h_layout_of_original_and_changed_of_the_image.addWidget(self.label_of_original_image)

        self.label_of_components_based_on = QLabel("test")
        # self.label_of_components_based_on.setScaledContents(True)
        self.h_layout_of_original_and_changed_of_the_image.addWidget(self.label_of_components_based_on)


        self.combo_box_of_components_based_on = QComboBox()
        self.combo_box_of_components_based_on.addItem("Magnitude")
        self.combo_box_of_components_based_on.addItem("Phase")
        self.combo_box_of_components_based_on.addItem("Real")
        self.combo_box_of_components_based_on.addItem("Imaginary")

        self.h_layout_of_buttons_and_combo_box.addWidget(self.combo_box_of_components_based_on)

        self.button_to_add_image = QPushButton("add")
        self.h_layout_of_buttons_and_combo_box.addWidget(self.button_to_add_image)

        self.v_layout_container.addLayout(self.h_layout_of_original_and_changed_of_the_image)
        self.v_layout_container.addLayout(self.h_layout_of_buttons_and_combo_box)

        pass

    def load_image(self, image_path):
        """Load an image and convert it to grayscale if needed."""
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.brightness = 0
        self.contrast = 1.0
        self.update_display()

    def add_image(self, image_path):
        self.image = image_path
    
    def update_display(self):
        """Update the displayed image based on brightness and contrast adjustments."""
        if self.image is not None:
            # Apply brightness and contrast adjustments
            adjusted = cv2.convertScaleAbs(self.image, alpha=self.contrast, beta=self.brightness)
            self.adjusted_image = adjusted

            # Convert to QPixmap and display
            height, width = adjusted.shape
            print(adjusted.data)
            print(self.image)
            q_image = QImage(adjusted.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.setPixmap(pixmap)

    
    def plotImage(self):
        pass


class OutputImageUi:
    def __init__(self):
        self.v_layout = QVBoxLayout()
        self.grid_layout_of_slider = QGridLayout()


        self.label_1 = QLabel("test 1 ")
        self.label_1.setMinimumSize(350,300)
        self.v_layout.addWidget(self.label_1)

        self.seprator_1 = creat_separator("h")
        self.v_layout.addWidget(self.seprator_1)
        
        self.label_2 = QLabel("test 2")
        self.label_2.setMinimumSize(350,300)
        self.v_layout.addWidget(self.label_2)

        self.seprator_2 = creat_separator("h")
        self.v_layout.addWidget(self.seprator_2)
        
        
        self.slider_magnitude = QSlider(Qt.Vertical)
        self.slider_magnitude.setFixedHeight(100)
        self.grid_layout_of_slider.addWidget(self.slider_magnitude, 0, 0)
        self.label_of_magnitude = QLabel("magnitude")
        self.grid_layout_of_slider.addWidget(self.label_of_magnitude, 1, 0)

        self.slider_phase = QSlider(Qt.Vertical)
        self.slider_phase.setFixedHeight(100)
        self.grid_layout_of_slider.addWidget(self.slider_phase, 0, 1)
        self.label_of_phase = QLabel("phase")
        self.grid_layout_of_slider.addWidget(self.label_of_phase, 1, 1)

        self.slider_real = QSlider(Qt.Vertical)
        self.slider_real.setFixedHeight(100)
        self.grid_layout_of_slider.addWidget(self.slider_real, 0, 2)
        self.label_of_real = QLabel("real")
        self.grid_layout_of_slider.addWidget(self.label_of_real, 1, 2)

        self.slider_imaginary = QSlider(Qt.Vertical)
        self.slider_imaginary.setFixedHeight(100)
        self.grid_layout_of_slider.addWidget(self.slider_imaginary, 0, 3)
        self.label_of_imaginary = QLabel("imaginary")
        self.grid_layout_of_slider.addWidget(self.label_of_imaginary, 1, 3)

        self.slider_reigon = QSlider(Qt.Vertical)
        self.slider_reigon.setFixedHeight(100)
        self.grid_layout_of_slider.addWidget(self.slider_reigon, 0, 4)
        
        self.label_of_reigon = QLabel("reigon")
        self.grid_layout_of_slider.addWidget(self.label_of_reigon, 1, 4)


        self.v_layout.addLayout(self.grid_layout_of_slider)
        # self.v_layout.setContentsMargins(0, 0, 0, 0)
