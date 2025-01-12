from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class AddNoteGui(QWidget):
    change_to_note_menu_signal = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Appointment")
        self.controller = controller
        layout = QVBoxLayout()
        self.note_input = QTextEdit()
        self.refresh_input() #refresh input box
        self.note_input.textChanged.connect(self.note_entered)

        #add note button
        self.add_note_button = QPushButton("Add Note")
        self.add_note_button.setEnabled(False) #initial state
        self.add_note_button.clicked.connect(self.add_note_button_clicked)

        #back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_button_clicked)

        layout.addWidget(self.note_input)
        layout.addWidget(self.add_note_button)


        self.setLayout(layout)

    def refresh_input(self):
        self.note_input.setText("") #clear text
        self.note_input.setPlaceholderText("Enter note") #set Placeholder

    def note_entered(self):
        self.add_note_button.setEnabled(True)

    def back_button_clicked(self):
        self.refresh_input() 
        self.change_to_note_menu_signal.emit() #emit signal to go back to note menu
        
    def add_note_button_clicked(self):
        text = self.note_input.toPlainText()
        self.controller.create_note(text)
        dlg = QMessageBox()
        dlg.setWindowTitle("Note added")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText("Note successfully added!")
        dlg.exec()
        self.back_button_clicked()