# DARTS_Gains.py
# The gain control tab for the DARTS Application.

from customtkinter import (CTkFrame, CTkTextbox)

class GainsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.Text = CTkTextbox(self)
        self.Text.insert("0.0", "Gains Frame")
        self.Text.pack()
        self.Text.configure(state="disabled")