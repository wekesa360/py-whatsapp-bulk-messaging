import unittest
import csv
import os
import tempfile
from contact_converter import ContactConverter


class TestContactConverter(unittest.TestCase):
    def test_convert(self):
        # Create a temportary CSV file with some contacts
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w+", suffix=".csv"
        ) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["name", "phone"])
            writer.writeheader()
            writer.writerow({"name": "John Doe", "phone": "0792589417"})
            writer.writerow({"name": "John Doe", "phone": "792589417"})
            writer.writerow({"name": "John Doe", "phone": "0192589417"})
            writer.writerow({"name": "John Doe", "phone": "192589417"})
            writer.writerow({"name": "Jane Smith", "phone": "+44 7911 123456"})
            writer.writerow({"name": "Ahmad Ali", "phone": "+971 50 123 4567"})
            writer.writerow({"name": "Lucy Kimani", "phone": "+254 712 345 678"})

        # Test the convert() method with temporary CSV file
        converter = ContactConverter(csv_file.name, "phone")
        contacts = converter.convert()

        # Assert that the phone numbers were correctly formatted
        self.assertIn("+254792589417", contacts)
        self.assertIn("+254792589417", contacts)
        self.assertIn("+254192589417", contacts)
        self.assertIn("+254192589417", contacts)
        self.assertIn("+447911123456", contacts)
        self.assertIn("+971501234567", contacts)
        self.assertIn("+254712345678", contacts)
        # Delete the temporary CSV file
        os.unlink(csv_file.name)


if __name__ == "__main__":
    unittest.main()
