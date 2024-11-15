# DARTS_Attitude.py
# The attitude reporting tab for the DARTS Application.

import __main__
import time

from customtkinter import (CTk, CTkCheckBox, CTkComboBox, CTkFrame, CTkLabel, CTkTextbox, CTkButton)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np

import DARTS_API as api
import DARTS_Utilities as util
from DARTS_Render import DARTS_RenderingFrame

def _Attitude_Print(value: str):
    util.Debug_Print(__file__, value, __main__.Environment["DEBUG_ATTITUDE_PAGE"])

def _Attitude_Active() -> bool:
    return __main__.App.MainFrame.MainTabs.get() == "Attitude"
class AttitudeFrame(CTkFrame):

    def __init__(self, master, **kwargs):
        _Attitude_Print("Initializing Attitude Frame")

        super().__init__(master, **kwargs)

        self.GraphSettingsFrame = AttitudeGraphSettingsFrame(self)
        self.AttitudeRenderingFrame = AttitudeRenderingFrame(self)
        self.TimeGraphFrame = AttitudeTimeGraphFrame(self, self.GraphSettingsFrame)

        self.AttitudeRenderingFrame.place(relx=0, rely=0, relwidth=0.5, relheight=0.75, anchor="nw")
        self.TimeGraphFrame.place(relx=1, rely=0, relwidth=0.5, relheight=0.75, anchor="ne")
        self.GraphSettingsFrame.place(relx=1, rely=1, relwidth=0.5, relheight=0.25, anchor="se")

class AttitudeRenderingFrame(DARTS_RenderingFrame):
    def __init__(self, master, **kwargs):
        _Attitude_Print("Initializing Attitude Rendering Frame")

        super().__init__(master, **kwargs)

        self.plot_axes()

        self.Canvas.draw()
        self.Canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        self.after(2500, self.draw_attitude_process)

    def draw_attitude_process(self):
        _Attitude_Print("Drawing Attitude Process")
        
        if _Attitude_Active():

            self.draw_attitude_callback()
        
        self.after(200, self.draw_attitude_process)

    def draw_attitude_callback(self):
        _Attitude_Print("Drawing Attitude Callback")

        self.Axes.clear()
        
        self.Axes.set_xlim(-1, 1)
        self.Axes.set_ylim(-1, 1)
        self.Axes.set_zlim(-1, 1)

        self.Axes.set_xticks([-1, 1])
        self.Axes.set_yticks([-1, 1])
        self.Axes.set_zticks([-1, 1])

        self.plot_axes()

        _Attitude_Print("Plotting Current Attitude")
        self.plot_vector(self.Axes, angles=api.Attitude_Get_Current_Type(type="RPY Angles"), degrees=False, color='c')
        
        if len(api.Targets_Get_List()) > 0:
            _Attitude_Print("Plotting Current Target")
            self.plot_vector(self.Axes, angles=util.Convert_Quaternion_to_RPY(api.Targets_Get_List()[0]), degrees=False, color='k')
    
        self.Canvas.draw()

