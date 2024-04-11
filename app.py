import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import contact_converter.contact_converter as contact_converter
import whatsapp_bot.whatsapp_bot as whatsapp_bot

class WhatsAppBotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WhatsApp Bot")
        self.geometry("800x600")
        self.style = Style(theme="flatly")

        # Create widgets
        self.file_label = tk.Label(self, text="Upload CSV File:")
        self.file_label.pack(pady=10)
        self.file_button = ttk.Button(self, text="Choose File", command=self.open_file_dialog)
        self.file_button.pack()

        

        self.contacts_frame = ttk.Frame(self)
        self.contacts_frame.pack(pady=10)
        self.contacts_label = tk.Label(self.contacts_frame, text="Contacts:")
        self.contacts_label.pack(side=tk.TOP)
        self.contacts_treeview = ttk.Treeview(self.contacts_frame, columns=("Name", "Number"))
        self.contacts_treeview.pack()
        self.contacts_treeview.heading("Name", text="Name")
        self.contacts_treeview.heading("Number", text="Number")

        self.column_name_label = tk.Label(self, text="Phone Number Column Name:")
        self.column_name_label.pack(pady=10)
        self.column_name_entry = tk.Entry(self)
        self.column_name_entry.pack()

        self.message_label = tk.Label(self, text="Enter Message:")
        self.message_label.pack(pady=10)
        self.message_text = tk.Text(self, height=5)
        self.message_text.pack()

        self.send_button = ttk.Button(self, text="Send Message", command=self.start_whatsapp_bot)
        self.send_button.pack(pady=10)

        # Initialize variables
        self.file_path = None
        self.contacts = []

    # def open_file_dialog(self):
    #     self.file_path = filedialog.askopenfilename(
    #         initialdir="/",
    #         title="Select CSV File",
    #         filetypes=[("CSV Files", "*.csv")]
    #     )
    #     if self.file_path:
    #         self.process_csv_file()

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=[("CSV files", "*.csv")]
        )
        if self.file_path:
            contacts_converter = contact_converter.ContactConverter(
                self.file_path, self.column_name_entry.get()
            )
            self.contacts = contacts_converter.convert()
            if self.contacts is False:
                messagebox.showerror(
                    title="Error message", message="Invalid column name"
                )
            else:
                self.populate_contacts_treeview()

    def populate_contacts_treeview(self):
        self.contacts_treeview.delete(*self.contacts_treeview.get_children())
        for contact in self.contacts:
            self.contacts_treeview.insert("", "end", text=contact)

    def start_whatsapp_bot(self):
        message = self.message_text.get(1.0, "end").strip()
        if self.contacts and message:
            bot = whatsapp_bot.WhatsAppBot(self.contacts, message, browser="edge")
            result = bot.start()
            if result == "No internet connection":
                messagebox.showwarning(
                    title="Error Message", message="No internet connection"
                )
            elif "Element not found" in result:
                messagebox.showwarning(
                    title="Error Message", message="Element not found"
                )
            else:
                messagebox.showinfo(
                    title="Info", message="Successfully sent to all contacts"
                )
        else:
            messagebox.showwarning(
                title="Warning", message="Please upload a file and enter a message."
            )


   
if __name__ == "__main__":
    app = WhatsAppBotGUI()
    app.mainloop()