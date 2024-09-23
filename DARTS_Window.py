# Darts_Window.py
# The main window for the DARTS Application.

import __main__
import time

from customtkinter import (CTk, CTkFrame, CTkTabview, CTkButton, CTkFont, CTkComboBox)

from DARTS_Attitude import AttitudeFrame
from DARTS_Targets import TargetsFrame
from DARTS_Gains import GainsFrame
from DARTS_Telemetry import TelemetryFrame
from DARTS_Settings import SettingsFrame
from DARTS_Debug import DebugFrame

class Window(CTk):
    def __init__(self):
        super().__init__()

        self.title("DARTS - Data Acquisition and Remote Telecommand Script")
        self.geometry("1024x768")
        self.minsize(800, 600)
        self.resizable(True, True)

        self.MainFrame = MainFrame(self)
        self.MainFrame.grid(row=0, column=0, sticky="nsew")
        self.SideFrame = SideFrame(self)
        self.SideFrame.grid(row=0, column=1, sticky="nsew") 

class MainFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.MainTabs = MainTabs(self)
        self.MainTabs.pack()

class MainTabs(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.OuterAttitudeFrame     = self.add("Attitude")
        self.OuterTargetsFrame      = self.add("Targets")
        self.OuterGainsFrame        = self.add("Gains")
        self.OuterTelemetryFrame    = self.add("Telemetry")
        self.OuterSettingsFrame     = self.add("Settings")
        self.OuterDebugFrame        = self.add("Debug")

        self.InnerAttitudeFrame     = AttitudeFrame(self.tab("Attitude"))
        self.InnerTargetsFrame      = TargetsFrame(self.tab("Targets"))
        self.InnerGainsFrame        = GainsFrame(self.tab("Gains"))
        self.InnerTelemetryFrame    = TelemetryFrame(self.tab("Telemetry"))
        self.InnerSettingsFrame     = SettingsFrame(self.tab("Settings"))
        self.InnerDebugFrame        = DebugFrame(self.tab("Debug"))

        self.InnerAttitudeFrame.pack()
        self.InnerTargetsFrame.pack()
        self.InnerGainsFrame.pack()
        self.InnerTelemetryFrame.pack()
        self.InnerSettingsFrame.pack()
        self.InnerDebugFrame.pack()

class SideFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.ButtonFont = CTkFont(family="sans-serif", size=30, weight="bold")

        self.StartButton = CTkButton(self, text="START", text_color="white", fg_color="lime", hover_color="green", font=self.ButtonFont, command=self.StartButton_Callback)
        self.HaltButton = CTkButton(self, text="HALT", text_color="white", fg_color="red", hover_color="maroon", font=self.ButtonFont, command=self.HaltButton_Callback)

        self.StartButton.pack()
        self.HaltButton.pack()

        self.AngleComboBox = CTkComboBox(self, values=["Degrees", "Radians"], command=self.AngleRepresentation_Callback)
        self.AngleComboBox.pack()
    
    def StartButton_Callback(self):
        __main__.DARTS_Settings["Halt"] = False
        __main__.DARTS_Settings["StartTime"] = time.time()
        __main__.DARTS_Settings["AttitudeDisplayTime"] = []
    
    def HaltButton_Callback(self):
        __main__.DARTS_Settings["Halt"] = True

    def AngleRepresentation_Callback(self, setting):
        __main__.DARTS_Settings["AngleType"] = setting