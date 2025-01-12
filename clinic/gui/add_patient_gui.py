from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

from clinic.controller import IllegalOperationException

class AddPatientMenu(QWidget):
    patient_added_signal = pyqtSignal()
    change_to_patient_menu = pyqtSignal()
    def __init__(self, controller, patients_menu):
        super().__init__()
        self.controller = controller
        self.patients_menu = patients_menu
        self.setWindowTitle("Add Patient")

        main_layout = QVBoxLayout()

        input_layout = QGridLayout()

        #making QHBoxLayouts for each field

        phn_label = QLabel("PHN")
        self.phn_input = QLineEdit()
        self.phn_input.textChanged.connect(self.phn_entered)

        name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setEnabled(False) #initial state
        self.name_input.textChanged.connect(self.name_entered)  #connecting to function

        dob_label = QLabel("Birth-Date")
        self.dob_input = QLineEdit()
        self.dob_input.setEnabled(False) #initial state
        self.dob_input.textChanged.connect(self.dob_entered) #connection to function

        phone_label = QLabel("Phone")
        self.phone_input = QLineEdit()
        self.phone_input.setEnabled(False)
        self.phone_input.textChanged.connect(self.phone_entered)

        email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setEnabled(False)
        self.email_input.textChanged.connect(self.email_entered)

        address_label = QLabel("Address")
        self.address_input = QLineEdit()
        self.address_input.setEnabled(False)
        self.address_input.textChanged.connect(self.address_entered)


        #add button
        self.add_button = QPushButton("ADD")
        self.add_button.setEnabled(False) #initial state
        self.add_button.clicked.connect(self.add_button_clicked)

        #clear button
        self.clear_button = QPushButton("CLEAR")
        self.clear_button.clicked.connect(self.clear_fields)

        #back button
        self.back_button = QPushButton("BACK")
        self.back_button.clicked.connect(self.back_button_clicked)


        #adding input labels and linedits to gridlayout
        input_layout.addWidget(phn_label, 0, 0)
        input_layout.addWidget(self.phn_input, 0, 1)
        input_layout.addWidget(name_label, 1, 0)
        input_layout.addWidget(self.name_input, 1, 1)
        input_layout.addWidget(dob_label, 2, 0)
        input_layout.addWidget(self.dob_input, 2, 1)
        input_layout.addWidget(phone_label, 3, 0)
        input_layout.addWidget(self.phone_input, 3, 1)
        input_layout.addWidget(email_label, 4, 0)
        input_layout.addWidget(self.email_input, 4, 1)
        input_layout.addWidget(address_label, 5, 0)
        input_layout.addWidget(self.address_input, 5, 1)

        input_layout.setColumnMinimumWidth(0, 200)  #setting minimun column width

        #aligning the text
        phn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dob_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        phone_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        address_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #now adding all layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.clear_button)
        main_layout.addWidget(self.back_button)

        self.setLayout(main_layout)

    def phn_entered(self):
        self.name_input.setEnabled(True)

    def name_entered(self):
        self.dob_input.setEnabled(True)

    def dob_entered(self):
        self.phone_input.setEnabled(True)

    def phone_entered(self):
        self.email_input.setEnabled(True)

    def email_entered(self):
        self.address_input.setEnabled(True)

    def address_entered(self):
        self.add_button.setEnabled(True)

    def add_button_clicked(self):
        phn = int(self.phn_input.text())
        name = self.phn_input.text()
        dob = self.dob_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        try:
            self.controller.create_patient(phn, name, dob, phone, email, address)
            self.clear_fields()
            dlg = QMessageBox()
            dlg.setWindowTitle("Patient added")
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.setText("Patient successfully added!")
            dlg.exec()
            self.patients_menu.refresh_table() #refreshing table
            self.patient_added_signal.emit()

        except IllegalOperationException:
            self.clear_fields()
            dlg = QMessageBox()
            dlg.setWindowTitle("Invalid operation")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText("Patient with phn already exists, try again!")
            dlg.exec()

    def clear_fields(self):
        # clearing text in all QLineEdits
        self.phn_input.clear()
        self.name_input.clear()
        self.dob_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()

        # reset button state and input state
        self.add_button.setEnabled(False)
        self.name_input.setEnabled(False)
        self.dob_input.setEnabled(False)
        self.phone_input.setEnabled(False)
        self.email_input.setEnabled(False)
        self.address_input.setEnabled(False)

    def back_button_clicked(self):
        self.clear_fields()
        self.change_to_patient_menu.emit()
