from json import JSONEncoder
from clinic.patient import Patient

#Converts a Patient object to a json object that can be used to store in json file
class PatientEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Patient):
            #passing autosave as the last parameter for file persistence
            return {"__type__": "Patient", \
                    "phn": obj.get_phn(), \
                    "name": obj.get_name(), \
                    "dob": obj.get_dob(), \
                    "phone_no": obj.get_phone_no(), \
                    "email": obj.get_email(), \
                    "address": obj.get_address(), \
                    "autosave": obj.autosave}
        return super().default(obj)