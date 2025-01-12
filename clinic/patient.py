#! /usr/bin/env python3
from clinic.patient_record import PatientRecord

class Patient:
    def __init__(self, phn:int, name:str, dob:str, phone_no:str, email:str, address:str, autosave=False):
        self.phn = phn
        self.name = name
        self.birth_date = dob
        self.phone = phone_no
        self.email = email
        self.address = address
        self.autosave = autosave
        self.patient_record = PatientRecord(phn, autosave)

    def create_note(self, text):
        return self.get_patient_record().create_note(text)   

    def search_note(self, code):
        return self.get_patient_record().search_note(code)  

    def retrieve_notes(self, text):
        return self.get_patient_record().retrieve_notes(text)   
    
    def update_note(self, code, text):
        return self.get_patient_record().update_note(code, text)
    
    def delete_note(self, code):
        return self.get_patient_record().delete_note(code)
    
    def list_notes(self):
        return self.get_patient_record().list_notes()

    def get_phn(self)->int:
        return self.phn

    def get_name(self):
        return self.name
    
    def get_dob(self)->str:
        return self.birth_date
    
    def get_phone_no(self)->str:
        return self.phone
    
    def get_email(self)->str:
        return self.email
    
    def get_address(self)->str:
        return self.address
    
    def get_patient_record(self):
        return self.patient_record

    def set_phn(self, phn:int)->None:
        self.phn = phn

    def set_name(self, name:str)->None:
        self.name = name
    
    def set_dob(self, dob:str)->None:
        self.birth_date = dob
    
    def set_phone_no(self, phone_no:str)->None:
        self.phone = phone_no

    def set_email(self, email:str)->None:
        self.email = email

    def set_address(self, address:str)->None:
        self.address = address
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Patient):
            return self.get_phn() == other.get_phn() \
            and self.get_name()==other.get_name() \
            and self.get_dob()==other.get_dob() \
            and self.get_phone_no()==other.get_phone_no() \
            and self.get_email()==other.get_email() \
            and self.get_address()==other.get_address() 
        return False

    def __str__(self) -> str:
        return f"Patient(phn={self.get_phn()}, name={self.get_name()}, dob={self.get_dob()}, phone_no={self.get_phone_no()}, email={self.get_email()}, address={self.get_address()})"
