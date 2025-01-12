import sys

from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal
from clinic.patient import Patient
from clinic.controller import Controller

class PatientsTableModel(QAbstractTableModel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._data = []
        self.refresh_data()

    def refresh_data(self):
        self._data = []
        patients = self.controller.list_patients()
        for patient in patients:
            self._data.append([patient.phn, patient.name, patient.birth_date, patient.phone, patient.email, patient.address])
        self.layoutChanged.emit() #emitting signal to alert QtableView of model changes

    #calling for retrive data updates
    #TODO:
    def display_custom_data(self, patient_list):
        self._data=[]
        for patient in patient_list:
            self._data.append([patient.phn, patient.name, patient.birth_date, patient.phone, patient.email, patient.address])
        self.layoutChanged.emit()

    def reset(self):
        self._data = []
        self.layoutChanged.emit() #emitting signal to alert QtableView of model changes

    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            return value
        
    def rowCount(self, index):
        #the length of outer list
        return len(self._data)

    def columnCount(self, index):
        #the fields being displayed are phn, name, dob, phone, email, address
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ['PHN', 'Name', 'Birth-date', 'Phone', 'Email', 'Address']

        if orientation==Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)