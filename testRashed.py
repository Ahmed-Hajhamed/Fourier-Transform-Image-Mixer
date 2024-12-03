from PyQt5.QtWidgets import QLabel, QFileDialog

class FileLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Double-click to load a file")
        self.setStyleSheet("border: 1px solid black; padding: 5px;")
    
    def mouseDoubleClickEvent(self, event):
        # Open file dialog on double-click
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open File", 
            "", 
            "All Files (*.*);;Text Files (*.txt);;Images (*.png *.jpg)"
        )
        if file_path:
            self.setText(file_path)  # Update label text with the selected file path

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom QLabel with File Loading")
        self.resize(400, 200)

        # Set up layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Add custom QLabel
        self.file_label = FileLabel()
        layout.addWidget(self.file_label)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
