import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from clinic.controller import Controller
from clinic.gui.login_gui import LoginDashBoard
from clinic.gui.main_menu_gui import MainMenu
from clinic.controller import InvalidLoginException, IllegalOperationException
from clinic.gui.patients_gui import PatientsGui
from clinic.gui.add_patient_gui import AddPatientMenu
from clinic.gui.edit_patient_gui import EditPatientMenu
from clinic.gui.appointment_gui import AppointmentMenu
from clinic.gui.note_menu_gui import NoteMenu
from clinic.gui.add_note_gui import AddNoteGui
from clinic.gui.edit_note_menu import UpdateNoteMenu, DeleteNoteMenu
from clinic.gui.list_notes_gui import ListNotesGui

#Stacked window indexes 
LOGIN_PAGE        = 0
MAIN_MENU         = 1
PATIENTS_MENU     = 2
ADD_PATIENT_MENU  = 3
APPOINTMENT_MENU  = 4
NOTE_MENU         = 5
ADD_NOTE_MENU     = 6
UPDATE_NOTE_MENU  = 7
DELETE_NOTE_MENU  = 8
LIST_NOTE_MENU    = 9
EDIT_PATIENT_MENU = 10

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        #Using stacked widgets as central widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.controller = Controller(autosave=True)
        self.setWindowTitle("Clinic")
        self.resize(800, 500)

        #login page
        self.login_page = LoginDashBoard()
        self.login_page.login_button_clicked_signal.connect(self.handle_login) #connecting login signal

        #main menu
        self.main_menu = MainMenu(self.controller)
        #connecting all emmitted signals from menu
        self.main_menu.patient_menu_signal.connect(self.switch_to_patient_menu)
        self.main_menu.appointment_menu_signal.connect(self.switch_to_appointment_menu)
        self.main_menu.logout_signal.connect(self.handle_logout)
        self.edit_patient_menu = None

        self.central_widget.addWidget(self.login_page)    #index of login page = 0
        self.central_widget.addWidget(self.main_menu)     #index of main menu page = 1
    
    def handle_login(self, username, password):
        try:
            self.controller.login(username, password)

            self.patients_menu = PatientsGui(self.controller) #creating patients menu only if login successful
            self.central_widget.addWidget(self.patients_menu) #adding to stacked layout with index 2
            self.patients_menu.change_to_main_menu_signal.connect(self.switch_to_main_menu) #back button signal

            self.add_patient_menu = AddPatientMenu(self.controller, self.patients_menu) #creating add_patient menu if login successful
            self.central_widget.addWidget(self.add_patient_menu) #adding to stacked layout with index 3

            self.appointment_menu = AppointmentMenu(self.controller) #creating appointment menu
            self.central_widget.addWidget(self.appointment_menu) #adding to stacked layout with index 4

            self.note_menu = NoteMenu(self.controller) #creating note menu
            self.central_widget.addWidget(self.note_menu) #adding to stacked layout with index 5
            self.note_menu.change_to_appointment_menu_signal.connect(self.switch_to_appointment_menu)
            self.note_menu.change_to_add_note_menu_signal.connect(self.change_to_add_note_gui)
            self.note_menu.change_to_update_note_menu_signal.connect(self.change_to_update_note_menu)
            self.note_menu.change_to_delete_note_menu_signal.connect(self.change_to_delete_note_menu)
            self.note_menu.change_to_search_note_signal.connect(self.change_to_list_note_with_search)

            self.add_note_menu = AddNoteGui(self.controller) #creating add note gui
            self.central_widget.addWidget(self.add_note_menu) #adding to stacked layout with index 6
            self.add_note_menu.change_to_note_menu_signal.connect(self.change_to_note_menu) #connecting back signal\

            self.update_note_menu = UpdateNoteMenu(self.controller) #creating update note gui
            self.central_widget.addWidget(self.update_note_menu) #adding to stacked layout with index 7
            self.add_note_menu.change_to_note_menu_signal.connect(self.change_to_note_menu)

            self.delete_note_menu = DeleteNoteMenu(self.controller) #creating delete note menu
            self.central_widget.addWidget(self.delete_note_menu) #adding to stacked layout with index 8
            self.delete_note_menu.change_to_note_menu_signal.connect(self.change_to_note_menu)

            self.list_note_menu = ListNotesGui(self.controller)
            self.central_widget.addWidget(self.list_note_menu) #adding to stacked layout with index 9
            self.list_note_menu.change_to_note_menu_signal.connect(self.change_to_note_menu)

            #connecting on double click on patient 
            self.patients_menu.patient_double_clicked_signal.connect(self.switch_to_edit_patient_menu)

            #connecting signals emitted
            self.patients_menu.change_to_add_menu_signal.connect(self.change_to_add_patient_menu)
            self.add_patient_menu.patient_added_signal.connect(self.switch_to_patient_menu)
            self.patients_menu.phn_searched_signal.connect(self.switch_to_edit_patient_menu)
            self.appointment_menu.change_to_note_menu_signal.connect(self.change_to_note_menu)
            self.appointment_menu.change_to_main_menu_signal.connect(self.switch_to_main_menu)
            self.add_patient_menu.change_to_patient_menu.connect(self.switch_to_patient_menu)
            self.update_note_menu.change_to_note_menu_signal.connect(self.change_to_note_menu)
            self.note_menu.change_to_list_note_signal.connect(self.change_to_list_note_menu)

            self.central_widget.setCurrentIndex(MAIN_MENU) #switch to menu if login successful
        except InvalidLoginException:
            self.login_page.refresh()
            dlg = QMessageBox()
            dlg.setWindowTitle("Login Status")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText("Incorrect credential, try again!")
            dlg.exec()

    def handle_logout(self):
        self.controller.logout() #logout from controller
        self.login_page.refresh() #clearing fields
        self.central_widget.setCurrentIndex(LOGIN_PAGE) #switching to login page

    def switch_to_main_menu(self):
        self.central_widget.setCurrentIndex(MAIN_MENU)

    def switch_to_patient_menu(self):
        self.patients_menu.update_button.setEnabled(False) #disabling update initially
        self.patients_menu.delete_button.setEnabled(False) #disabling deletes initially
        self.patients_menu.phn_search_button.setEnabled(False) #disabling name search button 
        self.patients_menu.name_search_button.setEnabled(False) #disabling name search button
        self.patients_menu.phn_search_input.setText("") #clearing search phn 
        self.central_widget.setCurrentIndex(PATIENTS_MENU)

    def change_to_add_note_gui(self):
        self.central_widget.setCurrentIndex(ADD_NOTE_MENU)
    
    def change_to_update_note_menu(self):
        self.central_widget.setCurrentIndex(UPDATE_NOTE_MENU)
    
    def change_to_delete_note_menu(self):
        self.central_widget.setCurrentIndex(DELETE_NOTE_MENU)
    
    def change_to_list_note_menu(self):
        notes = self.controller.list_notes()
        notes_display = self.get_display_notes_text(notes)
        self.list_note_menu.note_display.setText(notes_display)
        self.central_widget.setCurrentIndex(LIST_NOTE_MENU)

    #using list notes menu, to display results of search with additional parameter
    def change_to_list_note_with_search(self, text):
        notes = self.controller.retrieve_notes(text)
        notes_display = self.get_display_notes_text(notes)
        self.list_note_menu.note_display.setText(notes_display)
        self.central_widget.setCurrentIndex(LIST_NOTE_MENU)

    def switch_to_appointment_menu(self):
        self.central_widget.setCurrentIndex(APPOINTMENT_MENU)

    def switch_to_edit_patient_menu(self, phn):
        #creating edit menu with phn passed when double clicked
        if not self.edit_patient_menu:
            self.edit_patient_menu = EditPatientMenu(self.controller, self.patients_menu, phn)
        else: 
            #changing selected patient from old patient to current selected patient
            self.edit_patient_menu.change_selected_patient(phn)

        #back button signal
        self.edit_patient_menu.change_to_patients_menu.connect(self.switch_to_patient_menu)

        #connecting updated signal, switching to patient menu after updating
        self.edit_patient_menu.patient_updated_signal.connect(self.switch_to_patient_menu)

        #connecting deleted patient signal, switching to patient menu after deleting
        self.edit_patient_menu.patient_deleted_signal.connect(self.switch_to_patient_menu)
        

        patient_being_updated = self.controller.search_patient(phn)

        #setting text to enable user to know whats originally stored

        self.edit_patient_menu.phn_input.clear()
        self.edit_patient_menu.phn_input.setText(str(patient_being_updated.phn))

        self.edit_patient_menu.name_input.clear()
        self.edit_patient_menu.name_input.setText(patient_being_updated.name)

        self.edit_patient_menu.dob_input.clear()
        self.edit_patient_menu.dob_input.setText(patient_being_updated.birth_date)

        self.edit_patient_menu.phone_input.clear()
        self.edit_patient_menu.phone_input.setText(patient_being_updated.phone)

        self.edit_patient_menu.email_input.clear()
        self.edit_patient_menu.email_input.setText(patient_being_updated.email)

        self.edit_patient_menu.address_input.clear()
        self.edit_patient_menu.address_input.setText(patient_being_updated.address)

        #adding to central stacked widget
        self.central_widget.addWidget(self.edit_patient_menu) # stacked widget with index 10

        self.central_widget.setCurrentIndex(EDIT_PATIENT_MENU)

    def change_to_add_patient_menu(self):
        self.central_widget.setCurrentIndex(ADD_PATIENT_MENU)

    def change_to_note_menu(self):
        self.note_menu.clear()
        self.central_widget.setCurrentIndex(NOTE_MENU)

    def get_display_notes_text(self, notes):
        #returns a string to display for list_notes
        result = ""
        if notes==[]:
            return "No Patient Record found"
        for note in notes:
            cur_note_text = f"#{note.code}, created on {note.time} \n{note.text}\n"
            result += cur_note_text + "\n"
        return result


def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
