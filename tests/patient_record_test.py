from unittest import TestCase
from unittest import main
from clinic.patient_record import PatientRecord
from clinic.note import Note

class PatientRecordTests(TestCase):
    def setUp(self):
        self.patient_record = PatientRecord()

    def test_create_note(self):
        self.assertTrue(self.patient_record.note_count==0, "0 notes created initially")

        note1 = Note(1, "note1")
        self.patient_record.create_note("note1")
        self.assertTrue(self.patient_record.note_count==1, "added one note, so note_count should be one")
        self.assertTrue(self.patient_record.notes[0]==note1, "note1 should be added to note list")

        note2 = Note(2, "note2")
        self.patient_record.create_note("note2")
        self.assertTrue(self.patient_record.note_count==2, "note count should be 2")
        self.assertTrue(self.patient_record.notes[1]==note2, "second note in list should be note2")

    def test_search_note(self):
        note1 = Note(1, "note1")
        note2 = Note(2, "note2")
        self.patient_record.create_note("note1")
        self.patient_record.create_note("note2")

        self.assertTrue(self.patient_record.search_note(1)==note1, "first note should be note1")
        self.assertTrue(self.patient_record.search_note(2)==note2, "second note should be note2")
        self.assertIsNone(self.patient_record.search_note(4), "no note with code 4 exists")

    def test_update_note(self):
        note1 = Note(1, "note1")
        new_note1 = Note(1, "note1 changed")
        note2 = Note(2, "note2")

        self.patient_record.create_note("note1")
        self.patient_record.create_note("note2")

        self.assertTrue(self.patient_record.update_note(1, "note1 changed"))
        self.assertEqual(self.patient_record.notes[0], new_note1, "updated change should be stored")

        self.assertFalse(self.patient_record.update_note(4, "note4"), "no note with code 4 exists")

    def test_delete_note(self):
        note1 = Note(1, "note1")
        note2 = Note(2, "note2")
        self.patient_record.create_note("note1")
        self.patient_record.create_note("note2")

        self.patient_record.delete_note(1)
        self.assertEqual(self.patient_record.note_count, 1, "note count should be 1 after deletion")
        self.assertIsNone(self.patient_record.search_note(1), "note should be deleted")

        self.patient_record.delete_note(2)
        self.assertEqual(self.patient_record.note_count, 0, "no notes are stored after deletion of both")
        self.assertIsNone(self.patient_record.search_note(1), "note should be deleted")

    def test_list_notes(self):
        note_list = []
        self.assertEqual(self.patient_record.list_notes(), note_list, "notelist should be empty initially")

        note1 = Note(1, "note1")
        note2 = Note(2, "note2")
        self.patient_record.create_note("note1")
        self.patient_record.create_note("note2")
        note_list = [note1, note2]
        stored_note_list = []
        stored_note_list.append(self.patient_record.search_note(1))
        stored_note_list.append(self.patient_record.search_note(2))
        self.assertEqual(stored_note_list, note_list, "added two notes two list")
        
if __name__ == '__main__':
    main()