import customtkinter as ctk # type: ignore
import tkinter as tk
from tkinter import filedialog, messagebox
import emoji # type: ignore
import time
import threading
from whatsapp_bot import WhatsAppBot
from contact_converter import ContactConverter
from browser_prompt import BrowserPrompt
from emoji_picker import EmojiPicker
from constants import (
    DELAY_BETWEEN_MESSAGES,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    LIGHT_BG,
    DARK_BG,
    LIGHT_TEXT,
    DARK_TEXT,
    LIGHT_ACCENT,
    DARK_ACCENT,
    ERROR_RED
)

class Theme:
    def __init__(self):
        self.mode = "light"
        self.update()

    def toggle(self):
        self.mode = "dark" if self.mode == "light" else "light"
        self.update()

    def update(self):
        if self.mode == "light":
            self.bg = LIGHT_BG
            self.text = LIGHT_TEXT
            self.accent = LIGHT_ACCENT
            ctk.set_appearance_mode("light")
        else:
            self.bg = DARK_BG
            self.text = DARK_TEXT
            self.accent = DARK_ACCENT
            ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

class WhatsAppBotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WhatsApp Bot")
        self.geometry("500x800")
        self.resizable(False, False)
        self.theme = Theme()
        self.configure(fg_color=self.theme.bg)

        self.file_path = None
        self.contacts = []
        self.whatsapp_bot = None
        self.sending_thread = None

        self.create_widgets()
        self.center_window()

        self.browser_prompt = BrowserPrompt(self, self.theme)
        self.wait_window(self.browser_prompt)

        if self.browser_prompt.accepted.get():
            self.selected_browser = self.browser_prompt.browser_var.get()
            self.headless_mode = self.browser_prompt.headless.get()
            self.whatsapp_bot = WhatsAppBot(self.selected_browser, self.log_message, self.headless_mode)
            self.update_browser_label()
        else:
            self.quit()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Header
        header_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header_frame, text="WhatsApp Bot", font=("Roboto", 24, "bold"), text_color="white").grid(row=0, column=0, pady=20)
        
        theme_button = ctk.CTkButton(header_frame, text="🌓", command=self.toggle_theme, width=40, font=("Roboto", 20))
        theme_button.grid(row=0, column=1, padx=20)

        # Browser Info
        browser_frame = ctk.CTkFrame(self, fg_color="transparent")
        browser_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 0))
        browser_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(browser_frame, text="Selected Browser:", font=("Roboto", 14), text_color=self.theme.text).grid(row=0, column=0)
        self.browser_label = ctk.CTkLabel(browser_frame, text="", font=("Roboto", 14), text_color=self.theme.text)
        self.browser_label.grid(row=0, column=1, sticky="w")

        # Main Content
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(20, 10))
        main_frame.grid_columnconfigure(1, weight=1)

        # Input Fields
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Phone Column:", font=("Roboto", 12), text_color=self.theme.text).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.phone_column_entry = ctk.CTkEntry(input_frame, width=200, font=("Roboto", 12))
        self.phone_column_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Name Column:", font=("Roboto", 12), text_color=self.theme.text).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.name_column_entry = ctk.CTkEntry(input_frame, width=200, font=("Roboto", 12))
        self.name_column_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # CSV File Upload
        upload_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        upload_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        upload_frame.grid_columnconfigure(0, weight=1)

        self.file_path_var = tk.StringVar()
        ctk.CTkEntry(upload_frame, textvariable=self.file_path_var, width=400, font=("Roboto", 12), state="readonly").grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(upload_frame, text="Upload CSV", command=self.open_file_dialog, fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR, font=("Roboto", 12, "bold")).grid(row=0, column=1, padx=5)

        # Message Input
        message_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        message_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(20, 0), )
        message_frame.grid_columnconfigure(0, weight=1)
        message_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(message_frame, text="Message:", font=("Roboto", 12), text_color=self.theme.text).grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")
        self.message_text = ctk.CTkTextbox(message_frame, height=100, width=400, font=("Roboto", 12))
        self.message_text.grid(row=1, column=0, padx=5, sticky="nsew")
        
        emoji_button = ctk.CTkButton(message_frame, text="Add Emoji", command=self.show_emoji_picker, 
                                     fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR, 
                                     font=("Roboto", 12, "bold"))
        emoji_button.grid(row=2, column=0, padx=5, pady=(10, 0), sticky="w")

        # Note about personalization
        ctk.CTkLabel(main_frame, text="Note: Messages will be personalized if names are available.", 
                     font=("Roboto", 10, "italic"), text_color=self.theme.text).grid(row=3, column=0, columnspan=3, padx=5, pady=(10, 0), sticky="w")

        # Send and Stop Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.send_button = ctk.CTkButton(button_frame, text="Send Messages", 
                                         command=self.start_whatsapp_bot, 
                                         fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR, 
                                         font=("Roboto", 14, "bold"))
        self.send_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ctk.CTkButton(button_frame, text="Stop Sending", 
                                         command=self.stop_sending, state="disabled", 
                                         fg_color="#e0e0e0", text_color=self.theme.text, 
                                         hover_color="#d0d0d0", font=("Roboto", 14, "bold"))
        self.stop_button.pack(side=tk.LEFT)

        # Progress Bar
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 0))
        progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(progress_frame, orientation="horizontal", mode="determinate")
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.progress_bar.set(0)

        # Log Area
        log_frame = ctk.CTkFrame(self, fg_color="transparent")
        log_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 20))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(log_frame, text="Log Messages:", font=("Roboto", 12), text_color=self.theme.text).grid(row=0, column=0, sticky="w")
        self.log_area = ctk.CTkTextbox(log_frame, height=150, width=760, font=("Roboto", 11))
        self.log_area.grid(row=1, column=0, sticky="nsew")
        self.log_area.tag_config("error", foreground=ERROR_RED)

    def toggle_theme(self):
        self.theme.toggle()
        self.update_theme()

    def update_theme(self):
        self.configure(fg_color=self.theme.bg)
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=self.theme.bg)
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=self.theme.text)
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(fg_color=self.theme.accent, text_color=self.theme.text)
        self.update_browser_label()

    def update_browser_label(self):
        mode = "Headless" if self.headless_mode else "Normal"
        self.browser_label.configure(text=f"{self.selected_browser} ({mode} mode)", text_color=self.theme.text)

    def open_file_dialog(self):
        phone_column = self.phone_column_entry.get().strip()
        name_column = self.name_column_entry.get().strip() or None

        if not phone_column:
            messagebox.showerror("Error", "Please enter the phone number column name.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_var.set(file_path)
            self.file_path = file_path
            self.progress_bar.start()
            threading.Thread(target=self.load_contacts, args=(file_path, phone_column, name_column), daemon=True).start()

    def load_contacts(self, file_path, phone_column, name_column):
        try:
            self.contacts = ContactConverter.convert(file_path, phone_column, name_column)
            self.log_message(f"Loaded {len(self.contacts)} contacts from the CSV file.")
        except Exception as e:
            self.log_message(f"Error: {str(e)}", is_error=True)
            messagebox.showerror("Error", str(e))
        finally:
            self.progress_bar.stop()
            self.progress_bar.set(0)

    def show_emoji_picker(self):
        EmojiPicker(self, self.insert_emoji, self.theme)

    def insert_emoji(self, emoji):
        self.message_text.insert(tk.END, emoji)

    def log_message(self, message, is_error=False):
        self.log_area.insert(tk.END, message + "\n", "error" if is_error else "")
        self.log_area.see(tk.END)

    def start_whatsapp_bot(self):
        message_template = self.message_text.get("1.0", "end").strip()
        if not self.contacts:
            messagebox.showwarning("Warning", "Please upload a CSV file with contacts.")
            return
        if not message_template:
            messagebox.showwarning("Warning", "Please enter a message to send.")
            return

        self.send_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress_bar.set(0)
        self.whatsapp_bot.stop_flag = False
        self.sending_thread = threading.Thread(target=self.run_whatsapp_bot, args=(message_template,), daemon=True)
        self.sending_thread.start()

    def stop_sending(self):
        if self.whatsapp_bot:
            self.whatsapp_bot.stop_flag = True
        self.log_message("Stopping the message sending process...")
        self.stop_button.configure(state="disabled")

    def run_whatsapp_bot(self, message_template):
        try:
            self.whatsapp_bot.initialize_driver()
            total_contacts = len(self.contacts)
            successful_sends = 0

            for i, (phone, name) in enumerate(self.contacts, 1):
                if self.whatsapp_bot.stop_flag:
                    self.log_message("Message sending stopped by user.")
                    break

                personalized_message = f"Hi {name}, " + message_template if name else message_template
                personalized_message = emoji.emojize(personalized_message)
                if self.whatsapp_bot.send_message(phone, personalized_message):
                    successful_sends += 1
                self.title(f"WhatsApp Bot - Progress: {i}/{total_contacts}")
                self.progress_bar.set(i / total_contacts)
                time.sleep(DELAY_BETWEEN_MESSAGES)

                self.log_message(f"Messages sent successfully to {successful_sends} out of {total_contacts} contacts.")
        except Exception as e:
            self.log_message(f"Error: {str(e)}", is_error=True)
        finally:
            self.whatsapp_bot.close()
            self.title("WhatsApp Bot")
            self.send_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.progress_bar.set(0)

def main():
    app = WhatsAppBotGUI()
    app.mainloop()

if __name__ == "__main__":
    main()