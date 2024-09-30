# Darts_Window.py
# The main window for the DARTS Application.

import __main__
import time

from customtkinter import (CTk, CTkFrame, CTkTabview, CTkButton, CTkFont, CTkSegmentedButton, CTkComboBox, CTkLabel, CTkImage)
from PIL import Image

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

        self.title("DARTS - Data Acquisition and Remote Telecommand Script")
        self.geometry("1024x768")
        self.minsize(800, 600)
        self.resizable(True, True)

        self.MainFrame = MainFrame(self)
        self.MainFrame.place(relx=0, rely=0, relwidth=0.75, relheight=1, anchor="nw")
        self.SideFrame = SideFrame(self)
        self.SideFrame.place(relx=1, rely=0, relwidth=0.25, relheight=1, anchor="ne")

class MainFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.MainTabs = MainTabs(self)
        self.MainTabs.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")

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

        self.InnerAttitudeFrame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")
        self.InnerTargetsFrame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")
        self.InnerGainsFrame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")
        self.InnerTelemetryFrame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")
        self.InnerSettingsFrame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")
        self.InnerDebugFrame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

class SideFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.LogoImage = Image.open("DARTS_Icon.png")
        self.LogoImageCTk = CTkImage(self.LogoImage, size=(self._current_width, self._current_width))
        self.Logo = CTkLabel(self, image=self.LogoImageCTk, text="")
        self.Logo.pack(fill="x")

        self.ButtonFont = CTkFont(family="sans-serif", size=30, weight="bold")

        self.StartButton = CTkButton(self, text="START", text_color="white", fg_color="lime", hover_color="green", font=self.ButtonFont, command=self.StartButton_Callback)
        self.HaltButton = CTkButton(self, text="HALT", text_color="white", fg_color="red", hover_color="maroon", font=self.ButtonFont, command=self.HaltButton_Callback)

        self.StartButton.place(relx=0.5, rely=0.8, relwidth=0.9, relheight=0.1, anchor="center")
        self.HaltButton.place(relx=0.5, rely=0.9, relwidth=0.9, relheight=0.1, anchor="center")

        self.Q0Text = "[Q0, Q1, Q2, Q3]"
        self.Q4Text = "[Q1, Q2, Q3, Q4]"

        self.AngleLabel = CTkLabel(self, text="Angle Representation:", justify="left")
        self.AngleComboBox = CTkSegmentedButton(self, values=["Degrees", "Radians"], command=self.AngleRepresentation_Callback)
        self.AngleLabel.pack(anchor="w")
        self.AngleComboBox.pack(anchor="w", fill="x")

        self.AngleComboBox.set(api.Settings_Get_AngleType())
        
        self.QuaternionLabel = CTkLabel(self, text="Quaternion Representation:", justify="left")
        self.QuaternionComboBox = CTkComboBox(self, values=[self.Q0Text, self.Q4Text], command=self.QuaternionRepresentation_Callback)
        self.QuaternionLabel.pack(anchor="w")
        self.QuaternionComboBox.pack(anchor="w", fill="x")

        self.QuaternionComboBox.set({"Q0": self.Q0Text, "Q4": self.Q4Text}[api.Settings_Get_QuaternionType()])
        
    
    def StartButton_Callback(self):
        util.StartTestbed()
    
    def HaltButton_Callback(self):
        util.StopTestbed()

    def AngleRepresentation_Callback(self, setting):
        api.Settings_Set_AngleType(setting)

    def QuaternionRepresentation_Callback(self, setting):
        api.Settings_Set_QuaternionType({self.Q0Text: "Q0", self.Q4Text: "Q4"}[setting])