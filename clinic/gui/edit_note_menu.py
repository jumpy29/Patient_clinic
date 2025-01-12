from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from clinic.controller import Controller
class UpdateNoteMenu(QWidget):
    change_to_note_menu_signal = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("Enter updated note here")

        note_number_layout = QHBoxLayout()
        self.note_number_input = QLineEdit()
        self.note_number_input.setPlaceholderText("Enter note number to update")
        self.note_number_input.textChanged.connect(self.note_number_entered)
        self.update_button = QPushButton("Update note")
        self.update_button.setEnabled(False) #initial state
        self.update_button.clicked.connect(self.update_button_clicked)
        
        note_number_layout.addWidget(self.note_number_input)
        note_number_layout.addWidget(self.update_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_button_clicked)

        layout.addWidget(self.note_input)
        layout.addLayout(note_number_layout)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def note_number_entered(self):
        self.update_button.setEnabled(True)

    def reset_input(self):
        #returning to initial state
        self.note_number_input.setText("")
        self.update_button.setEnabled(False)
        self.note_input.setText("")
        self.note_input.setPlaceholderText("Enter updated note here")

    def update_button_clicked(self):
        try:
            note_number = int(self.note_number_input.text())
            text = self.note_input.toPlainText()
            if text == "":
                dlg = QMessageBox()
                dlg.setWindowTitle("Error")
                dlg.setIcon(QMessageBox.Icon.Warning)
                dlg.setText("Please enter updated note")
                dlg.exec()
            else:
                self.controller.update_note(note_number, text)
                dlg = QMessageBox()
                dlg.setWindowTitle("Done")
                dlg.setIcon(QMessageBox.Icon.Information)
                dlg.setText("Note updated successfully")
                dlg.exec()
                self.reset_input()
                self.back_button_clicked()
        except:
            dlg = QMessageBox()
            dlg.setWindowTitle("Error")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText("Invalid note number, try again!")
            dlg.exec()
        self.reset_input()

    def back_button_clicked(self):
        self.reset_input()
        self.change_to_note_menu_signal.emit()

class DeleteNoteMenu(QWidget):
    change_to_note_menu_signal = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        note_number_layout = QHBoxLayout()
        self.note_number_input = QLineEdit()
        self.note_number_input.setPlaceholderText("Enter note number to delete")
        self.note_number_input.textChanged.connect(self.note_number_entered)
        self.delete_button = QPushButton("Delete note")
        self.delete_button.setEnabled(False) #initial state
        self.delete_button.clicked.connect(self.delete_button_clicked)
        
        note_number_layout.addWidget(self.note_number_input)
        note_number_layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_button_clicked)

        layout.addLayout(note_number_layout)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def note_number_entered(self):
        self.delete_button.setEnabled(True)

    def reset_input(self):
        #returning to initial state
        self.note_number_input.setText("")
        self.delete_button.setEnabled(False)


    def delete_button_clicked(self):
        try:
            note_number = int(self.note_number_input.text())
            self.controller.delete_note(note_number)
            dlg = QMessageBox()
            dlg.setWindowTitle("Done")
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.setText("Note deleted successfully")
            dlg.exec()
            self.reset_input()
            self.back_button_clicked()
        except:
            dlg = QMessageBox()
            dlg.setWindowTitle("Error")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText("Invalid note number, try again!")
            dlg.exec()
        self.reset_input()

    def back_button_clicked(self):
        self.reset_input()
        self.change_to_note_menu_signal.emit()