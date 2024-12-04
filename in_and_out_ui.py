import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QPushButton, QComboBox, QSlider, QFileDialog, QProgressBar, QGraphicsView, QGraphicsScene, QCheckBox
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage
from Image import Image


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

def slider_creator():
    slider = QSlider(Qt.Vertical)
    slider.setMinimum(0)
    slider.setMaximum(100)
    slider.setValue(100)
    slider.setFixedHeight(100)
    return slider



class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = Image()
        self.last_mouse_pos = QPoint()
    
    def update_display(self):
        """Update the displayed image based on brightness and contrast adjustments."""
        if self.image is not None:
            self.image.image = cv2.resize(self.image.image, (400, 500))
            # Apply brightness and contrast adjustments
            adjusted = cv2.convertScaleAbs(self.image.image, alpha=self.image.contrast, beta=self.image.brightness)
            self.adjusted_image = adjusted
            # Convert to QPixmap and display
            height, width = adjusted.shape
            q_image = QImage(adjusted.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.setPixmap(pixmap)

    def mouseDoubleClickEvent(self, event):
        # Open file dialog on double-click
        self.image.load_image()
        self.update_display()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.image.image is not None and event.buttons() & Qt.LeftButton:

            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()


            self.image.brightness += delta.y()
            self.image.contrast = max(0.1, self.image.contrast + delta.x() * 0.01)  # Prevent zero or negative contrast
            self.update_display()


class InputImageUi:
    def __init__(self, parent=None):
        # super().__init__(parent)
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

        self.label_of_original_image = ImageLabel()
        # self.label_of_original_image.setScaledContents(True)
        self.h_layout_of_original_and_changed_of_the_image.addWidget(self.label_of_original_image)

        self.label_of_components_based_on = QLabel("zeyad")
        # self.label_of_components_based_on.setScaledContents(True)
        self.h_layout_of_original_and_changed_of_the_image.addWidget(self.label_of_components_based_on)


        self.combo_box_of_components_based_on = QComboBox()
        self.combo_box_of_components_based_on.addItem("Magnitude")
        self.combo_box_of_components_based_on.addItem("Phase")
        self.combo_box_of_components_based_on.addItem("Real")
        self.combo_box_of_components_based_on.addItem("Imaginary")

        self.h_layout_of_buttons_and_combo_box.addWidget(self.combo_box_of_components_based_on)

        # self.button_to_add_image = QPushButton("add")
        # self.h_layout_of_buttons_and_combo_box.addWidget(self.button_to_add_image)

        self.v_layout_container.addLayout(self.h_layout_of_original_and_changed_of_the_image)
        self.v_layout_container.addLayout(self.h_layout_of_buttons_and_combo_box)

    
    

    def mouseDoubleClickEvent(self, a0):

        self.image_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open File", 
            "", 
            "All Files (*.*);;Text Files (*.txt);;Images (*.png *.jpg)"
        )
        self.load_image(self.image_path)


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
            self.image = cv2.resize(self.image, (400, 500))
            # Apply brightness and contrast adjustments
            adjusted = cv2.convertScaleAbs(self.image, alpha=self.contrast, beta=self.brightness)
            self.adjusted_image = adjusted
            # Convert to QPixmap and display
            height, width = adjusted.shape
            q_image = QImage(adjusted.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.label_of_original_image.setPixmap(pixmap)
            # self.label_of_original_image.resize(int(width/10), int(height/10))

    
    def plotImage(self):
        pass


class OutputImageUi:
    def __init__(self):

        self.choice = 1
        self.v_layout = QVBoxLayout()
        self.grid_layout_of_slider = QGridLayout()


        self.label_1 = QLabel("test 1 ")
        self.label_1.setMinimumSize(350,300)
        self.v_layout.addWidget(self.label_1)

        self.check_of_output_1 = QCheckBox("show")
        self.check_of_output_1.setChecked(True)
        self.check_of_output_1.stateChanged.connect(lambda: self.check_box_1())
        self.v_layout.addWidget(self.check_of_output_1)

        self.seprator_1 = creat_separator("h")
        self.v_layout.addWidget(self.seprator_1)
        
        self.label_2 = QLabel("test 2")
        self.label_2.setMinimumSize(350,300)
        self.v_layout.addWidget(self.label_2)

        self.check_of_output_2 = QCheckBox("show")
        self.check_of_output_2.setChecked(False)
        self.check_of_output_2.stateChanged.connect(self.check_box_2)
        self.v_layout.addWidget(self.check_of_output_2)

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

        
        self.v_layout.addLayout(self.grid_layout_of_slider)
        

        h_layout_of_mix_and_region = QHBoxLayout()
        self.mix_button = QPushButton("Mix")
        self.mix_button.setFixedWidth(100)
        h_layout_of_mix_and_region.addWidget(self.mix_button)

        self.slider_reigon = QSlider(Qt.Horizontal)
        self.slider_reigon.setFixedWidth(200)
        h_layout_of_mix_and_region.addWidget(self.slider_reigon)

        self.label_of_reigon = QLabel("reigon")
        self.label_of_reigon.setFixedWidth(100)
        h_layout_of_mix_and_region.addWidget(self.label_of_reigon)

        self.v_layout.addLayout(h_layout_of_mix_and_region)
        


        
        # self.v_layout.setContentsMargins(0, 0, 0, 0)

    def check_box_1(self):
        print(f"test1---> ")
        if self.check_of_output_1.isChecked():
            print("test2")
            self.check_of_output_2.setChecked(False)
        else:
            self.check_of_output_2.setChecked(True)

    def check_box_2(self): 
        if self.check_of_output_2.isChecked():
            self.check_of_output_1.setChecked(False)
        else:
            self.check_of_output_1.setChecked(True)

    
