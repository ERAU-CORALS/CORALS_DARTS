# DARTS_Settings.py
# The testbed settings control tab for the DARTS Application.

from customtkinter import (CTkFrame, CTkTextbox)

class SettingsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.Text = CTkTextbox(self)
        self.Text.insert("0.0", "Settings Frame")
        self.Text.pack()
        self.Text.configure(state="disabled")