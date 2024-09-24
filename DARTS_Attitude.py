# DARTS_Attitude.py
# The attitude reporting tab for the DARTS Application.

import __main__

from customtkinter import (CTk, CTkCheckBox, CTkComboBox, CTkFrame, CTkLabel, CTkTextbox, CTkButton)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import tight_layout

import time
import numpy as np
from scipy.spatial.transform import Rotation as R

import DARTS_API as api
import DARTS_Utilities as util

class AttitudeFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        __main__.DARTS_Settings.register("Attitude_Current", [1, 0, 0, 0])

        __main__.DARTS_Settings.register("Attitude_Plot_StartTime", time.time())
        __main__.DARTS_Settings.register("Attitude_Plot_TimeLength", 10)
        __main__.DARTS_Settings.register("Attitude_Plot_TimeData", [])
        __main__.DARTS_Settings.register("Attitude_Plot_QuaternionData")
        __main__.DARTS_Settings.register("Attitude_Plot_DisplayType", "Quaternion", ["RPY Angles", "Euler Parameters", "Gibbs-Rodriguez", "Quaternion"])

        self.AttitudeRenderingFrame = AttitudeRenderingFrame(self)
        self.GraphSettingsFrame = AttitudeGraphSettingsFrame(self)
        self.TimeGraphFrame = AttitudeTimeGraphFrame(self, self.GraphSettingsFrame)

        self.AttitudeRenderingFrame.grid(row=0, column=0, sticky="nsew")
        self.TimeGraphFrame.grid(row=0, column=1, sticky="nsew")
        self.GraphSettingsFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")

class AttitudeRenderingFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.Figure = Figure(figsize=(5, 5), dpi=100)
        self.Axes   = self.Figure.add_subplot(111, projection="3d")
        self.Axes.set_xlim(-1, 1)
        self.Axes.set_ylim(-1, 1)
        self.Axes.set_zlim(-1, 1)
        self.Axes.set_xticks([-1, 1])
        self.Axes.set_yticks([-1, 1])
        self.Axes.set_zticks([-1, 1])
        self.Axes.view_init(elev=30, azim=30)
        self.Axes.set_aspect("equal")
        
        # self.Vectors = np.array([[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])
        # self.VectorsX, self.VectorsY, self.VectorsZ, self.VectorsU, self.VectorsV, self.VectorsW = zip(*self.Vectors)

        # self.Axes.quiver(self.VectorsX, self.VectorsY, self.VectorsZ, self.VectorsU, self.VectorsV, self.VectorsW, color=["r", "g", "b"])

        
        def define_vector(apex=None, 
                        start=[0,0,0], 
                        rotAngles=[0,45,0], 
                        length=1.0, 
                        tipHeight=None,
                        tipWidth=None,
                        heightRatio = 0.2,
                        widthRatio = 0.05):
            r = R.from_euler("xyz", rotAngles, degrees=True)
            
            def f(x, y, height):
                return np.sqrt(x ** 2 + y ** 2) *-1.0*height
            
            if apex is not None:
                if tipHeight is None:
                    tipHeight = np.sqrt(apex * 1.0) * heightRatio * apex / abs(apex)
                if tipWidth is None:
                    tipWidth = np.sqrt(apex * 1.0) * widthRatio;

                u1, v1 = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]
                x1 = np.cos(u1) * np.sin(v1)
                y1 = np.sin(u1) * np.sin(v1)
                z1 = f(x1, y1, tipHeight) + apex

                x1 *= tipWidth
                y1 *= tipWidth

                vals = np.dot(np.dstack((x1, y1, z1)), r.as_matrix().T)
                vals2 = np.dot(np.array([[0,0,0], [0,0,1]]), r.as_matrix().T)

            return vals,vals2
        
        def plot_vector(axes, origin=[0,0,0], angles=[0,0,0], length=1.0, **kwargs):
            covals, rovals = define_vector(1, origin, angles, length)
            axes.plot_surface(covals[:,:,0], covals[:,:,1], covals[:,:,2], zorder=3, **kwargs)
            axes.plot3D(rovals[:,0]*.9, rovals[:,1]*.9, rovals[:,2]*.9, zorder=2, **kwargs)

        plot_vector(self.Axes, [0,0,0], [0,90,0], 1.0, color="r")
        plot_vector(self.Axes, [0,0,0], [-90,0,0], 1.0, color="g")
        plot_vector(self.Axes, [0,0,0], [0,0,0], 1.0, color="b")
        
        # self.Axes.legend(["Roll",,"Pitch", "Yaw"])

        self.Canvas = FigureCanvasTkAgg(self.Figure, self)
        self.Canvas.draw()
        self.Canvas.get_tk_widget().pack()

