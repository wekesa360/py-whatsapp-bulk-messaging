import customtkinter as ctk # type: ignore
from tkinter import Label, font as tkfont
from constants import (
    PRIMARY_COLOR,
)

class EmojiPicker(ctk.CTkToplevel):
    def __init__(self, master, callback, theme):
        super().__init__(master)
        self.title("Emoji Picker")
        self.geometry("400x400")
        self.theme = theme
        self.configure(fg_color=self.theme.bg)
        self.callback = callback


        self.emoji_list = [
            "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
            "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩", "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣",
            "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗",
            "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵", "🤐",
            "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🤠", "😈", "👿", "👹", "👺", "🤡", "💩", "👻", "💀", "☠️", "👽", "👾",
            "🤖", "🎃", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "👋", "🤚", "🖐", "✋", "🖖", "👌", "🤌", "🤏", "✌️",
            "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "🖕", "👇", "☝️", "👍", "👎", "✊", "👊", "🤛", "🤜", "👏", "🙌", "👐", "🤲",
            "🤝", "🙏", "✍️", "💅", "🤳", "💪", "🦾", "🦵", "🦿", "🦶", "👣", "👂", "🦻", "👃", "🫀", "🫁", "🧠", "🦷", "🦴", "👀",
            "👁", "👅", "👄", "💋", "🩸", "🐵", "🐒", "🦍", "🦧", "🐶", "🐕", "🦮", "🐩", "🐺", "🦊", "🦝", "🐱", "🐈", "🦁", "🐯",
            "🐅", "🐆", "🐴", "🐎", "🦄", "🦓", "🦌", "🦬", "🐮", "🐂", "🐃", "🐄", "🐷", "🐖", "🐗", "🐽", "🐏", "🐑", "🐐", "🐪"
        ]

        self.create_emoji_buttons()

    def create_emoji_buttons(self):
        # Create a canvas with scrollbar
        canvas = ctk.CTkCanvas(self, bg=self.theme.bg, highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=canvas.yview)
        
        # Create a frame inside the canvas
        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color=self.theme.bg)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Try different fonts
        emoji_fonts = ["Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", "Twitter Color Emoji", "EmojiOne Color"]
        emoji_font = None
        for font_name in emoji_fonts:
            try:
                emoji_font = tkfont.Font(family=font_name, size=24)
                break
            except:
                continue

        if emoji_font is None:
            emoji_font = tkfont.nametofont("TkDefaultFont").copy()
            emoji_font.config(size=24)

        # Create labels for each emoji
        for i, emoji_char in enumerate(self.emoji_list):
            label = Label(self.scrollable_frame, text=emoji_char, font=emoji_font, bg=self.theme.bg)
            label.grid(row=i // 8, column=i % 8, padx=2, pady=2)
            label.bind("<Button-1>", lambda e, emoji=emoji_char: self.select_emoji(emoji))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_emoji(self, emoji):
        self.callback(emoji)
        self.destroy()