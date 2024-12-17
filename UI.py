from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QProgressBar, QSlider, QGridLayout,
                QFrame, QComboBox, QVBoxLayout, QRadioButton, QPushButton, QWidget)
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
import Image
ft_combobox_components = ["Magnitude", "Phase", "Real", "Imaginary"]

class ImageLabel(QLabel):
    def __init__(self, MainWindow, parent=None):
        super().__init__(parent)
        self.image = Image.Image(self)
        self.image.load_image("imgaes\IMG_20230807_000054_971.jpg")
        self.last_mouse_pos = QPoint()
        self.ft_label = QLabel()
        magnitude_8bit = Image.normalize_to_8bit(self.image.magnitude_log)
        mag_pixmap = Image.array_to_pixmap(magnitude_8bit)
        self.ft_label.setPixmap(mag_pixmap)

        self.magnitude_real_slider = QSlider()
        self.magnitude_real_slider.setOrientation(Qt.Horizontal)
        self.phase_imaginary_slider = QSlider()
        self.phase_imaginary_slider.setOrientation(Qt.Horizontal)

        self.magnitude_real_label = QLabel("Magnitude")
        self.phase_imaginary_label = QLabel("Phase")
        combobox_label = QLabel("FT Component:")

        self.ft_combobox = QComboBox()
        self.ft_combobox.addItems(ft_combobox_components)
        self.ft_combobox.currentIndexChanged.connect(lambda: MainWindow.change_ft_component(self.image, self.ft_label))

        self.magnitude_real_slider.setMinimum(10)
        self.magnitude_real_slider.setMaximum(200)
        self.magnitude_real_slider.setValue(100)
        self.magnitude_real_slider.setMaximumWidth(200)

        self.phase_imaginary_slider.setMinimum(10)
        self.phase_imaginary_slider.setMaximum(200)
        self.phase_imaginary_slider.setValue(100)
        self.phase_imaginary_slider.setMaximumWidth(200)

        self.setFixedSize(300,400)
        self.ft_label.setFixedSize(300,400)
        self.setScaledContents(True)
        self.ft_label.setScaledContents(True)

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)

        self.image_layout = QGridLayout()
        self.image_layout.addWidget(self, 0, 0, 1, 2)
        self.image_layout.addWidget(self.ft_label, 0, 3, 1, 2)
        self.image_layout.addWidget(self.magnitude_real_label, 1, 0)
        self.image_layout.addWidget(self.magnitude_real_slider, 1, 1)
        self.image_layout.addWidget(line, 1, 2, 2, 1)
        self.image_layout.addWidget(combobox_label, 1, 3, 2, 1)
        self.image_layout.addWidget(self.ft_combobox, 1, 4, 2, 1)

        self.image_layout.addWidget(self.phase_imaginary_label, 2, 0)
        self.image_layout.addWidget(self.phase_imaginary_slider, 2, 1)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.image.load_image()

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1233, 799)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_gridLayout = QGridLayout(self.centralwidget)
        self.main_gridLayout.setObjectName("main_layout")

        self.image_1_label = ImageLabel(MainWindow, self.centralwidget)
        self.image_2_label = ImageLabel(MainWindow, self.centralwidget)
        self.image_3_label = ImageLabel(MainWindow, self.centralwidget)
        self.image_4_label = ImageLabel(MainWindow, self.centralwidget)

        self.main_gridLayout.addLayout(self.image_1_label.image_layout, 0, 0)
        self.main_gridLayout.addLayout(self.image_2_label.image_layout, 0, 2)
        self.main_gridLayout.addLayout(self.image_3_label.image_layout, 1, 0)
        self.main_gridLayout.addLayout(self.image_4_label.image_layout, 1, 2)

        self.output_layout = QGridLayout()
        self.output_layout.setObjectName("output_v_layout")

        self.output_1_label = QLabel(self.centralwidget)
        self.output_1_label.setText("")
        self.output_1_label.setObjectName("output_1_label")

        self.output_2_label = QLabel(self.centralwidget)
        self.output_2_label.setText("")
        self.output_2_label.setObjectName("output_2_label")

        self.output_1_image = Image.Image(self.output_1_label)
        self.output_2_image = Image.Image(self.output_2_label)

        self.output_layout.addWidget(self.output_1_label, 0, 0)

        self.output_1_radiobutton = QRadioButton(self.centralwidget)
        self.output_1_radiobutton.setText("Show")
        self.output_1_radiobutton.setChecked(True)
        self.output_1_radiobutton.toggled.connect(MainWindow.switch_output_label)
        self.output_layout.addWidget(self.output_1_radiobutton, 1, 0)

        self.line_8 = QFrame(self.centralwidget)
        self.line_8.setFrameShape(QFrame.VLine)
        self.line_8.setFrameShadow(QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.output_layout.addWidget(self.line_8, 0, 1, 2, 1)


        self.output_layout.addWidget(self.output_2_label, 0, 2)

        self.output_2_radiobutton = QRadioButton(self.centralwidget)
        self.output_2_radiobutton.setText("Show")
        self.output_2_radiobutton.setChecked(False)
        self.output_2_radiobutton.toggled.connect(MainWindow.switch_output_label)
        self.output_layout.addWidget(self.output_2_radiobutton, 1, 2)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.output_layout.addWidget(self.line_2, 2, 0, 1, 3)


        self.main_gridLayout.addLayout(self.output_layout, 0, 3, 1, 1)
        self.main_controls_layout = QGridLayout()

        self.line_7 = QFrame(self.centralwidget)
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)
        self.line_7.setObjectName("line_7")

        self.select_region_label = QLabel(text= "Region",parent= self.centralwidget)
        self.select_region_label.setObjectName("select_region_label")

        self.select_region_slider = QSlider(self.centralwidget)
        self.select_region_slider.setOrientation(Qt.Horizontal)
        self.select_region_slider.setObjectName("select_region_label_2")

        self.ft_pairs_combobox = QComboBox(self.centralwidget)
        self.ft_pairs_combobox.setObjectName("ft_pairs_combobox")
        self.ft_pairs_combobox.addItems(["Magnitude and Phase", "Real and Imaginary"])

        self.mix_button = QPushButton(self.centralwidget)
        self.mix_button.setText("Mix")

        self.ft_pairs_label = QLabel(self.centralwidget)
        self.ft_pairs_label.setText("FT Pairs")
        self.line_9 = QFrame(self.centralwidget)
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)
        self.line_9.setObjectName("line_9")


        self.progress_label = QLabel("Mixing Progress:")

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setRange(0, 100) 
        self.progress_bar.setValue(0)

        self.main_controls_layout.addWidget(self.mix_button, 0, 0, 1, 1)
        self.main_controls_layout.addWidget(self.line_9, 0, 1, 1, 1)
        self.main_controls_layout.addWidget(self.progress_label, 0, 2, 1, 1)
        self.main_controls_layout.addWidget(self.progress_bar, 0, 3, 1, 1)

        self.main_controls_layout.addWidget(self.select_region_label, 2, 0, 1, 1)
        self.main_controls_layout.addWidget(self.select_region_slider, 2, 2, 1, 1)

        # self.main_controls_layout.addWidget(self.line_7, 2, 1, 1, 1)

        self.main_controls_layout.addWidget(self.ft_pairs_label, 3, 0, 1, 1)
        self.main_controls_layout.addWidget(self.ft_pairs_combobox, 3, 1, 1, 1)

        self.main_gridLayout.addLayout(self.main_controls_layout, 1, 3, 2, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.main_gridLayout.addWidget(self.line, 0, 1, 2, 1)

        self.images = [self.image_1_label, self.image_2_label, 
                         self.image_3_label, self.image_4_label]

        self.mix_button.clicked.connect(lambda: MainWindow.mix_images(self.images))

        self.ft_pairs_combobox.currentIndexChanged.connect(lambda:MainWindow.change_reconstruction_pairs(self.images))

        self.output_1_label.setScaledContents(True)
        self.output_2_label.setScaledContents(True)
        
        self.output_1_label.setFixedSize(300, 400)
        self.output_2_label.setFixedSize(300, 400)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
