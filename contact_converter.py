import csv
import re

class ContactConverter:
    @staticmethod
    def convert(file_path, phone_column, name_column=None, progress_callback=None):
        contacts = []
        try:
            with open(file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                total_rows = sum(1 for row in reader)
                csv_file.seek(0)
                reader = csv.DictReader(csv_file)
                
                if phone_column not in reader.fieldnames:
                    raise ValueError(f"Column '{phone_column}' not found in CSV file.")
                
                for i, row in enumerate(reader):
                    phone = ContactConverter.validate(row[phone_column])
                    if phone:
                        name = row.get(name_column, "") if name_column else ""
                        contacts.append((phone, name))
                    if progress_callback:
                        progress_callback((i + 1) / total_rows)
        except Exception as e:
            raise Exception(f"Error processing CSV file: {str(e)}")
        return contacts

    @staticmethod
    def validate(contact):
        country_code = "+254"
        if contact.startswith(("7", "1")):
            contact = country_code + contact
        elif contact.startswith("0"):
            contact = country_code + contact[1:]
        else:
            return None
        contact = re.sub(r"[^\d+]", "", contact)
        return contact
