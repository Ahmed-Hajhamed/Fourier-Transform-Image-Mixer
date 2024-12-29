import ImageProcessor
import ImageSelector
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QLabel, QGridLayout, QComboBox, QFrame, QSlider
from PyQt5.QtCore import Qt
FT_COMPONENTS = [["Magnitude", "Phase"], ["Real", "Imaginary"]]


class InputImageLabel(QLabel):
    def __init__(self, MainWindow, region_slider, parent=None, removable = False):
        super().__init__(parent)
        self.MainWindow = MainWindow
        self.removable = removable
        self.image = ImageProcessor.ImageProcessor(self)
        self.image.load_image("imgaes/Screen Shot 2024-11-10 at 10.27.12 AM.png")
        self.image.resize_image()
        self.last_mouse_pos = QPoint()
        self.ft_label = ImageSelector.ImageSelector(slider= region_slider)
        
        self.weight_slider = create_slider(1, 200)
        line = create_line()

        self.ft_pair_label = QLabel("Weight:")
        combobox_label = QLabel("FT Component:")

        self.ft_combobox = QComboBox()
        self.ft_combobox.addItems(FT_COMPONENTS[0])
        self.ft_combobox.currentIndexChanged.connect(lambda: MainWindow.change_ft_component(
                        self.ft_combobox.currentText(), self.image, self.ft_label))
        
        self.weight_slider.valueChanged.connect(MainWindow.mix_images)

        MainWindow.change_ft_component(self.ft_combobox.currentText(), self.image, self.ft_label)

        self.image_layout = QGridLayout()
        self.image_layout.addWidget(self, 0, 0, 1, 2)
        self.image_layout.addWidget(self.ft_label, 0, 3, 1, 2)
        self.image_layout.addWidget(self.ft_pair_label, 1, 0, 2, 1)
        self.image_layout.addWidget(self.weight_slider, 1, 1, 2, 1)
        self.image_layout.addWidget(line, 1, 2, 2, 1)
        self.image_layout.addWidget(combobox_label, 1, 3, 2, 1)
        self.image_layout.addWidget(self.ft_combobox, 1, 4, 2, 1)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.image.load_image()

        elif event.button() == Qt.RightButton and self.removable:
            self.image.image = None
            self.image.update_display()

        self.MainWindow.resize_images()
        self.MainWindow.change_ft_component(self.ft_combobox.currentText(), self.image, self.ft_label)
        self.weight_slider.setValue(100)
        # self.phase_imaginary_slider.setValue(100)

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
            new_contrast = max(0.1, self.in_con + delta.x()/10 * 0.01) 
            brightness_min, brightness_max = -50, 50  
            contrast_min, contrast_max = 0.5, 2.0  
            self.image.brightness = max(brightness_min, min(brightness_max, new_brightness))
            self.image.contrast = max(contrast_min, min(contrast_max, new_contrast))
            self.image.adjust_brightness_contrast()


def create_line(horizontal = False, thick = True):
        line = QFrame() 
        line.setFrameShape(QFrame.HLine) if horizontal else line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        if thick: line.setStyleSheet("border: 1px solid purple;")
        return line

def create_slider(minimum, maximum):
    slider = QSlider()
    slider.setOrientation(Qt.Horizontal)
    slider.setMinimum(minimum)
    slider.setMaximum(maximum)
    slider.setValue(maximum // 2)
    return slider
