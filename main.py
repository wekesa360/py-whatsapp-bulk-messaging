import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from contact_converter.contact_converter import ContactConverter
from whatsapp_bot.whatsapp_bot import WhatsAppBot
import sys


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("WhatsApp Bulk Message Automation")

        # Configure the style of the GUI
        style = ttk.Style()
        style.configure("TLabel", background="#303030", foreground="#FFFFFF", font=("Segoe UI", 10))
        style.configure("TEntry", background="#FFFFFF", foreground="#000000", font=("Segoe UI", 10))
        style.configure("TButton", background="#4CAF50", foreground="#FFFFFF", font=("Segoe UI", 10))
        style.configure("TFrame", background="#303030")

        # Create message input field
        self.message_label = ttk.Label(self.master, text="Enter the message you want to send:")
        self.message_label.pack(padx=10, pady=10, anchor="w")

        self.message_entry = ttk.Entry(self.master, width=50)
        self.message_entry.pack(padx=10, pady=5, fill="x")

        # Create column name input field
        self.column_name_label = ttk.Label(self.master, text="Enter the column name of the phone numbers:")
        self.column_name_label.pack(padx=10, pady=10, anchor="w")

        self.column_name_entry = ttk.Entry(self.master, width=50)
        self.column_name_entry.pack(padx=10, pady=5, fill="x")

        # Create upload button
        self.upload_button = ttk.Button(self.master, text="Upload file", command=self.upload_file)
        self.upload_button.pack(padx=10, pady=10, anchor="w")

        # Create a frame to display the output
        self.output_frame = ttk.Frame(self.master)
        self.output_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_label = ttk.Label(self.output_frame, text="Output:")
        self.output_label.pack(padx=10, pady=10, anchor="w")

        self.output_text = tk.Text(self.output_frame, bg="#FFFFFF", fg="#000000", font=("Segoe UI", 10), wrap="word")
        self.output_text.pack(padx=10, pady=5, fill="both", expand=True)

        #Redirect the standard output to the text widget
        sys.stdout = self

        def write(self, text):
            self.output_text.insert(tk.END, text)
            # Autoscroll to the bottom
            self.output_text.see(tk.END)

    def upload_file(self):
        # Open the file dialog box
        file_path = filedialog.askopenfilename()

        # Check if the file path is not None
        if file_path:
            # Create a contact converter object
            contact_converter = ContactConverter(file_path, self.column_name_entry.get())

            # Convert the contacts
            contacts = contact_converter.convert()


            # Create a whatsapp bot object
            whatsapp_bots = [WhatsAppBot(contact, self.message_entry.get()) for contact in contacts]

            # Start each instance in a separate thread
            for bot in whatsapp_bots:
                bot.start()

            # Wait for all threads to finish
            for bot in whatsapp_bots:
                bot.join()


if __name__ == "__main__":
    # Create a Tkinter root window
    root = tk.Tk()

    # Create a GUI object
    gui = GUI(root)

    # Start the main loop
    root.mainloop()