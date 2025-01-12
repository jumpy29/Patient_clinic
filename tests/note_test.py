
from unittest import TestCase
from unittest import main
from clinic.note import Note
from datetime import datetime

class NoteTests(TestCase):
    def test_equality(self):
         note1 = Note(1, "1")
         note2 = Note(1, "1")
         self.assertTrue(note1==note2, "same note check (assuming time can be different for equality)")

         note3 = Note(1, "3")
         note4 = Note(4, "1")
         note5 = Note(5, "5")
         self.assertFalse(note1==note3, "different text but same code, should not be equal")
         self.assertFalse(note1==note4, "same text but different code, should not be equal")
         self.assertFalse(note1==note5, "both code and text different, should not be equal")
         

    def test_time(self):
        note_1 = Note(1, "1")
        creation_time = note_1.get_time()
        self.assertTrue(isinstance(note_1.get_time(), datetime), "checking if time is stored")
        note_1.update_time()
        self.assertFalse(creation_time==note_1.get_time(), "time should change on updation")

    def test_str(self):
        note = Note(1, "note")
        expected_str = "Note[code=1, text='note']"
        self.assertEqual(str(note), expected_str, "str test")


if __name__ == '__main__':
	main()