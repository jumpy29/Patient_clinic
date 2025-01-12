from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class NoteMenu(QWidget):
    change_to_appointment_menu_signal = pyqtSignal()
    change_to_add_note_menu_signal = pyqtSignal()
    change_to_update_note_menu_signal = pyqtSignal()
    change_to_delete_note_menu_signal = pyqtSignal()
    change_to_list_note_signal = pyqtSignal()
    change_to_search_note_signal = pyqtSignal(str)
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Appointment")
        self.controller = controller
        layout = QVBoxLayout()
        
        current_patient = self.controller.get_current_patient()

        search_notes_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text to search patient records")
        self.search_input.textChanged.connect(self.search_input_changed)
        self.search_notes_button = QPushButton("Search patient Records")
        self.search_notes_button.setEnabled(False) #initial state
        self.search_notes_button.clicked.connect(self.search_notes_button_clicked)
        search_notes_layout.addWidget(self.search_input)
        search_notes_layout.addWidget(self.search_notes_button)

        self.add_note_button = QPushButton("Add new note")
        self.add_note_button.clicked.connect(self.add_note_button_clicked)

        self.update_note_button = QPushButton("Update note")
        self.update_note_button.clicked.connect(self.update_note_button_clicked)

        self.delete_note_button = QPushButton("Delete note")
        self.delete_note_button.clicked.connect(self.delete_note_button_clicked)

        self.list_notes_button = QPushButton("List patient records")
        self.list_notes_button.clicked.connect(self.list_notes_button_clicked)


        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_button_clicked)

        # layout.addWidget(self.title)
        layout.addLayout(search_notes_layout)
        layout.addWidget(self.add_note_button)
        layout.addWidget(self.update_note_button)
        layout.addWidget(self.delete_note_button)
        layout.addWidget(self.list_notes_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def add_note_button_clicked(self):
        self.change_to_add_note_menu_signal.emit()

    def list_notes_button_clicked(self):
        self.change_to_list_note_signal.emit()

    def update_note_button_clicked(self):
        self.change_to_update_note_menu_signal.emit()

    def delete_note_button_clicked(self):
        self.change_to_delete_note_menu_signal.emit()

    def back_button_clicked(self):
        self.controller.unset_current_patient() #unset current patient
        self.change_to_appointment_menu_signal.emit()

    def search_input_changed(self):
        self.search_notes_button.setEnabled(True) #enabling search

    def search_notes_button_clicked(self):
        text = self.search_input.text()
        self.change_to_search_note_signal.emit(text) #sending signal to clinic
        self.clear() #resetting fields

    def clear(self):
        self.search_notes_button.setEnabled(False)
        self.search_input.setPlaceholderText("Enter text to search patient records")
        self.search_input.setText("")

