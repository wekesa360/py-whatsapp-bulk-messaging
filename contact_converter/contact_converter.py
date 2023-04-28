import csv

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