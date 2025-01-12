from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
from pickle import load, dump

#dao for notes
class NoteDAOPickle(NoteDAO):
    def __init__(self, phn, autosave=False) -> None:
        self.note_count = 0
        self.notes = []
        self.filename = 'clinic/records/'+str(phn)+'.dat' #path where new file is stored
        self.autosave = autosave

        if self.autosave:
        # loading collection from file if file exists
            try:
                with open(self.filename, "rb") as f:
                    while True:
                        try:
                            note = load(f)
                            self.note_count+=1
                            self.notes.append(note)
                        except EOFError:
                            break
            except:
                pass

    #function to write collection to file
    def update_file(self):
        with open(self.filename, "wb") as f:
            for note in self.notes:
                dump(note, f)

    def create_note(self, text):
        self.note_count+=1
        note = Note(self.note_count, text)
        self.notes.append(note) #adding note to collection
        if self.autosave:
            with open(self.filename, "ab") as f: 
                dump(note, f) #adding to file as well
        return note
    
    def search_note(self, code):
        for note in self.notes:
            if note.get_code()==code:
                return note
    
    def update_note(self, code, text):
        note_to_update = self.search_note(code)
        if note_to_update:
            note_to_update.set_text(text)
            note_to_update.update_time()
            if self.autosave:
                self.update_file() #re write updated note collection to file
            return True
        return False
    
    def delete_note(self, code):
        note_to_del = self.search_note(code)
        if note_to_del:
            self.notes.remove(note_to_del)
            self.note_count-=1
            if self.autosave:
                self.update_file() #re writing updated note collection to file
            return True
        return False

    def retrieve_notes(self, text):
        result = []
        for note in self.notes:
            if text in note.get_text():
                result.append(note)
        return result

    def list_notes(self):
        return self.notes[::-1]