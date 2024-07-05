import customtkinter as ctk # type: ignore
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
        canvas = ctk.CTkCanvas(self, bg=self.theme.bg, highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color=self.theme.bg)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, emoji_char in enumerate(self.emoji_list):
            btn = ctk.CTkButton(scrollable_frame, text=emoji_char, font=("Segoe UI Emoji", 20),
                                command=lambda x=emoji_char: self.select_emoji(x),
                                fg_color=self.theme.accent, text_color=self.theme.text,
                                hover_color=PRIMARY_COLOR, width=40, height=40)
            btn.grid(row=i // 8, column=i % 8, padx=2, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_emoji(self, emoji):
        self.callback(emoji)
        self.destroy()