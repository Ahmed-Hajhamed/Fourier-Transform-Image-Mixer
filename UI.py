from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QProgressBar, QGridLayout,
                QComboBox, QRadioButton, QButtonGroup, QPushButton, QWidget)
from ImageProcessor import ImageProcessor
import InputImageLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("FT Image Mixer")
        MainWindow.resize(1000, 600)
        self.centralwidget = QWidget(MainWindow)
        self.main_gridLayout = QGridLayout(self.centralwidget)
        self.output_layout = QGridLayout()
        self.main_controls_layout = QGridLayout()
        self.selected_region_slider = InputImageLabel.create_slider(1, 90)

        line_1 = InputImageLabel.create_line(self.centralwidget)
        line_2 = InputImageLabel.create_line(self.centralwidget)
        line_3 = InputImageLabel.create_line(self.centralwidget)
        line_4 = InputImageLabel.create_line(self.centralwidget)
        line_5 = InputImageLabel.create_line(self.centralwidget, horizontal= True)
        line_6 = InputImageLabel.create_line(self.centralwidget, horizontal= True)
        line_7 = InputImageLabel.create_line(self.centralwidget)
        line_8 = InputImageLabel.create_line(self.centralwidget)
        line_9 = InputImageLabel.create_line(self.centralwidget, horizontal= True)

        self.image_1_label = InputImageLabel.InputImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.image_2_label = InputImageLabel.InputImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.image_3_label = InputImageLabel.InputImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.image_4_label = InputImageLabel.InputImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.image_labels = [self.image_1_label, self.image_2_label, self.image_3_label, self.image_4_label]

        self.output_1_label = QLabel(self.centralwidget)
        self.output_2_label = QLabel(self.centralwidget)
        self.select_region_label = QLabel(text= "Selected Region:")
        self.ft_pairs_label = QLabel("Reconstruction Pairs:")
        self.progress_label = QLabel("Mixing Progress:")

        self.output_1_image = ImageProcessor(self.output_1_label)
        self.output_2_image = ImageProcessor(self.output_2_label)

        self.group_button = QButtonGroup(self.centralwidget)
        self.output_1_radiobutton = create_radio_button(MainWindow, self.group_button ,state= True)
        self.output_2_radiobutton = create_radio_button(MainWindow, self.group_button)

        self.output_layout.addWidget(self.output_1_label, 0, 0)
        self.output_layout.addWidget(self.output_2_label, 0, 2)
        self.output_layout.addWidget(line_8, 0, 1, 2, 1)
        self.output_layout.addWidget(self.output_1_radiobutton, 1, 0, 2, 1)
        self.output_layout.addWidget(self.output_2_radiobutton, 1, 2, 2, 1)
        self.output_layout.addWidget(line_9, 2, 0, 1, 3)

        self.ft_pairs_combobox = QComboBox()
        self.ft_pairs_combobox.addItems(["Magnitude and Phase", "Real and Imaginary"])
        self.ft_pairs_combobox.currentIndexChanged.connect(MainWindow.change_reconstruction_pairs)

        self.mix_button = QPushButton()
        self.mix_button.setText("Mix Images")
        self.mix_button.clicked.connect(MainWindow.mix_images)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100) 
        self.progress_bar.setValue(0)

        self.group_button_inner_outer = QButtonGroup(self.centralwidget)
        self.inner_region_radio_button = create_radio_of_inner_outer(name="Inner Region",
                                                            gruop_button= self.group_button_inner_outer, state=True)
        self.outer_region_radio_button = create_radio_of_inner_outer(name="Outer Region",
                                                            gruop_button= self.group_button_inner_outer)
        self.sliders_weights_radio_button = create_radio_of_inner_outer(name="Sliders' Weight",
                                                            gruop_button= self.group_button_inner_outer)

        self.inner_region_radio_button.toggled.connect(MainWindow.mix_images)
        self.outer_region_radio_button.toggled.connect(MainWindow.mix_images)
        self.sliders_weights_radio_button.toggled.connect(MainWindow.mix_images)

        self.main_controls_layout.addWidget(self.mix_button, 0, 0, 1, 1)
        self.main_controls_layout.addWidget(line_7, 0, 1, 1, 1)
        self.main_controls_layout.addWidget(self.progress_label, 0, 2, 1, 1)
        self.main_controls_layout.addWidget(self.progress_bar, 0, 3, 1, 1)
        self.main_controls_layout.addWidget(self.select_region_label, 2, 0, 1, 1)
        self.main_controls_layout.addWidget(self.inner_region_radio_button, 1, 0, 1, 2)
        self.main_controls_layout.addWidget(self.outer_region_radio_button, 1, 1, 1, 2)
        self.main_controls_layout.addWidget(self.sliders_weights_radio_button, 1, 3, 1, 2)
        self.main_controls_layout.addWidget(self.selected_region_slider, 2, 2, 1, 2)
        self.main_controls_layout.addWidget(self.ft_pairs_label, 3, 0, 1, 1)
        self.main_controls_layout.addWidget(self.ft_pairs_combobox, 3, 2, 1, 2)

        self.main_gridLayout.addLayout(self.image_1_label.image_layout, 0, 0)
        self.main_gridLayout.addLayout(self.image_2_label.image_layout, 0, 2)
        self.main_gridLayout.addLayout(self.image_3_label.image_layout, 2, 0)
        self.main_gridLayout.addLayout(self.image_4_label.image_layout, 2, 2)
        self.main_gridLayout.addLayout(self.output_layout, 0, 4, 1, 1)
        self.main_gridLayout.addLayout(self.main_controls_layout, 1, 4, 2, 1)
        self.main_gridLayout.addWidget(line_1, 0, 3, 1, 1)
        self.main_gridLayout.addWidget(line_2, 2, 3, 1, 1)
        self.main_gridLayout.addWidget(line_3, 0, 1, 1, 1)
        self.main_gridLayout.addWidget(line_4, 2, 1, 1, 2)
        self.main_gridLayout.addWidget(line_5, 1, 0, 1, 1)
        self.main_gridLayout.addWidget(line_6, 1, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


def create_radio_button(MainWindow, gruop_button, state = False):
    radio_button = QRadioButton()
    radio_button.setText("Show")
    radio_button.setChecked(state)
    radio_button.toggled.connect(MainWindow.switch_output_label)
    gruop_button.addButton(radio_button)
    return radio_button

def create_radio_of_inner_outer(name, gruop_button, state = False):
    radio_button = QRadioButton()
    radio_button.setText(name)
    radio_button.setChecked(state)
    gruop_button.addButton(radio_button)
    return radio_button
