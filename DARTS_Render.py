# DARTS_Attitude.py
# The attitude rendering class for the DARTS Application.

import __main__

from customtkinter import (CTkFrame)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
from scipy.spatial.transform import Rotation as R

def _Render_Print(value:str) -> None:
    if __main__.DEBUG_RENDERING:
        print(f"Render: {value}")

class DARTS_RenderingFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        _Render_Print("Initializing Attitude Rendering Frame")

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

        self.Canvas = FigureCanvasTkAgg(self.Figure, self)

    def plot_axes(self):
        self.plot_vector(self.Axes, [0,0,0], [0,0,0], 1.0, color="r")
        self.plot_vector(self.Axes, [0,0,0], [0,0,90], 1.0, color="g")
        self.plot_vector(self.Axes, [0,0,0], [0,-90,0], 1.0, color="b")
        
    def define_vector(self,
                      apex=None, 
                      origin=[0,0,0], 
                      rotAngles=[0,0,0],
                      length=1.0,
                      tipHeight=None,
                      tipWidth=None,
                      heightRatio = 0.25,
                      widthRatio = 0.0625):
        _Render_Print(f"Defining New Vector")

        r = R.from_euler("xyz", rotAngles, degrees=True)
        
        def f(y, z, height):
            return np.sqrt(y ** 2 + z ** 2) *-1.0*height
        
        if apex is not None:
            if tipHeight is None:
                tipHeight = np.sqrt(apex * 1.0) * heightRatio * apex / abs(apex)
            if tipWidth is None:
                tipWidth = np.sqrt(apex * 1.0) * widthRatio;
            
            u1, v1 = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]
            y1 = np.cos(u1) * np.sin(v1)
            z1 = np.sin(u1) * np.sin(v1)
            x1 = f(y1, z1, tipHeight) + apex

            y1 *= tipWidth
            z1 *= tipWidth

            x1 += origin[0]
            y1 += origin[1]
            z1 += origin[2]

            end = [origin[0] + length, origin[1], origin[2]]

            cone_vals = np.dot(np.dstack((x1, y1, z1)), r.as_matrix().T)
            rod_vals = np.dot(np.array([origin, end]), r.as_matrix().T)

        return cone_vals,rod_vals
    
    def plot_vector(self, axes, origin=[0,0,0], angles=[0,0,0], length=1.0, **kwargs):
        _Render_Print(f"Plotting Vector")

        cone_vals, rod_vals = self.define_vector(1, origin, angles, length)
        axes.plot_surface(cone_vals[:,:,0], cone_vals[:,:,1], cone_vals[:,:,2], zorder=3, **kwargs)
        axes.plot3D(rod_vals[:,0]*.9, rod_vals[:,1]*.9, rod_vals[:,2]*.9, zorder=2, **kwargs)