from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class ListNotesGui(QWidget):
    change_to_note_menu_signal = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("List Notes")
        self.controller = controller
        layout = QVBoxLayout()
        self.note_display = QTextEdit()
        self.note_display.setEnabled(False) #Disabling edits

        #back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_button_clicked)

        layout.addWidget(self.note_display)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_button_clicked(self):
        self.change_to_note_menu_signal.emit() #emit signal to go back to note menu