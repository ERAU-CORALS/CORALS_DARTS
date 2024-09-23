# DARTS_Attitude.py
# The attitude reporting tab for the DARTS Application.

import __main__

from customtkinter import (CTk, CTkCheckBox, CTkComboBox, CTkFrame)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import tight_layout

import time
import numpy as np
from scipy.spatial.transform import Rotation as R

class AttitudeFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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
        print ("Drawing Data")     
        self.Axes.clear()
        self.AltAxes.clear()
        time_data = __main__.DARTS_Settings["AttitudeDisplayTime"]

        if len(time_data) >= 2:

            self.Axes.set_xlim(time_data[0], time_data[-1])
            self.AltAxes.set_xlim(time_data[0], time_data[-1])

            q0_data = __main__.DARTS_Settings["AttitudeDisplayData"][0]
            q1_data = __main__.DARTS_Settings["AttitudeDisplayData"][1]
            q2_data = __main__.DARTS_Settings["AttitudeDisplayData"][2]
            q3_data = __main__.DARTS_Settings["AttitudeDisplayData"][3]

            if self.Settings.DisplayTypeSelect.get() != "Quaternion":
                phi_data = 2*np.arccos(q0_data)

                qhat_mag = np.sqrt(q1_data**2 + q2_data**2 + q3_data**2)
                e1_data = q1_data / qhat_mag
                e2_data = q2_data / qhat_mag
                e3_data = q3_data / qhat_mag
            
            if self.Settings.DisplayTypeSelect.get() == "RPY Angles":
                
                if self.Settings.RollCheckbox.get():
                    roll_data = np.arctan2(2*(q0_data*q1_data + q2_data*q3_data), 1 - 2*(q1_data**2 + q2_data**2))
                    if __main__.DARTS_Settings["AngleType"] == "Degrees":
                        roll_data = np.degrees(roll_data)
                    self.Axes.plot(time_data, roll_data.tolist(), color="red")
                
                if self.Settings.PitchCheckbox.get():
                    pitch_data = np.arcsin(2*(q0_data*q2_data - q3_data*q1_data))
                    if __main__.DARTS_Settings["AngleType"] == "Degrees":
                        pitch_data = np.degrees(pitch_data)
                    self.Axes.plot(time_data, pitch_data.tolist(), color="green")
                
                if self.Settings.YawCheckbox.get():
                    yaw_data = np.arctan2(2*(q0_data*q3_data + q1_data*q2_data), 1 - 2*(q2_data**2 + q3_data**2))
                    if __main__.DARTS_Settings["AngleType"] == "Degrees":
                        yaw_data = np.degrees(yaw_data)
                    self.Axes.plot(time_data, yaw_data.tolist(), color="blue")

                self.Axes.legend(["Roll", "Pitch", "Yaw"], loc='upper left')
                if __main__.DARTS_Settings["AngleType"] == "Degrees":
                    self.Axes.set_ylim(-180, 180) 
                    self.Axes.set_yticks([-180, -90, 0, 90, 180])
                else:
                    self.Axes.set_ylim(-np.pi, np.pi) 
                    self.Axes.set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
                self.Axes.set_ylabel("Angle (deg)")
                
                self.AltAxes.set_ylabel("")
                self.AltAxes.set_yticks([])
                self.AltAxes.set_ylabel("")
                
                
            elif self.Settings.DisplayTypeSelect.get() == "Euler Parameters":

                if self.Settings.E1Checkbox.get():
                    self.Axes.plot(time_data, e1_data.tolist(), color="red")
                
                if self.Settings.E2Checkbox.get():
                    self.Axes.plot(time_data, e2_data.tolist(), color="green")
                
                if self.Settings.E3Checkbox.get():
                    self.Axes.plot(time_data, e3_data.tolist(), color="blue")
                
                if self.Settings.PhiCheckbox.get():
                    if __main__.DARTS_Settings["AngleType"] == "Degrees":
                        phi_data = np.degrees(phi_data)
                    self.AltAxes.plot(time_data, phi_data.tolist(), color="cyan")

                self.Axes.legend(["E1", "E2", "E3"], loc='upper left')
                self.Axes.set_ylim(-1, 1)
                self.Axes.set_yticks([-1, -0.5, 0, 0.5, 1])
                self.Axes.set_ylabel("Euler Parameter")
                
                self.AltAxes.legend(["Phi"], loc='upper right')
                if __main__.DARTS_Settings["AngleType"] == "Degrees":
                    self.AltAxes.set_ylim(0, 360)
                    self.AltAxes.set_yticks([0, 90, 180, 270, 360])
                else:
                    self.AltAxes.set_ylim(0, 2*np.pi)
                    self.AltAxes.set_yticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
                self.AltAxes.set_ylabel("Euler Angle", color='cyan')
                self.AltAxes.get_yaxis().set_label_position("right")
                
            elif self.Settings.DisplayTypeSelect.get() == "Gibbs-Rodriguez":

                if self.Settings.P1Checkbox.get():
                    p1_data = e1_data*np.tan(phi_data/2)
                    self.Axes.plot(time_data, p1_data.tolist(), color="red")
                
                if self.Settings.P2Checkbox.get():
                    p2_data = e2_data*np.tan(phi_data/2)
                    self.Axes.plot(time_data, p2_data.tolist(), color="green")
                
                if self.Settings.P3Checkbox.get():
                    p3_data = e3_data*np.tan(phi_data/2)
                    self.Axes.plot(time_data, p3_data.tolist(), color="blue")
                
                self.Axes.legend(["P1", "P2", "P3"], loc='upper left')
                self.Axes.set_ylabel("GR Parameter")
                
                self.AltAxes.set_ylabel("")
                self.AltAxes.set_yticks([])
                self.AltAxes.set_ylabel("")
                
            elif self.Settings.DisplayTypeSelect.get() == "Quaternion":

                if self.Settings.Q0Checkbox.get():
                    self.Axes.plot(time_data, q0_data.tolist(), color="red")
                
                if self.Settings.Q1Checkbox.get():
                    self.Axes.plot(time_data, q1_data.tolist(), color="green")
                
                if self.Settings.Q2Checkbox.get():
                    self.Axes.plot(time_data, q2_data.tolist(), color="blue")
                
                if self.Settings.Q3Checkbox.get():
                    self.Axes.plot(time_data, q3_data.tolist(), color="black")

                self.Axes.legend(["Q0", "Q1", "Q2", "Q3"], loc='upper left')
                self.Axes.set_ylim(-1, 1)
                self.Axes.set_yticks([-1, -0.5, 0, 0.5, 1])
                self.Axes.set_ylabel("Quaternion")
                
                self.AltAxes.set_ylabel("")
                self.AltAxes.set_yticks([])
                self.AltAxes.set_ylabel("")

            self.Canvas.draw()

        self.after(1000, self.draw_data_callback)

class AttitudeGraphSettingsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.RollCheckbox = CTkCheckBox(self, text="Roll")
        self.PitchCheckbox = CTkCheckBox(self, text="Pitch")
        self.YawCheckbox = CTkCheckBox(self, text="Yaw")

        self.EulerAngleCheckboxes = [self.RollCheckbox, 
                                     self.PitchCheckbox, 
                                     self.YawCheckbox]

        self.E1Checkbox = CTkCheckBox(self, text="E1")
        self.E2Checkbox = CTkCheckBox(self, text="E2")
        self.E3Checkbox = CTkCheckBox(self, text="E3")
        self.PhiCheckbox = CTkCheckBox(self, text="Phi")

        self.EulerParameterCheckboxes = [self.E1Checkbox,
                                         self.E2Checkbox,
                                         self.E3Checkbox,
                                         self.PhiCheckbox]

        self.P1Checkbox = CTkCheckBox(self, text="P1")
        self.P2Checkbox = CTkCheckBox(self, text="P2")
        self.P3Checkbox = CTkCheckBox(self, text="P3")

        self.GibbsRodriguezCheckboxes = [self.P1Checkbox,
                                         self.P2Checkbox,
                                         self.P3Checkbox]

        self.Q0Checkbox = CTkCheckBox(self, text="Q0")
        self.Q1Checkbox = CTkCheckBox(self, text="Q1")
        self.Q2Checkbox = CTkCheckBox(self, text="Q2")
        self.Q3Checkbox = CTkCheckBox(self, text="Q3")

        self.QuaternionCheckboxes = [self.Q0Checkbox,
                                     self.Q1Checkbox,
                                     self.Q2Checkbox,
                                     self.Q3Checkbox]
        
        self.Checkboxes = self.EulerAngleCheckboxes \
                        + self.EulerParameterCheckboxes \
                        + self.GibbsRodriguezCheckboxes \
                        + self.QuaternionCheckboxes
        
        for Checkbox in self.Checkboxes:
            Checkbox.select()

        self.DisplayTypeSelect = CTkComboBox(self, 
                                             values=["RPY Angles", 
                                                     "Euler Parameters", 
                                                     "Gibbs-Rodriguez", 
                                                     "Quaternion"],
                                             command=self.display_type_callback)
        
        self.DisplayTypeSelect.pack()
        self.DisplayTypeSelect.set(__main__.DARTS_Settings["AttitudeDisplayType"])
        
        self.display_type_callback(__main__.DARTS_Settings["AttitudeDisplayType"])
        
    def display_type_callback(self, selection):
        __main__.DARTS_Settings["AttitudeDisplayType"] = selection

        if selection == "RPY Angles":
            VisibleCheckboxes = self.EulerAngleCheckboxes
        elif selection == "Euler Parameters":
            VisibleCheckboxes = self.EulerParameterCheckboxes
        elif selection == "Gibbs-Rodriguez":
            VisibleCheckboxes = self.GibbsRodriguezCheckboxes
        elif selection == "Quaternion":
            VisibleCheckboxes = self.QuaternionCheckboxes
        else:
            raise ValueError("Invalid selection: " + selection)
        
        for checkbox in self.Checkboxes:
            if checkbox in VisibleCheckboxes:
                checkbox.pack()
            else:
                checkbox.pack_forget()


