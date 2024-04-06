import ttkbootstrap as ttk
from ttkbootstrap import Window
from ttkbootstrap.style import use
from tkinter import filedialog
from tkinter import messagebox
import contact_converter
import whatsapp_bot

class App:
    def __init__(self):
        self.root = Window(themename="superhero")
        self.root.title("WhatsApp Bulk Messaging")
        self.root.geometry("670x833")
        self.root.resizable(False, False)

        # Create UI elements
        self.title_label = ttk.Label(
            self.root,
            text="WhatsApp Bulk Messaging",
            bootstyle="primary",
            font=("Helvetica", 24),
        )
        self.column_name_label = ttk.Label(
            self.root, text="Column name containing contacts", font=("Helvetica", 12)
        )
        self.column_name_entry = ttk.Entry(self.root, font=("Helvetica", 12))
        self.message_label = ttk.Label(
            self.root, text="Message", font=("Helvetica", 12)
        )
        self.message_text = ttk.Text(self.root, height=5, font=("Helvetica", 12))
        self.upload_button = ttk.Button(
            self.root,
            text="UPLOAD FILE",
            command=self.open_file_dialog,
            bootstyle="outline-primary",
        )
        self.clear_button = ttk.Button(
            self.root, text="CLEAR", command=self.clear, bootstyle="outline-danger"
        )
        self.ready_button = ttk.Button(
            self.root,
            text="READY",
            command=self.start_whatsapp_bot,
            bootstyle="success",
        )
        self.output_label = ttk.Label(self.root, text="Output", font=("Helvetica", 12))

        # Create a custom style for the Treeview widget
        use("Treeview", font=('Helvetica', 12))

        # Create the Treeview widget and apply the custom style
        self.contacts_output = ttk.Treeview(self.root, show="tree", selectmode="browse", style='Treeview')
        self.contacts_output.configure(columns=(), height=8)
        self.contacts_output.heading("#0", text="", anchor="w")

        # Layout the UI elements
        self.title_label.grid(
            row=0, column=0, columnspan=2, padx=20, pady=20, sticky="n"
        )
        self.column_name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.column_name_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.message_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.message_text.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.upload_button.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.clear_button.grid(row=5, column=1, padx=20, pady=10, sticky="w")
        self.ready_button.grid(
            row=6, column=0, columnspan=2, padx=20, pady=10, sticky="ew"
        )
        self.output_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        self.contacts_output.grid(
            row=8, column=0, columnspan=2, padx=20, pady=10, sticky="ew"
        )

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def clear(self):
        self.column_name_entry.delete(0, "end")
        self.message_text.delete(1.0, "end")
        self.contacts_output.delete(*self.contacts_output.get_children())

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
                self.populate_contacts_output()

    def populate_contacts_output(self):
        self.contacts_output.delete(*self.contacts_output.get_children())
        for contact in self.contacts:
            self.contacts_output.insert("", "end", text=contact)

    def start_whatsapp_bot(self):
        message = self.message_text.get(1.0, "end").strip()
        if self.contacts and message:
            bot = whatsapp_bot.WhatsAppBot(self.contacts, message)
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

def main():
    app = App()
    app.root.mainloop()

if __name__ == "__main__":
    main()