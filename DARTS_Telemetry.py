# DARTS_Telemetry.py
# The telemetry monitoring and log location control tab for the DARTS Application.

from customtkinter import (CTkFrame, CTkTextbox)

class TelemetryFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.Text = CTkTextbox(self)
        self.Text.insert("0.0", "Telemetry Frame")
        self.Text.pack()
        self.Text.configure(state="disabled")