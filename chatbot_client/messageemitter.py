from PyQt6.QtCore import QObject, pyqtSignal

class MessageEmitter(QObject):
    message_recv_signal: pyqtSignal = pyqtSignal(str)

    def invoke(self, message:str):
        self.message_recv_signal.emit(message)