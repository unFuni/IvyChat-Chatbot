from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

class InfoPage(QWidget):

    def __init__(self):
        super().__init__()

        self.__create_page()

    def __create_page(self):

        title_label = QLabel("About Page")
        title_label.setStyleSheet("font-size: 20px;")

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)