class AttitudeTimeGraphFrame(CTkFrame):
    def __init__(self, master, settings, **kwargs):
        _Attitude_Print("Initializing Attitude Time Graph Frame")

        super().__init__(master, **kwargs)

        self.Settings = settings

        self.Figure = Figure(figsize=(5, 5), dpi=100)
        self.Axes   = self.Figure.add_subplot(111)
        self.AltAxes = self.Axes.twinx()
        
        self.start_time = time.time()

        self.Canvas = FigureCanvasTkAgg(self.Figure, self)
        self.Canvas.draw()
        self.Canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        self.after(2500, self.draw_data_process)

    def draw_data_process(self): 
        _Attitude_Print("Drawing Data Process")
        
        if _Attitude_Active():
            self.draw_data_callback()

        self.after(1000, self.draw_data_process)

    def draw_data_callback(self):  
        _Attitude_Print("Drawing Data Callback")

        self.Axes.clear()
        self.AltAxes.clear()

        time_data = api.Attitude_Plot_Get_TimeData()

        if len(time_data) >= 2:

            self.Axes.set_xlim(time_data[0], time_data[-1])
            self.AltAxes.set_xlim(time_data[0], time_data[-1])
            
            if util.AttitudePlot_IsRPYAngles():

                [roll_data, pitch_data, yaw_data] = api.Attitude_Plot_Get_AttitudeData(type="RPY Angles")

                del roll_data[len(time_data):]
                del pitch_data[len(time_data):]
                del yaw_data[len(time_data):]

                legend_entries = []
                
                if self.Settings.RollCheckbox.get():
                    if util.AngleType_IsDegrees():
                        roll_data = np.degrees(roll_data)
                    self.Axes.plot(time_data, roll_data, color="red")
                    legend_entries.append("Roll")
                
                if self.Settings.PitchCheckbox.get():
                    if util.AngleType_IsDegrees():
                        pitch_data = np.degrees(pitch_data)
                    self.Axes.plot(time_data, pitch_data, color="green")
                    legend_entries.append("Pitch")
                
                if self.Settings.YawCheckbox.get():
                    if util.AngleType_IsDegrees():
                        yaw_data = np.degrees(yaw_data)
                    self.Axes.plot(time_data, yaw_data, color="blue")
                    legend_entries.append("Yaw")

                self.Axes.legend(legend_entries, loc='upper left')

                if util.AngleType_IsDegrees():
                    self.Axes.set_ylim(-180, 180) 
                    self.Axes.set_yticks([-180, -90, 0, 90, 180])
                    self.Axes.set_yticklabels(["-180°", "-90°", "0°", "90°", "180°"])
                else:
                    self.Axes.set_ylim(-np.pi, np.pi) 
                    self.Axes.set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
                    self.Axes.set_yticklabels(["-π", "-π/2", "0", "π/2", "π"])
                self.Axes.set_ylabel("Angle")
                
                self.AltAxes.set_ylabel("")
                self.AltAxes.set_yticks([])
                self.AltAxes.set_ylabel("")
                
            elif util.AttitudePlot_IsEulerParameters():

                euler_data = api.Attitude_Plot_Get_AttitudeData(type="Euler Parameters")
                [e1_data, e2_data, e3_data] = euler_data["axis"]
                phi_data = euler_data["angle"]

                del e1_data[len(time_data):]
                del e2_data[len(time_data):]
                del e3_data[len(time_data):]
                del phi_data[len(time_data):]

                legend_entries = []

                if self.Settings.E1Checkbox.get():
                    self.Axes.plot(time_data, e1_data, color="red")
                    legend_entries.append("E1")
                
                if self.Settings.E2Checkbox.get():
                    self.Axes.plot(time_data, e2_data, color="green")
                    legend_entries.append("E2")
                
                if self.Settings.E3Checkbox.get():
                    self.Axes.plot(time_data, e3_data, color="blue")
                    legend_entries.append("E3")

                self.Axes.legend(legend_entries, loc='upper left')
                self.Axes.set_ylim(-1, 1)
                self.Axes.set_yticks([-1, -0.5, 0, 0.5, 1])
                self.Axes.set_ylabel("Euler Parameter")
                
                if self.Settings.PhiCheckbox.get():
                    if util.AngleType_IsDegrees():
                        phi_data = np.degrees(phi_data)
                    self.AltAxes.plot(time_data, phi_data, color="cyan")
                
                    self.AltAxes.legend(["Phi"], loc='upper right')
                    if util.AngleType_IsDegrees():
                        self.AltAxes.set_ylim(0, 360)
                        self.AltAxes.set_yticks([0, 90, 180, 270, 360])
                        self.AltAxes.set_yticklabels(["0°", "90°", "180°", "270°", "360°"])
                    else:
                        self.AltAxes.set_ylim(0, 2*np.pi)
                        self.AltAxes.set_yticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
                        self.AltAxes.set_yticklabels(["0", "π/2", "π", "3π/2", "2π"])
                    self.AltAxes.set_ylabel("Euler Angle", color='cyan')
                    self.AltAxes.get_yaxis().set_label_position("right")

                else:
                    self.AltAxes.set_ylabel("")
                    self.AltAxes.set_yticks([])
                    self.AltAxes.set_ylabel("")
                
            elif util.AttitudePlot_IsGibbsRodriguez():

                [p1_data, p2_data, p3_data] = api.Attitude_Plot_Get_AttitudeData(type="Gibbs-Rodriguez")

                del p1_data[len(time_data):]
                del p2_data[len(time_data):]
                del p3_data[len(time_data):]

                legend_entries = []

                if self.Settings.P1Checkbox.get():
                    self.Axes.plot(time_data, p1_data, color="red")
                    legend_entries.append("P1")
                
                if self.Settings.P2Checkbox.get():
                    self.Axes.plot(time_data, p2_data, color="green")
                    legend_entries.append("P2")
                
                if self.Settings.P3Checkbox.get():
                    self.Axes.plot(time_data, p3_data, color="blue")
                    legend_entries.append("P3")
                
                self.Axes.legend(legend_entries, loc='upper left')
                self.Axes.set_ylabel("GR Parameter")
                
                self.AltAxes.set_ylabel("")
                self.AltAxes.set_yticks([])
                self.AltAxes.set_ylabel("")
                
            elif util.AttitudePlot_IsQuaternion():

                [q1_data, q2_data, q3_data, q4_data] = api.Attitude_Plot_Get_AttitudeData(type="Quaternion")

                del q1_data[len(time_data):]
                del q2_data[len(time_data):]
                del q3_data[len(time_data):]
                del q4_data[len(time_data):]
                
                legend_entries = []

                if self.Settings.Q0Checkbox.get() and api.Settings_Get_QuaternionType() == "Q0":
                    self.Axes.plot(time_data, q4_data, color="cyan")
                    legend_entries.append("Q0")
                
                if self.Settings.Q1Checkbox.get():
                    self.Axes.plot(time_data, q1_data, color="red")
                    legend_entries.append("Q1")
                
                if self.Settings.Q2Checkbox.get():
                    self.Axes.plot(time_data, q2_data, color="green")
                    legend_entries.append("Q2")
                
                if self.Settings.Q3Checkbox.get():
                    self.Axes.plot(time_data, q3_data, color="blue")
                    legend_entries.append("Q3")

                if self.Settings.Q4Checkbox.get() and api.Settings_Get_QuaternionType() == "Q4":
                    self.Axes.plot(time_data, q4_data, color="cyan")
                    legend_entries.append("Q4")

                self.Axes.legend(legend_entries, loc='upper left')
                self.Axes.set_ylim(-1, 1)
                self.Axes.set_yticks([-1, -0.5, 0, 0.5, 1])
                self.Axes.set_ylabel("Quaternion")
                
                self.AltAxes.set_ylabel("")
                self.AltAxes.set_yticks([])
                self.AltAxes.set_ylabel("")

            self.Canvas.draw()

        self.Settings.update_displayed_fields()

class AttitudeGraphSettingsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        _Attitude_Print("Initializing Attitude Graph Settings Frame")

        super().__init__(master, **kwargs)

        _Attitude_Print("Creating Subframes")
        self.LeftFrame = CTkFrame(self)
        self.RightFrame = CTkFrame(self)

        _Attitude_Print("Placing Subframes")
        self.LeftFrame.place(relx=0, rely=0, relwidth=0.5, relheight=1, anchor="nw")
        self.RightFrame.place(relx=1, rely=0, relwidth=0.5, relheight=1, anchor="ne")

        _Attitude_Print("Creating RPY Checkboxes")
        self.RollCheckbox = CTkCheckBox(self.RightFrame, text="Roll")
        self.PitchCheckbox = CTkCheckBox(self.RightFrame, text="Pitch")
        self.YawCheckbox = CTkCheckBox(self.RightFrame, text="Yaw")

        self.EulerAngleCheckboxes = [self.RollCheckbox, 
                                     self.PitchCheckbox, 
                                     self.YawCheckbox]

        _Attitude_Print("Creating Euler Parameter Checkboxes")
        self.E1Checkbox = CTkCheckBox(self.RightFrame, text="E1")
        self.E2Checkbox = CTkCheckBox(self.RightFrame, text="E2")
        self.E3Checkbox = CTkCheckBox(self.RightFrame, text="E3")
        self.PhiCheckbox = CTkCheckBox(self.RightFrame, text="Phi")

        self.EulerParameterCheckboxes = [self.E1Checkbox,
                                         self.E2Checkbox,
                                         self.E3Checkbox,
                                         self.PhiCheckbox]

        _Attitude_Print("Creating Gibbs-Rodriguez Checkboxes")
        self.P1Checkbox = CTkCheckBox(self.RightFrame, text="P1")
        self.P2Checkbox = CTkCheckBox(self.RightFrame, text="P2")
        self.P3Checkbox = CTkCheckBox(self.RightFrame, text="P3")

        self.GibbsRodriguezCheckboxes = [self.P1Checkbox,
                                         self.P2Checkbox,
                                         self.P3Checkbox]

        _Attitude_Print("Creating Quaternion Checkboxes")
        self.Q0Checkbox = CTkCheckBox(self.RightFrame, text="Q0")
        self.Q1Checkbox = CTkCheckBox(self.RightFrame, text="Q1")
        self.Q2Checkbox = CTkCheckBox(self.RightFrame, text="Q2")
        self.Q3Checkbox = CTkCheckBox(self.RightFrame, text="Q3")
        self.Q4Checkbox = CTkCheckBox(self.RightFrame, text="Q4")

        self.QuaternionCheckboxes = [self.Q0Checkbox,
                                     self.Q1Checkbox,
                                     self.Q2Checkbox,
                                     self.Q3Checkbox,
                                     self.Q4Checkbox]
        
        self.Checkboxes = self.EulerAngleCheckboxes \
                        + self.EulerParameterCheckboxes \
                        + self.GibbsRodriguezCheckboxes \
                        + self.QuaternionCheckboxes
        
        _Attitude_Print("Setting ALL Checkboxes")
        for Checkbox in self.Checkboxes:
            Checkbox.select()

        _Attitude_Print("Creating Display Type Widgets")
        self.DisplayTypeLabel = CTkLabel(self.LeftFrame, text="Display Type:", justify="left")
        self.DisplayTypeSelect = CTkComboBox(self.LeftFrame, 
                                             values=["RPY Angles", 
                                                     "Euler Parameters", 
                                                     "Gibbs-Rodriguez", 
                                                     "Quaternion"],
                                             command=self.display_type_callback)

        _Attitude_Print("Placing Display Type Widgets")        
        self.DisplayTypeLabel.pack(anchor="w")
        self.DisplayTypeSelect.pack(anchor="w")
        self.DisplayTypeSelect.set(api.Attitude_Plot_Get_DisplayType())

        _Attitude_Print("Creating Timespan Widgets")
        self.TimespanLabel = CTkLabel(self.LeftFrame, text="Timespan (s):", justify="left")
        self.TimespanEntry = CTkTextbox(self.LeftFrame, height=12)
        self.TimespanUpdateButton = CTkButton(self.LeftFrame, text="Update", command=self.timespan_button_callback)

        _Attitude_Print("Placing Timespan Widgets")
        self.TimespanLabel.pack(anchor="w")
        self.TimespanEntry.pack(anchor="w")
        self.TimespanUpdateButton.pack(anchor="w")
        self.TimespanEntry.insert("0.0", api.Attitude_Plot_Get_TimeLength())
        
        self.display_type_callback(api.Attitude_Plot_Get_DisplayType())
        
    def display_type_callback(self, selection):
        _Attitude_Print(f"Display Type Callback: {selection}")

        api.Attitude_Plot_Set_DisplayType(selection)
        self.update_displayed_fields()

    def update_displayed_fields(self):
        _Attitude_Print("Updating Displayed Fields")

        if util.AttitudePlot_IsRPYAngles():
            VisibleCheckboxes = self.EulerAngleCheckboxes
        elif util.AttitudePlot_IsEulerParameters():
            VisibleCheckboxes = self.EulerParameterCheckboxes
        elif util.AttitudePlot_IsGibbsRodriguez():
            VisibleCheckboxes = self.GibbsRodriguezCheckboxes
        elif util.AttitudePlot_IsQuaternion():
            VisibleCheckboxes = [Checkbox for Checkbox in self.QuaternionCheckboxes \
                                 if Checkbox is not {"Q0": self.Q4Checkbox, "Q4": self.Q0Checkbox}[api.Settings_Get_QuaternionType()]]
        
        for checkbox in self.Checkboxes:
            checkbox.pack_forget()
            if checkbox in VisibleCheckboxes:
                checkbox.pack()

    def timespan_button_callback(self):
        _Attitude_Print("Timespan Button Callback")

        api.Attitude_Plot_Set_TimeLength(float(self.TimespanEntry.get("0.0", "end")))


