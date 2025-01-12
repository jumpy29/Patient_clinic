from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from clinic.gui.patients_gui import PatientsGui

class MainMenu(QWidget):
    #signals emitted 
    patient_menu_signal = pyqtSignal()
    appointment_menu_signal = pyqtSignal()
    logout_signal = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        #setting the font to use
        label_font = QFont("Courier New", 30, QFont.Weight.Bold)

        # parent layout
        layout = QVBoxLayout()

        # Title 
        label = QLabel("CLINIC")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(label_font)

        # creating buttons
        patients_button = QPushButton("Patients")
        make_appointment_button = QPushButton("Make an Appointment")
        logout_button = QPushButton("Logout")

        #connecting buttons 
        patients_button.clicked.connect(self.patients_button_clicked)
        make_appointment_button.clicked.connect(self.appointment_button_clicked)
        logout_button.clicked.connect(self.logout_button_clicked)

        # adding widegts to main layout
        layout.addWidget(label)
        layout.addWidget(patients_button)
        layout.addWidget(make_appointment_button)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def patients_button_clicked(self):
        self.patient_menu_signal.emit() #sending signal clinic_gui

    def appointment_button_clicked(self):
        self.appointment_menu_signal.emit() #sending signal to clinic_gui

    def logout_button_clicked(self):
        self.logout_signal.emit() #sending signal to clinic_gui


