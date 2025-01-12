
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHeaderView, QMessageBox, QHBoxLayout, QLineEdit
from PyQt6.QtWidgets import QPushButton, QTableView, QWidget
from clinic.gui.patients_table_model import PatientsTableModel
from clinic.controller import IllegalOperationException

class PatientsGui(QWidget):
    change_to_add_menu_signal = pyqtSignal()
    patient_double_clicked_signal = pyqtSignal(int)
    patient_deleted_signal = pyqtSignal()
    phn_searched_signal = pyqtSignal(int)
    change_to_main_menu_signal = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Patients")

        #setting up model and view
        self.patient_table = QTableView()
        self.patient_model = PatientsTableModel(self.controller)
        self.patient_table.setModel(self.patient_model)
        #making the table take all of the available width
        header = self.patient_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        #TODO:
        #search patient layout
        phn_search_layout = QHBoxLayout()
        self.phn_search_input = QLineEdit()
        self.phn_search_input.setPlaceholderText("Enter phn")
        self.phn_search_input.textChanged.connect(self.phn_to_search_entered) 
        self.phn_search_button = QPushButton("Search by PHN")
        self.phn_search_button.setEnabled(False) #initial state
        self.phn_search_button.clicked.connect(self.phn_search_button_clicked)

        #retrive patients layout
        name_search_layout = QHBoxLayout()
        self.name_search_input = QLineEdit()
        self.name_search_input.setPlaceholderText("Enter name")
        self.name_search_input.textChanged.connect(self.name_to_search_entered) #TODO:
        self.name_search_button = QPushButton("Search by name")
        self.name_search_button.setEnabled(False) #initial state
        self.name_search_button.clicked.connect(self.name_search_button_clicked) #TODO:

        #adding to layout
        phn_search_layout.addWidget(self.phn_search_input)
        phn_search_layout.addWidget(self.phn_search_button)
        name_search_layout.addWidget(self.name_search_input)
        name_search_layout.addWidget(self.name_search_button)

        #refresh button

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_button_clicked)

        add_button = QPushButton("Add Patient")
        add_button.clicked.connect(self.add_button_clicked)

        #update button
        self.update_button = QPushButton("Update Patient")
        self.update_button.setEnabled(False) #initial state
        self.update_button.clicked.connect(self.update_button_clicked)

        #delete button
        self.delete_button = QPushButton("Delete Patient")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_button_clicked)

        #back button 
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_button_clicked)

        #allowing to select a patient on double click
        self.current_patient_phn = None
        self.patient_table.doubleClicked.connect(self.patient_double_clicked)
        self.patient_table.clicked.connect(self.patient_selected)

        layout = QVBoxLayout()
        layout.addWidget(self.patient_table)
        layout.addLayout(phn_search_layout)
        layout.addLayout(name_search_layout)
        layout.addWidget(self.refresh_button)
        layout.addWidget(add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.refresh_table()

    def refresh_table(self):
        self.patient_model.refresh_data()

    def phn_to_search_entered(self):
        self.phn_search_button.setEnabled(True)

    def phn_search_button_clicked(self):
        phn = int(self.phn_search_input.text())
        #if patient does not exist show error
        if not self.controller.search_patient(phn):
            dlg = QMessageBox()
            dlg.setWindowTitle("Invalid search")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText("Invalid phn, try again!")
            dlg.exec()
        else:
            self.phn_searched_signal.emit(phn)

    
    def name_to_search_entered(self):
        self.name_search_button.setEnabled(True) #enabling to search after text entered

    
    def name_search_button_clicked(self):
        patients = self.controller.retrieve_patients(self.name_search_input.text())
        if patients:
            self.patient_model.display_custom_data(patients)
        else: 
            dlg = QMessageBox()
            dlg.setWindowTitle("Invalid search")
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.setText("No patient with name exists, try again!")
            dlg.exec()

    def reset_inputs(self):
        self.phn_search_input.setText("")
        self.phn_search_button.setEnabled(False)
        self.name_search_input.setText("")
        self.name_search_button.setEnabled(False)

    def refresh_button_clicked(self):
        self.reset_inputs()
        self.patient_model.refresh_data()

    def add_button_clicked(self):
        self.change_to_add_menu_signal.emit()

    def update_button_clicked(self):
        self.patient_double_clicked()

    def delete_button_clicked(self):
        #do not need to have try except as only what is displayed can be selected
        self.controller.delete_patient(self.current_patient_phn)
        self.refresh_table() #refreshing table
        dlg = QMessageBox()
        dlg.setWindowTitle("Patient deleted")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText("Patient successfully deleted!")
        dlg.exec()
        self.delete_button.setEnabled(False)
        self.update_button.setEnabled(False)
        self.patient_deleted_signal.emit()


    def patient_selected(self):
        index = self.patient_table.selectionModel().currentIndex()
        self.current_patient_phn = int(index.sibling(index.row(), 0).data())
        self.update_button.setEnabled(True) #enabling to update when patient is selected
        self.delete_button.setEnabled(True) #same as above

    def patient_double_clicked(self):
        index = self.patient_table.selectionModel().currentIndex()
        self.current_patient_phn = int(index.sibling(index.row(), 0).data())
        self.patient_double_clicked_signal.emit(self.current_patient_phn)

    def back_button_clicked(self):
        self.reset_inputs()
        self.change_to_main_menu_signal.emit()
        