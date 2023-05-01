import tkinter as tk
from tkinter import filedialog

class Upload:
    def __init__(self):
        self.file_path = None

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(initialdir="/",title="Select file",
                                                    filetypes=[("CSV files", "*.csv")])
        return self.file_path

