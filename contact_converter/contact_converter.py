import csv
import re


class ContactConverter:
    def __init__(self, filename, column_name):
        self.filename = filename
        self.column_name = column_name

    def convert(self):
        contacts = []
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                if self.column_name in row:

                    contact = self.validate(row[self.column_name])
                    if contact:
                        contacts.append(contact)
                else:
                    return False

        return contacts

    def validate(self, contact):
        country_code = "+254"
        # Convert the contact number to the international format
        if contact.startswith(("7", "1")):
            contact = country_code + contact
        elif contact.startswith("0"):
            contact = country_code + contact[1:]
        else:
            return "Invalid contacts"
        # Remove all non-numeric characters from the contact number
        contact = re.sub(r"[^\d+]", "", contact)

        return contact
