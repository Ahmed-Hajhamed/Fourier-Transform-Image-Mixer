import sys

from matplotlib import container
from in_and_out_ui import InputImageUi, OutputImageUi, creat_separator
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QPushButton, QComboBox, QSlider, QFileDialog, QProgressBar, QGraphicsView, QGraphicsScene
)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
import numpy as np
class ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FT Magnitude/Phase Mixer or Emphasizer")
        self.setGeometry(100, 100, 1200, 800)

        
        h_layout_of_output_and_input = QHBoxLayout()
        grid_layout_of_input = QGridLayout()
        
        #input images 
        self.input_1 = InputImageUi()
        grid_layout_of_input.addLayout(self.input_1.v_layout_container, 0 , 0)
        
        self.input_2 = InputImageUi()
        grid_layout_of_input.addLayout(self.input_2.v_layout_container, 0 , 1)

        self.input_3 = InputImageUi()
        grid_layout_of_input.addLayout(self.input_3.v_layout_container, 1 , 0)

        self.input_4 = InputImageUi()
        grid_layout_of_input.addLayout(self.input_4.v_layout_container, 1 , 1)

        h_layout_of_output_and_input.addLayout(grid_layout_of_input)

        #separator between input and output
        separator = creat_separator("v")
        h_layout_of_output_and_input.addWidget(separator)

        #output images
        output = OutputImageUi()
        h_layout_of_output_and_input.addLayout(output.v_layout)

        h_layout_of_output_and_input.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(h_layout_of_output_and_input)
        self.setCentralWidget(container)
        self.input_1.load_image("C:\\Users\VICTUS\Downloads\IMG_20230807_000054_971.jpg")
        self.input_2.load_image("C:\\Users\VICTUS\Downloads\IMG_20230807_000054_971.jpg")
        self.input_3.load_image("C:\\Users\VICTUS\Downloads\IMG_20230807_000054_971.jpg")
        self.input_4.load_image("C:\\Users\VICTUS\Downloads\IMG_20230807_000054_971.jpg")
        self.input_1.label_of_original_image.mouseDoubleClickEvent()


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, "dark_medical.xml")
    window = ui()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
