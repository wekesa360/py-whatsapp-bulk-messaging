import csv
import re


class ContactConverter:
    def __init__(self, file_path, column_name="number"):
        self.file_path = file_path
        self.column_name = column_name

    def convert(self):
        contacts = []
        with open(self.file_path, "r") as csv_file:
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
        """
        This function validates the contact number
        """
        country_code = "+254"
        if contact.startswith(("7", "1")):
            contact = country_code + contact
        elif contact.startswith("0"):
            contact = country_code + contact[1:]
        else:
            return "Invalid contacts"
        contact = re.sub(r"[^\d+]", "", contact)

        return contact
