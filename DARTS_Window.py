# Darts_Window.py
# The main window for the DARTS Application.

import __main__
import time

from customtkinter import (CTk, CTkFrame, CTkTabview, CTkButton, CTkFont, CTkComboBox, CTkLabel)

from DARTS_Attitude import AttitudeFrame
from DARTS_Targets import TargetsFrame
from DARTS_Gains import GainsFrame
from DARTS_Telemetry import TelemetryFrame
from DARTS_Settings import SettingsFrame
from DARTS_Debug import DebugFrame

import DARTS_API as api
import DARTS_Utilities as util

class Window(CTk):
    def __init__(self):
        super().__init__()

        __main__.DARTS_Settings.register("Settings_Halt", True, [True, False])
        __main__.DARTS_Settings.register("Settings_AngleType", "Degrees", ["Degrees", "Radians"])
        __main__.DARTS_Settings.register("Settings_QuaternionType", "Q4", ["Q0", "Q4"])
        __main__.DARTS_Settings.register("Settings_PlotDuration")

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

        self.Q0Text = "[Q0, Q1, Q2, Q3]"
        self.Q4Text = "[Q1, Q2, Q3, Q4]"

        self.AngleLabel = CTkLabel(self, text="Angle Representation:", justify="left")
        self.AngleComboBox = CTkComboBox(self, values=["Degrees", "Radians"], command=self.AngleRepresentation_Callback)
        self.AngleLabel.pack()
        self.AngleComboBox.pack()

        self.AngleComboBox.set(api.Settings_Get_AngleType())
        
        self.QuaternionLabel = CTkLabel(self, text="Quaternion Representation:", justify="left")
        self.QuaternionComboBox = CTkComboBox(self, values=[self.Q0Text, self.Q4Text], command=self.QuaternionRepresentation_Callback)
        self.QuaternionLabel.pack()
        self.QuaternionComboBox.pack()

        self.QuaternionComboBox.set({"Q0": self.Q0Text, "Q4": self.Q4Text}[api.Settings_Get_QuaternionType()])
        
    
    def StartButton_Callback(self):
        util.StartTestbed()
    
    def HaltButton_Callback(self):
        util.StopTestbed()

    def AngleRepresentation_Callback(self, setting):
        api.Settings_Set_AngleType(setting)

    def QuaternionRepresentation_Callback(self, setting):
        api.Settings_Set_QuaternionType({self.Q0Text: "Q0", self.Q4Text: "Q4"}[setting])