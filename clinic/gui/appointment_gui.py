from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from clinic.controller import Controller
class AppointmentMenu(QWidget):
    change_to_note_menu_signal = pyqtSignal()
    change_to_main_menu_signal = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Appointment")
        self.controller = controller
        layout = QVBoxLayout()

        phn_layout = QHBoxLayout()
        self.phn_input = QLineEdit()
        self.phn_input.setPlaceholderText("Enter phn to search")
        self.phn_input.textChanged.connect(self.phn_entered)
        self.appointment_button = QPushButton("Make appointment with patient")
        self.appointment_button.setEnabled(False) #initial state
        self.appointment_button.clicked.connect(self.appointment_button_clicked)
        
        phn_layout.addWidget(self.phn_input)
        phn_layout.addWidget(self.appointment_button)

        title_label = QLabel("Make an Appointment")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the text
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")  # Make text bigger and bold
        layout.addWidget(title_label)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_button_clicked)

        layout.addLayout(phn_layout)

        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def phn_entered(self):
        self.appointment_button.setEnabled(True)

    def reset_input(self):
        #returning to initial state
        self.phn_input.setText("")
        self.appointment_button.setEnabled(False)

    def appointment_button_clicked(self):
        try:
            phn = int(self.phn_input.text())
            self.controller.set_current_patient(phn)
            #TODO:
            self.change_to_note_menu_signal.emit()
        except:
            dlg = QMessageBox()
            dlg.setWindowTitle("Error")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText("Invalid phn, try again!")
            dlg.exec()
        self.reset_input()

    def back_button_clicked(self):
        self.reset_input()
        self.change_to_main_menu_signal.emit()