# DARTS_Targets.py
# The target control tab for the DARTS Application.

from customtkinter import (CTkFrame, CTkTextbox)

class TargetsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.Text = CTkTextbox(self)
        self.Text.insert("0.0", "Targets Frame")
        self.Text.pack()
        self.Text.configure(state="disabled")