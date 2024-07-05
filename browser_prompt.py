import customtkinter as ctk # type: ignore
from tkinter import messagebox
from constants import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    DARK_ACCENT,
)


class BrowserPrompt(ctk.CTkToplevel):
    def __init__(self, master, theme):
        super().__init__(master)
        self.title("Browser Selection")
        self.geometry("350x400")
        self.resizable(False, False)
        self.theme = theme
        self.configure(fg_color=self.theme.bg)

        self.browser_var = ctk.StringVar(value="Chrome")
        self.accepted = ctk.BooleanVar(value=False)
        self.headless = ctk.BooleanVar(value=False)

        ctk.CTkLabel(self, text="Select a browser", font=("Roboto", 20, "bold"), 
                     text_color=self.theme.text).pack(pady=20)
        
        radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame.pack(pady=10)
        for browser in ["Chrome", "Firefox", "Edge"]:
            ctk.CTkRadioButton(radio_frame, text=browser, variable=self.browser_var, 
                               value=browser, font=("Roboto", 16), text_color=self.theme.text,
                               fg_color=SECONDARY_COLOR, hover_color=DARK_ACCENT,
                               border_color=PRIMARY_COLOR).pack(pady=8, anchor="w")

        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.pack(pady=15, anchor="w", padx=20)

        self.accept_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(checkbox_frame, text="I have at least one of these browsers installed",
                        variable=self.accept_var, font=("Roboto", 14), 
                        text_color=self.theme.text, fg_color=SECONDARY_COLOR, 
                        hover_color=DARK_ACCENT, border_color=PRIMARY_COLOR).pack(pady=8, anchor="w") 

        ctk.CTkCheckBox(checkbox_frame, text="Run in headless mode", variable=self.headless,
                        font=("Roboto", 14), text_color=self.theme.text,
                        fg_color=SECONDARY_COLOR, hover_color=DARK_ACCENT,
                        border_color=PRIMARY_COLOR, command=self.on_headless).pack(pady=8, anchor="w") 


        ctk.CTkButton(self, text="Continue", command=self.on_continue,
                      font=("Roboto", 16, "bold"), fg_color=PRIMARY_COLOR,
                      hover_color=SECONDARY_COLOR, text_color="white",
                      height=40, width=120, corner_radius=10).pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.transient(master)
        self.grab_set()

    def on_headless(self):
        if self.headless.get():
            if messagebox.askyesno("Headless Mode", "Running in headless mode requires Firefox. Do you have Firefox installed?"):
                self.browser_var.set("Firefox")
            else:
                self.headless.set(False)

    def on_continue(self):
        if self.accept_var.get():
            self.accepted.set(True)
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Please confirm that you have at least one of the listed browsers installed.")

    def on_close(self):
        self.accepted.set(False)
        self.destroy()