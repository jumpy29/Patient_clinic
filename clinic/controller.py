#! /usr/bin/env python3
import hashlib
from clinic.patient import *
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class Controller:
    def __init__(self, autosave=False) -> None:
        self.__users = self.load_users()
        self.is_logged_in = False
        self.current_patient = None
        self.autosave = autosave
        self.patient_dao = PatientDAOJSON(autosave)

    def load_users(self):
        users = {}
        try:
            f = open("clinic/users.txt", "r")
            for line in f:
                line = line.strip()
                user = line.split(",")
                users[user[0]] = user[1]
            f.close()
        except:
            pass
        return users

    def get_password_hash(self, password):
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def login(self, user: str, password: str) -> bool:
        if not self.is_logged_in:
            password_hash = self.get_password_hash(password)
            if user not in self.__users or self.__users[user] != password_hash:
                raise InvalidLoginException
            self.is_logged_in = True
            return True
        raise DuplicateLoginException

    def logout(self) -> None:
        if self.is_logged_in:
            self.is_logged_in = False
            return True
        raise InvalidLogoutException

    def create_patient(self, phn: int, name: str, dob: str, phone_no: str, email: str, address: str) -> Patient:
        if self.is_logged_in:
            return self.patient_dao.create_patient(Patient(phn,name,dob,phone_no,email,address, self.autosave))
        raise IllegalAccessException

    def search_patient(self, phn: int) -> Patient:
        if self.is_logged_in:
            return self.patient_dao.search_patient(phn)
        raise IllegalAccessException

    def retrieve_patients(self, curname: str) -> list[Patient]:
        if self.is_logged_in:
            return self.patient_dao.retrieve_patients(curname)
        raise IllegalAccessException

    def update_patient(self, phn: int, new_phn: int, name: str, dob: str, phone_no: str, email: str, address: str) -> bool:
        if self.is_logged_in:
            cur_patient = self.get_current_patient()
            if (cur_patient==None or cur_patient.get_phn()!=phn) and self.patient_dao.update_patient(phn, Patient(new_phn,name,dob,phone_no,email, address, self.autosave)):
                return True
            raise IllegalOperationException
        raise IllegalAccessException

    def delete_patient(self, phn: int) -> bool:
        if self.is_logged_in:
            # patient = self.search_patient(phn)
            # if patient and patient != self.get_current_patient():
            #     self.patients.remove(patient)
            #     return True
            # raise IllegalOperationException
            if self.get_current_patient() and self.get_current_patient().get_phn()==phn or self.patient_dao.delete_patient(phn)==False:
                raise IllegalOperationException
            return True
        raise IllegalAccessException

    def list_patients(self) -> list[Patient]:
        if self.is_logged_in:
            return self.patient_dao.list_patients()
        raise IllegalAccessException

    def get_current_patient(self) -> Patient:
        if self.is_logged_in:
            return self.current_patient
        raise IllegalAccessException

    def set_current_patient(self, phn: int) -> None:
        if self.is_logged_in:
            patient = self.search_patient(phn)
            if patient:
                self.current_patient = patient
                return
            raise IllegalOperationException
        raise IllegalAccessException

    def unset_current_patient(self) -> None:
        if self.is_logged_in:
            self.current_patient = None
            return
        raise IllegalAccessException

    def create_note(self, text):
        if self.is_logged_in:
            patient = self.get_current_patient()
            if patient:
                return patient.create_note(text)
            raise NoCurrentPatientException
        raise IllegalAccessException

    def search_note(self, code):
        if self.is_logged_in:
            patient = self.get_current_patient()
            if patient:
                return patient.search_note(code)
            raise NoCurrentPatientException
        raise IllegalAccessException

    def retrieve_notes(self, text):
        if self.is_logged_in:
            patient = self.get_current_patient()
            if patient:
                return patient.retrieve_notes(text)
            raise NoCurrentPatientException
        raise IllegalAccessException

    def update_note(self, code, text):
        if self.is_logged_in:
            patient = self.get_current_patient()
            if patient:
                return patient.update_note(code, text)
            raise NoCurrentPatientException
        raise IllegalAccessException

    def delete_note(self, code):
        if self.is_logged_in:
            patient = self.get_current_patient()
            if patient:
                return patient.delete_note(code)
            raise NoCurrentPatientException
        raise IllegalAccessException

    def list_notes(self):
        if self.is_logged_in:
            patient = self.get_current_patient()
            if patient:
                return patient.list_notes()
            raise NoCurrentPatientException
        raise IllegalAccessException
