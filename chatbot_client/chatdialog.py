from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSizePolicy, QScrollArea
from PyQt6.QtCore import Qt, QTimer

class ChatText(QLabel):
    def __init__(self, text, is_self, width):
        super().__init__(text)
        
        if is_self:
            self.setStyleSheet("background-color: #3498db; font-size: 16px; color: white; padding: 10px; border-radius: 10px;")
        else:
            self.setStyleSheet("background-color: #807986; font-size: 16px; color: white; padding: 10px; border-radius: 10px;")

        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        fixed_width = int(width * 0.6)
        self.setFixedWidth(fixed_width)

class ChatBubble(QWidget):
    def __init__(self, text, is_self, align_flags):
        super().__init__()

        text = ChatText(text, is_self, self.width())
        
        layout = QHBoxLayout()
        layout.setAlignment(align_flags)
        layout.addWidget(text)  
        
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

class ChatDialog(QWidget):
    def __init__(self):    
        super().__init__()
        
        self.widget_area = QScrollArea()
        self.widget_area.setWidgetResizable(True)
        
        self.text_layout = QVBoxLayout()
        self.text_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        text_container = QWidget()
        text_container.setLayout(self.text_layout)
        
        self.widget_area.setWidget(text_container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.widget_area)
        
    def addSelfDialog(self, text):
        text = ChatBubble(text, True, Qt.AlignmentFlag.AlignRight)
        self.text_layout.addWidget(text)
        
        QTimer.singleShot(0, self.scroll_to_bottom)  # Delay scrolling
        
    def addOtherDialog(self, text):
        text = ChatBubble(text, False, Qt.AlignmentFlag.AlignLeft)
        self.text_layout.addWidget(text)

        QTimer.singleShot(0, self.scroll_to_bottom)  # Delay scrolling
        
    def scroll_to_bottom(self):
        scrollbar = self.widget_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        