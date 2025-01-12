import json
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder
from clinic.exception.illegal_operation_exception import IllegalOperationException

#DAO for patient class
class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave=False) -> None:
        self.autosave = autosave
        self.patients = []
        self.filename = 'clinic/patients.json'  #file where patients are stored

        #loading patients from file one by one and adding them to the collection
        if self.autosave:
            try:
                with open(self.filename, "r") as f:
                    patients = json.load(f, cls=PatientDecoder) #passing PatientDecoder to convert to Python object
                    self.patients = patients
            except:
                pass

    #function to write patients from collection to file
    def update_file(self):
        with open(self.filename, "w") as f:
            json.dump(self.patients, f, cls=PatientEncoder) #converting to json object then writing object to file


    def create_patient(self, patient):
        if self.search_patient(patient.get_phn()):
            raise IllegalOperationException
        self.patients.append(patient)
        if self.autosave:
            self.update_file() #storing new patient to file
        return patient

    def search_patient(self, key):
        for patient in self.patients:
            if patient.get_phn()==key:
                return patient

    def retrieve_patients(self, curname):
        result = []
        for patient in self.patients:
            if curname in patient.get_name():
                result.append(patient)
        return result

    def update_patient(self, key, patient):
        original_patient = self.search_patient(key)
        #patient can be updated if :
        # 1-original patient to update exists
        # 2-updated patient is not same as original patient
        # 3-if phn is updated, there shouldnt be another patient updated phn
        if original_patient!=None and (patient.get_phn()==key or self.search_patient(patient.get_phn())==None):
            self.delete_patient(key)
            self.create_patient(patient)
            if self.autosave:
                self.update_file() #writing updated collection to file
            return True
        return False

    def delete_patient(self, phn):
        patient_to_delete = self.search_patient(phn)
        if patient_to_delete:
            self.patients.remove(patient_to_delete)
            if self.autosave:
                self.update_file() #saving new collection to file
            return True
        return False

    def list_patients(self):
        return self.patients