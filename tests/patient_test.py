from unittest import TestCase
from unittest import main
from clinic.patient import Patient

class PatientTests(TestCase):
    def test_equality(self):
          patient1 = Patient(1, "name", "dob", "phone", "email", "address")
          patient2 = Patient(1, "name", "dob", "phone", "email", "address")
          patient3 = Patient(3, "name", "dob", "phone", "email", "address")
          patient4 = Patient(1, "name4", "dob", "phone", "email", "address")
          patient5 = Patient(30, "Sam", "29 April 2005", "1234556789", "sam@gmail.com", "1324")

          self.assertIsNotNone(patient1, "patient1 created")
          self.assertEqual(patient1, patient2, "patient1 and patient2 should be equal")
          self.assertNotEqual(patient1, patient3, "patients not equal")
          self.assertNotEqual(patient1, patient4, "patients not equal")
          self.assertNotEqual(patient1, patient5, "patients not equal")

    def test_str(self):
        patient = Patient(
            phn=123456789,
            name="person",
            dob="2024-11-04",
            phone_no="123-456-7890",
            email="person@example.com",
            address="123"
        )
        
        expected_str = (
            "Patient(phn=123456789, name=person, dob=2024-11-04, "
            "phone_no=123-456-7890, email=person@example.com, address=123)"
        )

        self.assertEqual(str(patient), expected_str, "str test")

if __name__ == '__main__':
	main()