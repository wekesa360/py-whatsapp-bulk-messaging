import csv
import re
import phonenumbers
class ContactConverter:
    def __init__(self, filename, column_name):
        self.filename = filename
        self.column_name = column_name
    
    def convert(self):
        contacts = []

        with open(self.filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if self.column_name in row:
                    contact = self.validate(row[self.column_name])
                    if contact:
                        contacts.append(contact)
        
        return contacts
    
    def validate(self, contact):
        # Remove all non-numeric characters from the contact number
        contact = ''.join([c for c in contact if c.isdigit()])

        # Check if the contact number is valid
        try:
            parsed_number = phonenumbers.parse(contact, None)
        except phonenumbers.NumberParseException:
            return None
        
        # Check if the contact number is a mobile number
        if not phonenumbers.is_valid_number(parsed_number):
            return None
        
        # Format the contact number in the international format
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        