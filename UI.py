from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QProgressBar
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtCore import Qt
from Image import Image

class ImageLabel(QLabel):
    def __init__(self, magnitude_real_slider, phase_imaginary_slider, image_ft_label,
                        magnitude_real_label, phase_imaginary_label, parent=None):
        super().__init__(parent)
        self.image = Image(self)
        self.image.load_image("imgaes\IMG_20230807_000054_971.jpg")
        self.last_mouse_pos = QPoint()
        self.ft_label = image_ft_label
        self.magnitude_real_slider = magnitude_real_slider
        self.phase_imaginary_slider = phase_imaginary_slider
        self.magnitude_real_label = magnitude_real_label
        self.phase_imaginary_label = phase_imaginary_label
        self.magnitude_real_label.setText("Magnitude")
        self.phase_imaginary_label.setText("Phase")

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

        ft_combobox_components = ["Magnitude", "Phase", "Real", "Imaginary"]

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.image_1_2_h_layout = QtWidgets.QHBoxLayout()
        self.image_1_2_h_layout.setObjectName("image_1_2_h_layout")
    
        self.image_1_ft_label = QtWidgets.QLabel(self.centralwidget)
        self.image_1_ft_label.setText("")
        self.image_1_ft_label.setObjectName("image_1_ft_label")

        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        self.image_2_ft_label = QtWidgets.QLabel(self.centralwidget)
        self.image_2_ft_label.setText("")
        self.image_2_ft_label.setObjectName("image_2_ft_label")

        self.gridLayout_4.addLayout(self.image_1_2_h_layout, 0, 0, 1, 1)
        self.image_3_4_controls_layout = QtWidgets.QGridLayout()
        self.image_3_4_controls_layout.setObjectName("image_3_4_controls_layout")

        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.image_3_4_controls_layout.addWidget(self.line_6, 0, 5, 2, 1)

        self.line_12 = QtWidgets.QFrame(self.centralwidget)
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.image_3_4_controls_layout.addWidget(self.line_12, 0, 2, 2, 1)

        self.image_3_ft_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.image_3_ft_combobox.setObjectName("image_3_ft_combobox")
        self.image_3_ft_combobox.addItems(ft_combobox_components)
        self.image_3_4_controls_layout.addWidget(self.image_3_ft_combobox, 0, 4, 2, 1)

        self.image_4_ft_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.image_4_ft_combobox.setObjectName("image_4_ft_combobox")
        self.image_4_ft_combobox.addItems(ft_combobox_components)

        self.image_3_4_controls_layout.addWidget(self.image_4_ft_combobox, 0, 10, 2, 1)

        self.image_3_ft_combobox_label = QtWidgets.QLabel(self.centralwidget)
        self.image_3_ft_combobox_label.setObjectName("image_3_ft_combobox_label")
        self.image_3_4_controls_layout.addWidget(self.image_3_ft_combobox_label, 0, 3, 2, 1)

        self.image_4_ft_combobox_label = QtWidgets.QLabel(self.centralwidget)
        self.image_4_ft_combobox_label.setObjectName("image_4_ft_combobox_label")
        self.image_3_4_controls_layout.addWidget(self.image_4_ft_combobox_label, 0, 9, 2, 1)

        self.image_4_magnitude_real_label = QtWidgets.QLabel(self.centralwidget)
        self.image_4_magnitude_real_label.setObjectName("image_4_magnitude_real_label")
        self.image_3_4_controls_layout.addWidget(self.image_4_magnitude_real_label, 0, 6, 1, 1)

        self.image_3_magnitude_real_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_3_magnitude_real_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_3_magnitude_real_slider.setObjectName("image_3_magnitude_real_slider")
        self.image_3_4_controls_layout.addWidget(self.image_3_magnitude_real_slider, 0, 1, 1, 1)

        self.image_4_phase_imaginary_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_4_phase_imaginary_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_4_phase_imaginary_slider.setObjectName("image_4_phase_imaginary_slider")
        self.image_3_4_controls_layout.addWidget(self.image_4_phase_imaginary_slider, 1, 7, 1, 1)

        self.image_3_magnitude_real_label = QtWidgets.QLabel(self.centralwidget)
        self.image_3_magnitude_real_label.setObjectName("image_3_magnitude_real_label")
        self.image_3_4_controls_layout.addWidget(self.image_3_magnitude_real_label, 0, 0, 1, 1)

        self.image_4_magnitude_real_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_4_magnitude_real_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_4_magnitude_real_slider.setObjectName("image_4_magnitude_real_slider")
        self.image_3_4_controls_layout.addWidget(self.image_4_magnitude_real_slider, 0, 7, 1, 1)

        self.image_3_phase_imaginary_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_3_phase_imaginary_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_3_phase_imaginary_slider.setObjectName("image_3_phase_imaginary_slider")
        self.image_3_4_controls_layout.addWidget(self.image_3_phase_imaginary_slider, 1, 1, 1, 1)

        self.image_4_phase_imaginary_label = QtWidgets.QLabel(self.centralwidget)
        self.image_4_phase_imaginary_label.setObjectName("image_4_phase_imaginary_label")
        self.image_3_4_controls_layout.addWidget(self.image_4_phase_imaginary_label, 1, 6, 1, 1)

        self.image_3_phase_imaginary_label = QtWidgets.QLabel(self.centralwidget)
        self.image_3_phase_imaginary_label.setObjectName("image_3_phase_imaginary_label")
        self.image_3_4_controls_layout.addWidget(self.image_3_phase_imaginary_label, 1, 0, 1, 1)

        self.line_13 = QtWidgets.QFrame(self.centralwidget)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.image_3_4_controls_layout.addWidget(self.line_13, 0, 8, 2, 1)

        self.gridLayout_4.addLayout(self.image_3_4_controls_layout, 3, 0, 1, 1)
        self.image_1_2_controls_layout = QtWidgets.QGridLayout()
        self.image_1_2_controls_layout.setObjectName("image_1_2_controls_layout")

        self.line_10 = QtWidgets.QFrame(self.centralwidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.image_1_2_controls_layout.addWidget(self.line_10, 0, 2, 2, 1)

        self.image_1_magnitude_real_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_1_magnitude_real_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_1_magnitude_real_slider.setObjectName("image_1_magnitude_real_slider")
        self.image_1_2_controls_layout.addWidget(self.image_1_magnitude_real_slider, 0, 1, 1, 1)

        self.image_2_ft_combobox_label = QtWidgets.QLabel(self.centralwidget)
        self.image_2_ft_combobox_label.setObjectName("image_2_ft_combobox_label")
        self.image_1_2_controls_layout.addWidget(self.image_2_ft_combobox_label, 0, 9, 2, 1)

        self.image_2_magnitude_real_label = QtWidgets.QLabel(self.centralwidget)
        self.image_2_magnitude_real_label.setObjectName("image_2_magnitude_real_label")
        self.image_1_2_controls_layout.addWidget(self.image_2_magnitude_real_label, 0, 6, 1, 1)

        self.image_2_phase_imaginary_label = QtWidgets.QLabel(self.centralwidget)
        self.image_2_phase_imaginary_label.setObjectName("image_2_phase_imaginary_label")
        self.image_1_2_controls_layout.addWidget(self.image_2_phase_imaginary_label, 1, 6, 1, 1)

        self.image_1_magnitude_real_label = QtWidgets.QLabel(self.centralwidget)
        self.image_1_magnitude_real_label.setObjectName("image_1_magnitude_real_label")
        self.image_1_2_controls_layout.addWidget(self.image_1_magnitude_real_label, 0, 0, 1, 1)

        self.image_1_phase_imaginary_label = QtWidgets.QLabel(self.centralwidget)
        self.image_1_phase_imaginary_label.setObjectName("image_1_phase_imaginary_label")
        self.image_1_2_controls_layout.addWidget(self.image_1_phase_imaginary_label, 1, 0, 1, 1)

        self.image_2_phase_imaginary_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_2_phase_imaginary_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_2_phase_imaginary_slider.setObjectName("image_2_phase_imaginary_slider")
        self.image_1_2_controls_layout.addWidget(self.image_2_phase_imaginary_slider, 1, 7, 1, 1)

        self.image_1_phase_imaginary_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_1_phase_imaginary_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_1_phase_imaginary_slider.setObjectName("image_1_phase_imaginary_slider")
        self.image_1_2_controls_layout.addWidget(self.image_1_phase_imaginary_slider, 1, 1, 1, 1)

        self.image_2_ft_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.image_2_ft_combobox.setObjectName("image_2_ft_combobox")
        self.image_2_ft_combobox.addItems(ft_combobox_components)
        self.image_1_2_controls_layout.addWidget(self.image_2_ft_combobox, 0, 10, 2, 1)

        self.image_2_magnitude_real_slider = QtWidgets.QSlider(self.centralwidget)
        self.image_2_magnitude_real_slider.setOrientation(QtCore.Qt.Horizontal)
        self.image_2_magnitude_real_slider.setObjectName("image_2_magnitude_real_slider")
        self.image_1_2_controls_layout.addWidget(self.image_2_magnitude_real_slider, 0, 7, 1, 1)

        self.image_1_ft_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.image_1_ft_combobox.setObjectName("image_1_ft_combobox")
        self.image_1_ft_combobox.addItems(ft_combobox_components)

        self.image_1_2_controls_layout.addWidget(self.image_1_ft_combobox, 0, 4, 2, 1)

        self.image_1_ft_combobox_label = QtWidgets.QLabel(self.centralwidget)
        self.image_1_ft_combobox_label.setObjectName("image_1_ft_combobox_label")
        self.image_1_2_controls_layout.addWidget(self.image_1_ft_combobox_label, 0, 3, 2, 1)

        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.image_1_2_controls_layout.addWidget(self.line_4, 0, 5, 2, 1)

        self.line_11 = QtWidgets.QFrame(self.centralwidget)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.image_1_2_controls_layout.addWidget(self.line_11, 0, 8, 2, 1)

        self.gridLayout_4.addLayout(self.image_1_2_controls_layout, 1, 0, 1, 1)
        self.image_2_3_h_layout = QtWidgets.QHBoxLayout()
        self.image_2_3_h_layout.setObjectName("image_2_3_h_layout")

        self.image_3_ft_label = QtWidgets.QLabel(self.centralwidget)
        self.image_3_ft_label.setText("")
        self.image_3_ft_label.setObjectName("image_3_ft_label")

        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")

        self.image_4_ft_label = QtWidgets.QLabel(self.centralwidget)
        self.image_4_ft_label.setText("")
        self.image_4_ft_label.setObjectName("image_4_ft_label")

        self.gridLayout_4.addLayout(self.image_2_3_h_layout, 2, 0, 1, 1)
        self.output_v_layout = QtWidgets.QVBoxLayout()
        self.output_v_layout.setObjectName("output_v_layout")

        self.output_1_label = QtWidgets.QLabel(self.centralwidget)
        self.output_1_label.setText("")
        self.output_1_label.setObjectName("output_1_label")

        self.output_2_label = QtWidgets.QLabel(self.centralwidget)
        self.output_2_label.setText("")
        self.output_2_label.setObjectName("output_2_label")

        self.output_1_image = Image(self.output_1_label)
        self.output_2_image = Image(self.output_2_label)

        self.output_v_layout.addWidget(self.output_1_label)
        self.output_1_radiobutton = QtWidgets.QRadioButton(self.centralwidget)
        self.output_1_radiobutton.setObjectName("output_1_checkbox")
        self.output_1_radiobutton.setChecked(True)
        self.output_1_radiobutton.toggled.connect(MainWindow.switch_output_label)
        self.output_v_layout.addWidget(self.output_1_radiobutton)

        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.output_v_layout.addWidget(self.line_8)


        self.output_v_layout.addWidget(self.output_2_label)
        self.output_2_radiobutton = QtWidgets.QRadioButton(self.centralwidget)
        self.output_2_radiobutton.setObjectName("output_2_checkbox")
        self.output_2_radiobutton.setChecked(False)
        self.output_2_radiobutton.toggled.connect(MainWindow.switch_output_label)
        self.output_v_layout.addWidget(self.output_2_radiobutton)

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.output_v_layout.addWidget(self.line_2)

        self.gridLayout_4.addLayout(self.output_v_layout, 0, 2, 3, 1)
        self.main_controls_layout = QtWidgets.QGridLayout()
        self.main_controls_layout.setObjectName("main_controls_layout")

        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.main_controls_layout.addWidget(self.line_7, 0, 4, 1, 1)

        self.select_region_label = QtWidgets.QLabel(self.centralwidget)
        self.select_region_label.setObjectName("select_region_label")
        self.main_controls_layout.addWidget(self.select_region_label, 0, 2, 1, 1)

        self.select_region_label_2 = QtWidgets.QSlider(self.centralwidget)
        self.select_region_label_2.setOrientation(QtCore.Qt.Horizontal)
        self.select_region_label_2.setObjectName("select_region_label_2")
        self.main_controls_layout.addWidget(self.select_region_label_2, 0, 3, 1, 1)

        self.ft_pairs_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.ft_pairs_combobox.setObjectName("ft_pairs_combobox")
        self.ft_pairs_combobox.addItems(["Magnitude and Phase", "Real and Imaginary"])

        self.main_controls_layout.addWidget(self.ft_pairs_combobox, 0, 6, 1, 1)
        self.mix_button = QtWidgets.QPushButton(self.centralwidget)
        self.mix_button.setObjectName("mix_button")
        self.main_controls_layout.addWidget(self.mix_button, 0, 0, 1, 1)
        self.ft_pairs_label = QtWidgets.QLabel(self.centralwidget)
        self.ft_pairs_label.setObjectName("ft_pairs_label")
        self.main_controls_layout.addWidget(self.ft_pairs_label, 0, 5, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.main_controls_layout.addWidget(self.line_9, 0, 1, 1, 1)


        self.progress_label = QLabel("Mixing Progress:")

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setRange(0, 100) 
        self.progress_bar.setValue(0)

        self.main_controls_layout.addWidget(self.progress_label, 1, 0, 1, 1)
        self.main_controls_layout.addWidget(self.progress_bar, 1, 1, 1, 6)

        self.gridLayout_4.addLayout(self.main_controls_layout, 3, 2, 1, 1)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 0, 1, 4, 1)

        self.image_1_label = ImageLabel(self.image_1_magnitude_real_slider, self.image_1_phase_imaginary_slider,
                                        self.image_1_ft_label, self.image_1_magnitude_real_label, self.image_1_phase_imaginary_label, self.centralwidget)
        self.image_1_label.setText("")
        self.image_1_label.setObjectName("image_1_label")
        self.image_1_2_h_layout.addWidget(self.image_1_label)
        self.image_1_2_h_layout.addWidget(self.image_1_ft_label)
        self.image_1_2_h_layout.addWidget(self.line_3)

        self.image_2_label = ImageLabel(self.image_2_magnitude_real_slider, self.image_2_phase_imaginary_slider,
                                        self.image_2_ft_label, self.image_2_magnitude_real_label, self.image_2_phase_imaginary_label, self.centralwidget)
        self.image_2_label.setText("")
        self.image_2_label.setObjectName("image_2_label")
        self.image_1_2_h_layout.addWidget(self.image_2_label)
        self.image_1_2_h_layout.addWidget(self.image_2_ft_label)

        self.image_3_label = ImageLabel(self.image_3_magnitude_real_slider, self.image_3_phase_imaginary_slider,
                                        self.image_3_ft_label, self.image_3_magnitude_real_label, self.image_3_phase_imaginary_label, self.centralwidget)
        self.image_3_label.setText("")
        self.image_3_label.setObjectName("image_3_label")
        self.image_2_3_h_layout.addWidget(self.image_3_label)
        self.image_2_3_h_layout.addWidget(self.image_3_ft_label)
        self.image_2_3_h_layout.addWidget(self.line_5)

        self.image_4_label = ImageLabel(self.image_4_magnitude_real_slider, self.image_4_phase_imaginary_slider,
                                        self.image_4_ft_label, self.image_4_magnitude_real_label, self.image_4_phase_imaginary_label, self.centralwidget)
        self.image_4_label.setText("")
        self.image_4_label.setObjectName("image_4_label")
        self.image_2_3_h_layout.addWidget(self.image_4_label)
        self.image_2_3_h_layout.addWidget(self.image_4_ft_label)

        self.images = [self.image_1_label, self.image_2_label, 
                         self.image_3_label, self.image_4_label]

        self.mix_button.clicked.connect(lambda: MainWindow.mix_images(self.images))

        self.ft_pairs_combobox.currentIndexChanged.connect(lambda:MainWindow.change_reconstruction_pairs(self.images))

        self.image_1_ft_combobox.currentIndexChanged.connect(lambda:MainWindow.change_ft_component(self.image_1_label.image, 
                                                                                            self.image_1_ft_label))
        
        self.image_2_ft_combobox.currentIndexChanged.connect(lambda:MainWindow.change_ft_component(self.image_2_label.image, 
                                                                                            self.image_2_ft_label))
        
        self.image_3_ft_combobox.currentIndexChanged.connect(lambda:MainWindow.change_ft_component(self.image_3_label.image, 
                                                                                            self.image_3_ft_label))
        
        self.image_4_ft_combobox.currentIndexChanged.connect(lambda:MainWindow.change_ft_component(self.image_4_label.image, 
                                                                                            self.image_4_ft_label))

        self.output_1_label.setScaledContents(True)
        self.output_2_label.setScaledContents(True)
        
        self.output_1_label.setFixedSize(300, 400)
        self.output_2_label.setFixedSize(300, 400)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1233, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("FT Image Mixer", "FT Image Mixer"))
        self.image_3_ft_combobox_label.setText(_translate("MainWindow", "FT Component"))
        self.image_4_ft_combobox_label.setText(_translate("MainWindow", "FT Component"))
        self.image_2_ft_combobox_label.setText(_translate("MainWindow", "FT Componet"))
        self.image_1_ft_combobox_label.setText(_translate("MainWindow", "FT Component"))
        self.output_1_radiobutton.setText(_translate("MainWindow", "Show"))
        self.output_2_radiobutton.setText(_translate("MainWindow", "Show"))
        self.select_region_label.setText(_translate("MainWindow", "Region:"))
        self.mix_button.setText(_translate("MainWindow", "Mix"))
        self.ft_pairs_label.setText(_translate("MainWindow", "FT Pairs"))
