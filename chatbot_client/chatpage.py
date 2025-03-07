from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt

from chatdialog import ChatDialog

import globals
import messaging.packet as packet

import globals

class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        self.__create_page()
        
    def __create_page(self):
        self.dialog = ChatDialog()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Ask anything')
        self.input_field.setStyleSheet("font-size: 18px; padding: 6px;") 
        self.input_field.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Enter")
        self.send_button.setStyleSheet("font-size: 18px; padding: 6px;") 
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.dialog)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def send_message(self):
        if globals.cli.connected == False:
            return

        message = self.input_field.text()

        self.dialog.addSelfDialog(message)

        message_packet = packet.SendMessagePacket()
        message_packet.write_packet(message)
        globals.cli.send(message_packet)

        self.input_field.setText("")

    def resizeEvent(self, e):
        super().resizeEvent(e)

        h = int(self.height() * 0.85)
        self.dialog.setFixedHeight(h)
        

        