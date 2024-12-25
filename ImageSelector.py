from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
import numpy as np

class ImageSelector(QWidget):
    def __init__(self, pixmap = None, slider = None, label_size=(300, 400),  parent=None,label=None):
        super().__init__(parent)
        self.inner_indices = None
        self.outer_indices = None
        self.layout_ = QVBoxLayout(self)

        self.image_label = ImageLabelSelector()
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(*label_size)
        self.layout_.addWidget(self.image_label)

        self.slider=slider
        self.slider.valueChanged.connect(self.updateRectangleSize)

        if pixmap:
            self.setPixmap(QPixmap(pixmap))

    def setPixmap(self, pixmap):
        """
        Set or update the pixmap displayed in the QLabel.
        """
        self.image_label.setPixmap(pixmap)
        self.image_label.update()
        self.get_inner_region()
        self.get_outer_region()

    def updateRectangleSize(self, value):
        self.image_label.setRectSizePercentage(value)

    def get_inner_region(self):
        self.inner_indices =  self.image_label.getModifiedIndices(inner=True)
        if self.inner_indices is not None:
            print(f"inner:{self.inner_indices}")
        if self.outer_indices  is not None:
            print(f"ouer: {self.outer_indices}")

    def get_outer_region(self):
        self.outer_indices =  self.image_label.getModifiedIndices(inner=False)


class ImageLabelSelector(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect_percentage = 50  

    def setRectSizePercentage(self, percentage):
        self.rect_percentage = percentage
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmap():
            return

        painter = QPainter(self)
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        painter.setPen(pen)

        label_width = self.width()
        label_height = self.height()

        # Calculate the maximum size for the rectangle while maintaining the aspect ratio
        rect_width = label_width * self.rect_percentage / 100
        rect_height = label_height * self.rect_percentage / 100

        # Center the rectangle within the label
        rect_x = (label_width - rect_width) / 2
        rect_y = (label_height - rect_height) / 2

        # Create the QRect for the rectangle
        rect = QRect(int(rect_x), int(rect_y), int(rect_width), int(rect_height))

        # Draw the rectangle
        painter.drawRect(rect)
        painter.end()


    def getModifiedIndices(self, inner=True):
        pixmap = self.pixmap()
        if pixmap is None:
            return None

        image = pixmap.toImage()
        width, height = image.width(), image.height()

        rect_size = min(width, height) * self.rect_percentage / 100
        x1 = int((width - rect_size) / 2)
        y1 = int((height - rect_size) / 2)
        x2 = x1 + int(rect_size)
        y2 = y1 + int(rect_size)

        mask = np.zeros((height, width), dtype=bool)
        mask[y1:y2, x1:x2] = True

        if inner:
            return np.where(mask) 
        else:
            return np.where(~mask) 


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # Create an instance of ImageSelector
    window = ImageSelector("imgaes\IMG_20230807_000054_971.jpg")
    window.show()
    sys.exit(app.exec_())
