from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self, phn, autosave=False) -> None:
        self.note_dao = NoteDAOPickle(phn, autosave)

    def create_note(self, text):
        return self.note_dao.create_note(text)
    
    def search_note(self, code):
        return self.note_dao.search_note(code)
    
    def retrieve_notes(self, text):
        return self.note_dao.retrieve_notes(text)
    
    def update_note(self, code, text):
        return self.note_dao.update_note(code, text)
        
    def delete_note(self, code):
        return self.note_dao.delete_note(code)
    
    def list_notes(self):
        return self.note_dao.list_notes()
    