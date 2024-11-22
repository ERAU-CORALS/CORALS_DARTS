# DARTS_Gains.py
# The gain control tab for the DARTS Application.

import __main__

from customtkinter import (CTkButton, CTkFont, CTkFrame, CTkLabel, CTkTextbox)

import DARTS_API as api
import DARTS_Utilities as util

def _Gains_Print(value: str):
    util.Debug_Print(__file__, value, __main__.Environment["DEBUG_GAINS_PAGE"])

def _Gains_Active() -> bool:
    return __main__.App.MainFrame.MainTabs.get() == "Attitude"
class GainsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.GainMatrixFrame = GainMatrixFrame(self)
        self.ExponentFrame = ExponentFrame(self)

        self.ButtonFont = CTkFont(family="sans-serif", size=20, weight="bold")
        self.ResetButton = CTkButton(self, text="Reset", font=self.ButtonFont, command=self.ResetGains)
        self.ApplyButton = CTkButton(self, text="Apply", font=self.ButtonFont, command=self.ApplyGains)

        self.GainMatrixFrame.place(relx=0, rely=0.0, relwidth=0.7, relheight=0.2, anchor="nw")
        self.ExponentFrame.place(relx=0.7, rely=0.0, relwidth=0.3, relheight=0.2, anchor="nw")
        self.ResetButton.place(relx=0.4, rely=0.25, relwidth=0.2, relheight=0.05, anchor="nw")
        self.ApplyButton.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.05, anchor="nw")

        self.ResetGains()

    def ResetGains(self) -> None:
        _Gains_Print("Resetting Gains")

        self.GainMatrixFrame.Gain11.delete("0.0", "end")
        self.GainMatrixFrame.Gain12.delete("0.0", "end")
        self.GainMatrixFrame.Gain13.delete("0.0", "end")
        self.GainMatrixFrame.Gain21.delete("0.0", "end")
        self.GainMatrixFrame.Gain22.delete("0.0", "end")
        self.GainMatrixFrame.Gain23.delete("0.0", "end")
        self.GainMatrixFrame.Gain31.delete("0.0", "end")
        self.GainMatrixFrame.Gain32.delete("0.0", "end")
        self.GainMatrixFrame.Gain33.delete("0.0", "end")

        matrix = api.Gains_Get_Matrix()

        self.GainMatrixFrame.Gain11.insert("0.0", str(matrix[0][0]))
        self.GainMatrixFrame.Gain12.insert("0.0", str(matrix[0][1]))
        self.GainMatrixFrame.Gain13.insert("0.0", str(matrix[0][2]))
        self.GainMatrixFrame.Gain21.insert("0.0", str(matrix[1][0]))
        self.GainMatrixFrame.Gain22.insert("0.0", str(matrix[1][1]))
        self.GainMatrixFrame.Gain23.insert("0.0", str(matrix[1][2]))
        self.GainMatrixFrame.Gain31.insert("0.0", str(matrix[2][0]))
        self.GainMatrixFrame.Gain32.insert("0.0", str(matrix[2][1]))
        self.GainMatrixFrame.Gain33.insert("0.0", str(matrix[2][2]))

        self.ExponentFrame.ExponentValue.delete("0.0", "end")

        self.ExponentFrame.ExponentValue.insert("0.0", str(api.Gains_Get_Exponent()))

    def ApplyGains(self) -> None:
        _Gains_Print("Applying Gains")

        matrix = [[float(self.GainMatrixFrame.Gain11.get()),
                   float(self.GainMatrixFrame.Gain12.get()),
                   float(self.GainMatrixFrame.Gain13.get())],
                  [float(self.GainMatrixFrame.Gain21.get()),
                   float(self.GainMatrixFrame.Gain22.get()),
                   float(self.GainMatrixFrame.Gain23.get())],
                  [float(self.GainMatrixFrame.Gain31.get()),
                   float(self.GainMatrixFrame.Gain32.get()),
                   float(self.GainMatrixFrame.Gain33.get())]]
        
        api.Gains_Set_Matrix(matrix)

        api.Gains_Set_Exponent(int(self.ExponentFrame.ExponentValue.get()))

class GainMatrixFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.Gain11 = CTkTextbox(self)
        self.Gain12 = CTkTextbox(self)
        self.Gain13 = CTkTextbox(self)
        self.Gain21 = CTkTextbox(self)
        self.Gain22 = CTkTextbox(self)
        self.Gain23 = CTkTextbox(self)
        self.Gain31 = CTkTextbox(self)
        self.Gain32 = CTkTextbox(self)
        self.Gain33 = CTkTextbox(self)

        self.Gain11.place(relx=0.025, rely=0.025, relwidth=0.3, relheight=0.3)
        self.Gain12.place(relx=0.350, rely=0.025, relwidth=0.3, relheight=0.3)
        self.Gain13.place(relx=0.675, rely=0.025, relwidth=0.3, relheight=0.3)
        self.Gain21.place(relx=0.025, rely=0.350, relwidth=0.3, relheight=0.3)
        self.Gain22.place(relx=0.350, rely=0.350, relwidth=0.3, relheight=0.3)
        self.Gain23.place(relx=0.675, rely=0.350, relwidth=0.3, relheight=0.3)
        self.Gain31.place(relx=0.025, rely=0.675, relwidth=0.3, relheight=0.3)
        self.Gain32.place(relx=0.350, rely=0.675, relwidth=0.3, relheight=0.3)
        self.Gain33.place(relx=0.675, rely=0.675, relwidth=0.3, relheight=0.3)

class ExponentFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.ExponentText = CTkLabel(self, text=" * 10 ^ ")
        self.ExponentText.grid(row=0, column=0)

        self.ExponentValue = CTkTextbox(self, height=12)
        self.ExponentValue.grid(row=0, column=1)