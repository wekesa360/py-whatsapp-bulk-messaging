import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from constants import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    DARK_ACCENT,
)


class BrowserPrompt(ctk.CTkToplevel):
    def __init__(self, master, theme, first_run=True):
        super().__init__(master)
        self.title("Browser Selection")
        self.geometry("400x450")
        self.resizable(False, False)
        self.theme = theme
        self.configure(fg_color="white")
        self.first_run = first_run

        # Set background to white
        self.create_white_bg()

        self.browser_var = ctk.StringVar(value="Chrome")
        self.accepted = ctk.BooleanVar(value=False)
        self.headless = ctk.BooleanVar(value=False)

        ctk.CTkLabel(self, text="Select a browser", font=("Roboto", 24, "bold"), 
                     text_color="black").pack(pady=25)
        
        radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame.pack(pady=15)

        # Load browser icons
        chrome_icon = self.load_icon("chrome.png")
        firefox_icon = self.load_icon("firefox.svg")
        edge_icon = self.load_icon("edge.png")

        browsers = [("Chrome", chrome_icon), ("Firefox", firefox_icon), ("Edge", edge_icon)]
        for browser, icon in browsers:
            browser_frame = ctk.CTkFrame(radio_frame, fg_color="transparent")
            browser_frame.pack(pady=10, fill="x", expand=True)
            
            ctk.CTkLabel(browser_frame, image=icon, text="").pack(side="left", padx=(0, 10))
            ctk.CTkRadioButton(browser_frame, text=browser, variable=self.browser_var, 
                               value=browser, font=("Roboto", 16), text_color="black",
                               fg_color=SECONDARY_COLOR, hover_color=DARK_ACCENT,
                               border_color=PRIMARY_COLOR).pack(side="left")

        ctk.CTkFrame(self, height=2, fg_color=SECONDARY_COLOR).pack(fill="x", padx=20, pady=15)

        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.pack(pady=15, anchor="w", padx=30)

        self.accept_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(checkbox_frame, text="I have at least one of these browsers installed",
                        variable=self.accept_var, font=("Roboto", 14), 
                        text_color="black", fg_color=SECONDARY_COLOR, 
                        hover_color=DARK_ACCENT, border_color=PRIMARY_COLOR).pack(pady=8, anchor="w") 

        if not self.first_run:
            ctk.CTkCheckBox(checkbox_frame, text="Run in headless mode", variable=self.headless,
                            font=("Roboto", 14), text_color="black",
                            fg_color=SECONDARY_COLOR, hover_color=DARK_ACCENT,
                            border_color=PRIMARY_COLOR).pack(pady=8, anchor="w") 

        continue_button = ctk.CTkButton(self, text="Continue", command=self.on_continue,
                      font=("Roboto", 16, "bold"), fg_color=PRIMARY_COLOR,
                      hover_color=SECONDARY_COLOR, text_color="white",
                      height=40, width=120, corner_radius=10)
        continue_button.pack(pady=25)
        
        # Add hover effect
        continue_button.bind("<Enter>", lambda e: continue_button.configure(fg_color=SECONDARY_COLOR))
        continue_button.bind("<Leave>", lambda e: continue_button.configure(fg_color=PRIMARY_COLOR))

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.transient(master)
        self.grab_set()

    def create_white_bg(self):
        self.configure(bg="white")

    def load_icon(self, filename):
        return ctk.CTkImage(Image.open(f"icons/{filename}"), size=(24, 24))

    def on_continue(self):
        if self.accept_var.get():
            if self.first_run and self.headless.get():
                messagebox.showwarning("Warning", "Headless mode is not allowed due to WhatsApp QR code requirement.")
            else:
                self.accepted.set(True)
                self.destroy()
        else:
            messagebox.showwarning("Warning", "Please confirm that you have at least one of the listed browsers installed.")

    def on_close(self):
        self.accepted.set(False)
        self.destroy()