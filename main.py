import tkinter as tk
from tkinter import filedialog
from contact_converter.contact_converter import ContactConverter
from tkinter import messagebox
from whatsapp_bot.whatsapp_bot import WhatsAppBot
import tkinter.font as tkFont
import sys

class App:
    def __init__(self, root):
        self.file_path = None
        self.contacts = None
        #setting title
        root.title("WhatsApp Bulk Messaging")
        #setting window size
        width=670
        height=833
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_636=tk.Button(root)
        GButton_636["bg"] = "#e1e1e1"
        ft = tkFont.Font(family='Times',size=10)
        GButton_636["font"] = ft
        GButton_636["fg"] = "#000000"
        GButton_636["justify"] = "center"
        GButton_636["text"] = "UPLOAD FILE"
        GButton_636.place(x=110,y=420,width=89,height=30)
        GButton_636["command"] = self.open_file_dialog

        clear_btn=tk.Button(root)
        clear_btn["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        clear_btn["font"] = ft
        clear_btn["fg"] = "#000000"
        clear_btn["justify"] = "center"
        clear_btn["text"] = "CLEAR"
        clear_btn.place(x=220,y=420,width=102,height=30)
        clear_btn["command"] = self.clear

        self.ready_button=tk.Button(root)
        self.ready_button["bg"] = "#5fb878"
        ft = tkFont.Font(family='Times',size=10)
        self.ready_button["font"] = ft
        self.ready_button["fg"] = "#ffffff"
        self.ready_button["justify"] = "center"
        self.ready_button["text"] = "READY"
        self.ready_button.place(x=110,y=470,width=440,height=30)
        self.ready_button["command"] = self.start_whatsapp_bot

        self.message = tk.Text(root)
        self.message["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        self.message["font"] = ft
        self.message["fg"] = "#333333"
        self.message.place(x=110,y=280,width=436,height=105)

        self.column_name = tk.Entry(root)
        self.column_name["bg"] = "#ffffff"
        self.column_name["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.column_name["font"] = ft
        self.column_name["fg"] = "#333333"
        self.column_name.place(x=110,y=170,width=431,height=41)

        self.contacts_output=tk.Listbox(root)
        self.contacts_output["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.contacts_output["font"] = ft
        self.contacts_output["fg"] = "#333333"
        self.contacts_output.place(x=110,y=550,width=446,height=162)

        self.label_column_name = tk.Label(root)
        ft = tkFont.Font(family='Times',size=11)
        self.label_column_name["font"] = ft
        self.label_column_name["fg"] = "#333333"
        self.label_column_name["text"] = "Column name containing contacts"
        self.label_column_name.place(x=110,y=130,width=404,height=30)

        self.tittle_label=tk.Label(root)
        
        self.tittle_label["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=30)
        self.tittle_label["font"] = ft
        self.tittle_label["fg"] = "#333333"
        self.tittle_label["justify"] = "center"
        self.tittle_label["text"] = "Whatsapp Bulk Messaging"
        self.tittle_label.place(x=80,y=30,width=509,height=71)

        self.message_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=11)
        self.message_label["font"] = ft
        self.message_label["fg"] = "#333333"
        self.message_label["justify"] = "left"
        self.message_label["text"] = "Message"
        self.message_label.place(x=110,y=240,width=70,height=25)

        self.output_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=11)
        self.output_label["font"] = ft
        self.output_label["fg"] = "#333333"
        self.output_label["justify"] = "center"
        self.output_label["text"] = "Output"
        self.output_label.place(x=100,y=520,width=70,height=25)

    def clear(self):
        self.column_name.delete(0, 'end')
        self.message.delete(1.0, 'end')
        self.contacts_output.delete(1.0, 'end')
        return None


    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(initialdir='/', title='Select file',
                                                    filetypes=[("CSV files", "*.csv")])
        contacts_converter = ContactConverter(self.file_path, self.column_name.get())
        self.contacts = contacts_converter.convert()

        return self.file_path

    def start_whatsapp_bot(self):
        message = self.message.get(1.0, 'end')
        bot = WhatsAppBot(self.contacts, message)
        bot.start()



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    
    
    