class AttitudeTimeGraphFrame(CTkFrame):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)

        self.Settings = settings

        self.Figure = Figure(figsize=(5, 5), dpi=100)
        self.Axes   = self.Figure.add_subplot(111)
        self.AltAxes = self.Axes.twinx()
        # tight_layout()
        
        self.start_time = time.time()

        self.Canvas = FigureCanvasTkAgg(self.Figure, self)
        self.Canvas.draw()
        self.Canvas.get_tk_widget().pack()

        self.draw_data_callback()

    def draw_data_callback(self):   
        self.Axes.clear()
        self.AltAxes.clear()

        time_data = api.Attitude_Plot_Get_TimeData()

        print ("Draw Data Callback")

        if len(time_data) >= 2:

            self.Axes.set_xlim(time_data[0], time_data[-1])
            self.AltAxes.set_xlim(time_data[0], time_data[-1])
            
            if util.AttitudePlot_IsRPYAngles():

                [roll_data, pitch_data, yaw_data] = util.Convert_Quaternion_to_RPY(api.Attitude_Plot_Get_QuaternionData())
                legend_entries = []
                
                if self.Settings.RollCheckbox.get():
                    if util.AngleType_IsDegrees():
                        roll_data = np.degrees(roll_data)
                    self.Axes.plot(time_data, roll_data.tolist(), color="red")
                    legend_entries.append("Roll")
                
                if self.Settings.PitchCheckbox.get():
                    if util.AngleType_IsDegrees():
                        pitch_data = np.degrees(pitch_data)
                    self.Axes.plot(time_data, pitch_data.tolist(), color="green")
                    legend_entries.append("Pitch")
                
                if self.Settings.YawCheckbox.get():
                    if util.AngleType_IsDegrees():
                        yaw_data = np.degrees(yaw_data)
                    self.Axes.plot(time_data, yaw_data.tolist(), color="blue")
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

                euler_data = util.Convert_Quaternion_to_Euler(api.Attitude_Plot_Get_QuaternionData())
                [e1_data, e2_data, e3_data] = euler_data["parameter"]
                phi_data = euler_data["angle"]
                legend_entries = []

                if self.Settings.E1Checkbox.get():
                    self.Axes.plot(time_data, e1_data.tolist(), color="red")
                    legend_entries.append("E1")
                
                if self.Settings.E2Checkbox.get():
                    self.Axes.plot(time_data, e2_data.tolist(), color="green")
                    legend_entries.append("E2")
                
                if self.Settings.E3Checkbox.get():
                    self.Axes.plot(time_data, e3_data.tolist(), color="blue")
                    legend_entries.append("E3")

                self.Axes.legend(legend_entries, loc='upper left')
                self.Axes.set_ylim(-1, 1)
                self.Axes.set_yticks([-1, -0.5, 0, 0.5, 1])
                self.Axes.set_ylabel("Euler Parameter")
                
                if self.Settings.PhiCheckbox.get():
                    if util.AngleType_IsDegrees():
                        phi_data = np.degrees(phi_data)
                    self.AltAxes.plot(time_data, phi_data.tolist(), color="cyan")
                
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

                [p1_data, p2_data, p3_data] = util.Convert_Quaternion_to_Gibbs(api.Attitude_Plot_Get_QuaternionData())
                legend_entries = []

                if self.Settings.P1Checkbox.get():
                    self.Axes.plot(time_data, p1_data.tolist(), color="red")
                    legend_entries.append("P1")
                
                if self.Settings.P2Checkbox.get():
                    self.Axes.plot(time_data, p2_data.tolist(), color="green")
                    legend_entries.append("P2")
                
                if self.Settings.P3Checkbox.get():
                    self.Axes.plot(time_data, p3_data.tolist(), color="blue")
                    legend_entries.append("P3")
                
                self.Axes.legend(legend_entries, loc='upper left')
                self.Axes.set_ylabel("GR Parameter")
                
                self.AltAxes.set_ylabel("")
                self.AltAxes.set_yticks([])
                self.AltAxes.set_ylabel("")
                
            elif util.AttitudePlot_IsQuaternion():

                [q0_data, q1_data, q2_data, q3_data] = api.Attitude_Plot_Get_QuaternionData()
                legend_entries = []

                if self.Settings.Q0Checkbox.get() and api.Settings_Get_QuaternionType() == "Q0":
                    self.Axes.plot(time_data, q0_data.tolist(), color="cyan")
                    legend_entries.append("Q0")
                
                if self.Settings.Q1Checkbox.get():
                    self.Axes.plot(time_data, q1_data.tolist(), color="red")
                    legend_entries.append("Q1")
                
                if self.Settings.Q2Checkbox.get():
                    self.Axes.plot(time_data, q2_data.tolist(), color="green")
                    legend_entries.append("Q2")
                
                if self.Settings.Q3Checkbox.get():
                    self.Axes.plot(time_data, q3_data.tolist(), color="blue")
                    legend_entries.append("Q3")

                if self.Settings.Q4Checkbox.get() and api.Settings_Get_QuaternionType() == "Q4":
                    self.Axes.plot(time_data, q0_data.tolist(), color="cyan")
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

        self.after(1000, self.draw_data_callback)

class AttitudeGraphSettingsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.LeftFrame = CTkFrame(self)
        self.RightFrame = CTkFrame(self)

        self.LeftFrame.grid(row=0, column=0, sticky="nsew")
        self.RightFrame.grid(row=0, column=1, sticky="nsew")

        self.RollCheckbox = CTkCheckBox(self.RightFrame, text="Roll")
        self.PitchCheckbox = CTkCheckBox(self.RightFrame, text="Pitch")
        self.YawCheckbox = CTkCheckBox(self.RightFrame, text="Yaw")

        self.EulerAngleCheckboxes = [self.RollCheckbox, 
                                     self.PitchCheckbox, 
                                     self.YawCheckbox]

        self.E1Checkbox = CTkCheckBox(self.RightFrame, text="E1")
        self.E2Checkbox = CTkCheckBox(self.RightFrame, text="E2")
        self.E3Checkbox = CTkCheckBox(self.RightFrame, text="E3")
        self.PhiCheckbox = CTkCheckBox(self.RightFrame, text="Phi")

        self.EulerParameterCheckboxes = [self.E1Checkbox,
                                         self.E2Checkbox,
                                         self.E3Checkbox,
                                         self.PhiCheckbox]

        self.P1Checkbox = CTkCheckBox(self.RightFrame, text="P1")
        self.P2Checkbox = CTkCheckBox(self.RightFrame, text="P2")
        self.P3Checkbox = CTkCheckBox(self.RightFrame, text="P3")

        self.GibbsRodriguezCheckboxes = [self.P1Checkbox,
                                         self.P2Checkbox,
                                         self.P3Checkbox]

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
        
        for Checkbox in self.Checkboxes:
            Checkbox.select()

        self.DisplayTypeLabel = CTkLabel(self.LeftFrame, text="Display Type:", justify="left")
        self.DisplayTypeSelect = CTkComboBox(self.LeftFrame, 
                                             values=["RPY Angles", 
                                                     "Euler Parameters", 
                                                     "Gibbs-Rodriguez", 
                                                     "Quaternion"],
                                             command=self.display_type_callback)
        
        self.DisplayTypeLabel.pack()
        self.DisplayTypeSelect.pack()
        self.DisplayTypeSelect.set(api.Attitude_Plot_Get_DisplayType())

        self.TimespanLabel = CTkLabel(self.LeftFrame, text="Timespan (s):", justify="left")
        self.TimespanEntry = CTkTextbox(self.LeftFrame)
        self.TimespanUpdateButton = CTkButton(self.LeftFrame, text="Update", command=self.timespan_button_callback)

        self.TimespanLabel.pack()
        self.TimespanEntry.pack()
        self.TimespanUpdateButton.pack()
        self.TimespanEntry.insert("0.0", api.Attitude_Plot_Get_TimeLength())
        
        self.display_type_callback(api.Attitude_Plot_Get_DisplayType())
        
    def display_type_callback(self, selection):
        api.Attitude_Plot_Set_DisplayType(selection)
        self.update_displayed_fields()

    def update_displayed_fields(self):
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
        api.Attitude_Plot_Set_TimeLength(float(self.TimespanEntry.get("0.0", "end")))


