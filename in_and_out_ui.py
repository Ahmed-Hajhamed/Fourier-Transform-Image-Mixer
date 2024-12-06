import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QPushButton, QComboBox, QSlider, QFileDialog, QProgressBar, QGraphicsView, QGraphicsScene, QCheckBox, 
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
        self.image = Image(self)
        # self.image.image_label = self
        self.last_mouse_pos = QPoint()
    
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Open file dialog on double-click
            self.image.load_image()
            self.image.resize_image(400, 500)
            # self.image.update_display()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.in_brightness = self.image.brightness
            self.in_con = self.image.contrast

    def mouseMoveEvent(self, event):
        if self.image.image is not None and event.buttons() & Qt.LeftButton:
            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()
            new_brightness = self.in_brightness - delta.y() /10
            new_contrast = max(0.1, self.in_con + delta.x()/10 * 0.01)  # Prevent zero or negative contrast

            brightness_min, brightness_max = -50, 50  # Set brightness limits
            contrast_min, contrast_max = 0.5, 2.0  

            self.image.brightness = max(brightness_min, min(brightness_max, new_brightness))
            self.image.contrast = max(contrast_min, min(contrast_max, new_contrast))

            self.image.adjust_brightness_contrast()
            # self.image.update_display()


class InputImageUi:
    def __init__(self, parent=None):
        # super().__init__(parent)
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
        self.h_layout_of_buttons_and_combo_box =QGridLayout()
        self.v_layout_container = QVBoxLayout() 
        self.label_of_original_image = ImageLabel()
        # self.label_of_original_image.setScaledContents(True)
        self.h_layout_of_original_and_changed_of_the_image.addWidget(self.label_of_original_image)

        self.label_of_components_based_on = QLabel("zeyad")
        # self.label_of_components_based_on.setScaledContents(True)
        self.h_layout_of_original_and_changed_of_the_image.addWidget(self.label_of_components_based_on)

        self.magnitude_real_label = QLabel("Magnitude:")
        self.phase_imaginary_label = QLabel("Phase:")

        self.magnitude_real_slider =  QSlider(Qt.Horizontal)
        self.phase_imaginary_slider = QSlider(Qt.Horizontal)

        self.ft_component_label = QLabel("FT Component:")

        self.combo_box_of_components_based_on = QComboBox()
        self.combo_box_of_components_based_on.addItem("Magnitude")
        self.combo_box_of_components_based_on.addItem("Phase")
        self.combo_box_of_components_based_on.addItem("Real")
        self.combo_box_of_components_based_on.addItem("Imaginary")

        self.h_layout_of_buttons_and_combo_box.addWidget(self.magnitude_real_label, 0, 0)
        self.h_layout_of_buttons_and_combo_box.addWidget(self.phase_imaginary_label, 1, 0)
        self.h_layout_of_buttons_and_combo_box.addWidget(self.magnitude_real_slider, 0, 1)
        self.h_layout_of_buttons_and_combo_box.addWidget(self.phase_imaginary_slider, 1, 1)
        self.h_layout_of_buttons_and_combo_box.addWidget(self.ft_component_label, 0, 2, 0, 1)
        self.h_layout_of_buttons_and_combo_box.addWidget(self.combo_box_of_components_based_on, 0, 3, 0, 1)


        self.v_layout_container.addLayout(self.h_layout_of_original_and_changed_of_the_image)
        self.v_layout_container.addLayout(self.h_layout_of_buttons_and_combo_box)

    
    
    
    def plotImage(self):
        pass


class OutputImageUi:
    def __init__(self):

        self.choice = 1
        self.v_layout = QVBoxLayout()

        self.label_1 = QLabel("test 1 ")
        # self.label_1.setMinimumSize(350,300)
        self.v_layout.addWidget(self.label_1)

        self.check_of_output_1 = QCheckBox("show")
        self.check_of_output_1.setChecked(True)
        self.check_of_output_1.stateChanged.connect(lambda: self.check_box_1())
        self.v_layout.addWidget(self.check_of_output_1)

        self.seprator_1 = creat_separator("h")
        self.v_layout.addWidget(self.seprator_1)
        
        self.label_2 = QLabel("test 2")
        # self.label_2.setMinimumSize(350,300)
        self.v_layout.addWidget(self.label_2)

        self.check_of_output_2 = QCheckBox("show")
        self.check_of_output_2.setChecked(False)
        self.check_of_output_2.stateChanged.connect(self.check_box_2)
        self.v_layout.addWidget(self.check_of_output_2)

        self.seprator_2 = creat_separator("h")
        self.v_layout.addWidget(self.seprator_2)
        
        
        self.ft_pairs_combobox = QComboBox()
        self.ft_pairs_combobox.addItems(["Magnitude and Phase", "Real and Imaginary"])

        self.ft_pairs_label = QLabel("FT Pairs:")

        h_layout_of_mix_and_region = QHBoxLayout()
        self.mix_button = QPushButton("Mix")
        # self.mix_button.setFixedWidth(100)
        h_layout_of_mix_and_region.addWidget(self.mix_button)

        self.slider_reigon = QSlider(Qt.Horizontal)
        self.slider_reigon.setFixedWidth(200)
        h_layout_of_mix_and_region.addWidget(self.slider_reigon)

        self.label_of_reigon = QLabel("Reigon")
        # self.label_of_reigon.setFixedWidth(100)

        h_layout_of_mix_and_region.addWidget(self.label_of_reigon)
        h_layout_of_mix_and_region.addWidget(self.ft_pairs_label)
        h_layout_of_mix_and_region.addWidget(self.ft_pairs_combobox)

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

    
