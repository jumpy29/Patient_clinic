from json import JSONDecoder
from clinic.patient import Patient

#Converts a json object to a Patient object and returns it
class PatientDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if '__type__' in dct and dct['__type__']=='Patient':
            #returning new patient with autosave as last parameter
            return Patient(dct['phn'],dct['name'],dct['dob'],dct['phone_no'],dct['email'],dct['address'],dct['autosave'])
        return dct