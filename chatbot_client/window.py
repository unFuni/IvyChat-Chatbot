from PyQt6.QtWidgets import QStackedWidget, QPushButton, QLabel, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from chatpage import ChatPage
from infopage import InfoPage
from settingspage import SettingsPage

import globals

class MainWindow():

    def __init__(self):

        self.window = QMainWindow()

        self.main_widget = QWidget()

        self.window.setCentralWidget(self.main_widget)

        self.chat_page = ChatPage()
        self.setting_page = SettingsPage()
        self.info_page = InfoPage()

        self.__create_window()

    def __create_window(self):
        self.window.setWindowTitle("Chatbot Client")
        self.window.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout(self.main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        btn_home = QPushButton("Chat")
        btn_settings = QPushButton("Settings")
        btn_about = QPushButton("About")

        sidebar = QWidget()
        sidebar.setFixedWidth(140)
        sidebar.setStyleSheet("background-color: #333;")  
        sidebar_layout = QVBoxLayout(sidebar)

        for btn in [btn_home, btn_settings, btn_about]:
            btn.setStyleSheet("""
                background-color: #555;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;""")
            
            sidebar_layout.addWidget(btn)

        self.pages = QStackedWidget()

        self.pages.addWidget(self.chat_page)
        self.pages.addWidget(self.setting_page)
        self.pages.addWidget(self.info_page)

        btn_home.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        btn_settings.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        btn_about.clicked.connect(lambda: self.pages.setCurrentIndex(2))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)  # Content takes remaining space

    def show(self):
        self.window.show()
