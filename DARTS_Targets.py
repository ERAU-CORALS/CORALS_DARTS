# DARTS_Targets.py
# The target control tab for the DARTS Application.

import __main__

from customtkinter import (CTkFrame, CTkLabel, CTkTextbox, CTkButton)

import matplotlib
matplotlib.use("TkAgg")

import numpy as np

import DARTS_API as api
import DARTS_Utilities as util
from DARTS_Render import DARTS_RenderingFrame

def _Targets_Print(value:str) -> None:
    if __main__.DEBUG_TARGETS_PAGE:
        print(f"Targets: {value}")

class TargetsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        _Targets_Print("Creating Targets Frame")

        super().__init__(master, **kwargs)

        __main__.DARTS_Settings.register("Targets_CurrentDisplayIndex", 0)
        __main__.DARTS_Settings.register("Targets_List", [])

        self.TargetRenderingSettingsFrame = RenderingSettingsFrame(self)
        self.TargetRenderingFrame = TargetRenderingFrame(self, self.TargetRenderingSettingsFrame)
        self.TargetEntryFrame = TargetEntryFrame(self)
        self.TargetListFrame = TargetListFrame(self, self.TargetEntryFrame)

        self.TargetRenderingFrame.place(relx=0, rely=0, relwidth=0.5, relheight=0.75, anchor="nw")
        self.TargetRenderingSettingsFrame.place(relx=0, rely=1, relwidth=0.5, relheight=0.25, anchor="sw")
        self.TargetEntryFrame.place(relx=1, rely=0, relwidth=0.5, relheight=0.25, anchor="ne")
        self.TargetListFrame.place(relx=1, rely=1, relwidth=0.5, relheight=0.75, anchor="se")

class TargetRenderingFrame(DARTS_RenderingFrame):
    def __init__(self, master, settings, **kwargs):
        _Targets_Print("Creating Target Rendering Frame")

        super().__init__(master, **kwargs)

        self.Settings = settings

        self.Canvas.draw()
        self.Canvas.get_tk_widget().place(x=0, y=0, relwidth=1, relheight=1, anchor="nw")

        self.update_rendered_targets_process()

    def update_rendered_targets_process(self):
        _Targets_Print("Updating Rendered Targets Process")

        self.Axes.clear()
        
        self.Axes.set_xlim(-1, 1)
        self.Axes.set_ylim(-1, 1)
        self.Axes.set_zlim(-1, 1)

        self.Axes.set_xticks([-1, 1])
        self.Axes.set_yticks([-1, 1])
        self.Axes.set_zticks([-1, 1])

        self.plot_axes()
        self.plot_vector(self.Axes, [0,0,0], [0,45,135], 1.0, color="r")

        try:
            if type(api.Targets_Get_CurrentDisplayIndex()) is int:
                angles = np.rad2deg(util.Convert_Quaternion_to_RPY(api.Targets_Get_List()[api.Targets_Get_CurrentDisplayIndex()]))
                print (f"Vector Angles: {angles}")
                if api.Targets_Get_CurrentDisplayIndex() is 0:
                    self.plot_vector(self.Axes, [0,0,0], angles, 1.0, color="c")
                else:
                    self.plot_vector(self.Axes, [0,0,0], angles, 1.0, color="o")
            
            elif type(api.Targets_Get_CurrentDisplayIndex()) is list[int]:
                for ListIndex, TargetIndex in enumerate(api.Targets_Get_CurrentDisplayIndex()):
                    angles = np.rad2deg(util.Convert_Quaternion_to_RPY(api.Targets_Get_List()[TargetIndex]))
                    if TargetIndex is 0:
                        self.plot_vector(self.Axes, [0,0,0], angles, 1.0, color="c")
                    elif ListIndex is 0:
                        self.plot_vector(self.Axes, [0,0,0], angles, 1.0, color="o")
                    else:
                        self.plot_vector(self.Axes, [0,0,0], angles, 1.0, color="k")

        except:
            _Targets_Print("Target Display Index Out of Range")
        
        finally:
            self.Canvas.draw()

        self.after(1000, self.update_rendered_targets_process)

class TargetEntryFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        _Targets_Print("Creating Target Entry Frame")

        super().__init__(master, **kwargs)

        self.TargetEntryLabel = CTkLabel(self, text="Target Entry:")
        self.TargetEntryField = CTkFrame(self)

        self.TargetEntryField1Label = CTkLabel(self.TargetEntryField, text="Q0:")
        self.TargetEntryField2Label = CTkLabel(self.TargetEntryField, text="Q1:")
        self.TargetEntryField3Label = CTkLabel(self.TargetEntryField, text="Q2:")
        self.TargetEntryField4Label = CTkLabel(self.TargetEntryField, text="Q3:")

        self.TargetEntryQ0Box = CTkTextbox(self.TargetEntryField, height=12)
        self.TargetEntryQ1Box = CTkTextbox(self.TargetEntryField, height=12)
        self.TargetEntryQ2Box = CTkTextbox(self.TargetEntryField, height=12)
        self.TargetEntryQ3Box = CTkTextbox(self.TargetEntryField, height=12)

        self.TargetEntryField1Label.place(relx=0, rely=0, relwidth=0.25, relheight=0.5, anchor="nw")
        self.TargetEntryField2Label.place(relx=0.25, rely=0, relwidth=0.25, relheight=0.5, anchor="nw")
        self.TargetEntryField3Label.place(relx=0.5, rely=0, relwidth=0.25, relheight=0.5, anchor="nw")
        self.TargetEntryField4Label.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.5, anchor="nw")

        self.TargetEntryQ0Box.place(relx=0, rely=1, relwidth=0.25, relheight=0.5, anchor="sw")
        self.TargetEntryQ1Box.place(relx=0.25, rely=1, relwidth=0.25, relheight=0.5, anchor="sw")
        self.TargetEntryQ2Box.place(relx=0.5, rely=1, relwidth=0.25, relheight=0.5, anchor="sw")
        self.TargetEntryQ3Box.place(relx=0.75, rely=1, relwidth=0.25, relheight=0.5, anchor="sw")

        self.TargetAddFrontButton = CTkButton(self, text="Add Front", command=self.add_front_callback)
        self.TargetAddBackButton = CTkButton(self, text="Add Back", command=self.add_back_callback)

        self.TargetEntryLabel.place(relx=0, rely=0.1, relwidth=1, relheight=0.1, anchor="sw")
        self.TargetEntryField.place(relx=0, rely=0.1, relwidth=1, relheight=0.4, anchor="nw")
        self.TargetAddFrontButton.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.25, anchor="nw")
        self.TargetAddBackButton.place(relx=1, rely=0.5, relwidth=0.5, relheight=0.25, anchor="ne")

    def add_front_callback(self):
        _Targets_Print("Adding Target to Front")

        q0 = float(self.TargetEntryQ0Box.get("0.0", "end").strip('\n'))
        q1 = float(self.TargetEntryQ1Box.get("0.0", "end").strip('\n'))
        q2 = float(self.TargetEntryQ2Box.get("0.0", "end").strip('\n'))
        q3 = float(self.TargetEntryQ3Box.get("0.0", "end").strip('\n'))

        qmag = np.sqrt(q0**2 + q1**2 + q2**2 + q3**2)

        api.Targets_Set_List([[q0, q1, q2, q3] / qmag] + api.Targets_Get_List())

        self.TargetEntryQ0Box.delete("0.0", "end")
        self.TargetEntryQ1Box.delete("0.0", "end")
        self.TargetEntryQ2Box.delete("0.0", "end")
        self.TargetEntryQ3Box.delete("0.0", "end")
    
    def add_back_callback(self):
        _Targets_Print("Adding Target to Back")

        q0 = float(self.TargetEntryQ0Box.get("0.0", "end").strip('\n'))
        q1 = float(self.TargetEntryQ1Box.get("0.0", "end").strip('\n'))
        q2 = float(self.TargetEntryQ2Box.get("0.0", "end").strip('\n'))
        q3 = float(self.TargetEntryQ3Box.get("0.0", "end").strip('\n'))

        qmag = np.sqrt(q0**2 + q1**2 + q2**2 + q3**2)
        
        api.Targets_Set_List(api.Targets_Get_List() + [[q0, q1, q2, q3] / qmag])

        self.TargetEntryQ0Box.delete("0.0", "end")
        self.TargetEntryQ1Box.delete("0.0", "end")
        self.TargetEntryQ2Box.delete("0.0", "end")
        self.TargetEntryQ3Box.delete("0.0", "end")

class TargetListFrame(CTkFrame):
    class TargetListEntry(CTkFrame):
        def __init__(self, master, index, **kwargs):
            _Targets_Print("Creating Target List Entry")

            super().__init__(master, **kwargs)

            self.TargetIndex = index

            self.TargetLabel = CTkLabel(self, text=util.Get_TargetList_Quaternion_String(index), anchor="w")
            self.TargetReplaceButton = CTkButton(self, text="Overwrite", command=self.replace_target_callback)
            self.TargetDeleteButton = CTkButton(self, text="Delete", command=self.delete_target_callback)

            self.TargetLabel.place(relx=0, rely=0, relwidth=0.5, relheight=1, anchor="nw")
            self.TargetReplaceButton.place(relx=0.5, rely=0, relwidth=0.25, relheight=1, anchor="nw")
            self.TargetDeleteButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=1, anchor="nw")

            # self.update_target()

        def replace_target_callback(self):
            _Targets_Print("Replacing Target")

            q0 = float(self.master.TargetEntry.TargetEntryQ0Box.get("0.0", "end").strip('\n'))
            q1 = float(self.master.TargetEntry.TargetEntryQ1Box.get("0.0", "end").strip('\n'))
            q2 = float(self.master.TargetEntry.TargetEntryQ2Box.get("0.0", "end").strip('\n'))
            q3 = float(self.master.TargetEntry.TargetEntryQ3Box.get("0.0", "end").strip('\n'))

            qmag = np.sqrt(q0**2 + q1**2 + q2**2 + q3**2)

            api.Targets_Get_List()[self.TargetIndex] = [q0, q1, q2, q3] / qmag

            self.master.TargetEntry.TargetEntryQ0Box.delete("0.0", "end")
            self.master.TargetEntry.TargetEntryQ1Box.delete("0.0", "end")
            self.master.TargetEntry.TargetEntryQ2Box.delete("0.0", "end")
            self.master.TargetEntry.TargetEntryQ3Box.delete("0.0", "end")

        def delete_target_callback(self):
            _Targets_Print("Deleting Target")
            api.Targets_Get_List().pop(self.TargetIndex)

    def __init__(self, master, entry, **kwargs):
        _Targets_Print("Creating Target List Frame")

        super().__init__(master, **kwargs)

        self.TargetEntry = entry

        self.TargetListLabel = CTkLabel(self, text="Target List:")
        self.TargetListLabel.pack(anchor='w')

        self.TargetListFrames = []

        self.update_target_list_process()

    def update_target_list_process(self):
        _Targets_Print("Updating Target List Process")

        if len(api.Targets_Get_List()) >= len(self.TargetListFrames):
            for index in range(len(api.Targets_Get_List())):
                if index >= len(self.TargetListFrames):
                    self.TargetListFrames.append(self.TargetListEntry(self, index))
                    self.TargetListFrames[index].place(relx=0, rely=(index+1)/16, relwidth=1, relheight=1/16, anchor="nw")
                else:
                    self.TargetListFrames[index].TargetLabel.configure(text=util.Get_TargetList_Quaternion_String(index))
        elif len(api.Targets_Get_List()) < len(self.TargetListFrames):
            for index in range(len(api.Targets_Get_List()), len(self.TargetListFrames)):
                self.TargetListFrames.pop(index).destroy()

        self.after(200, self.update_target_list_process)

class RenderingSettingsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        _Targets_Print("Creating Rendering Settings Frame")

        super().__init__(master, **kwargs)

        self.TargetIndexLabel = CTkLabel(self, text="Displayed Target Index (or Array):")
        self.TargetIndexEntry = CTkTextbox(self, height=12)
        self.TargetIndexUpdateButton = CTkButton(self, text="Update", command=self.update_target_index_callback)

        self.TargetIndexLabel.pack(anchor='w')
        self.TargetIndexEntry.pack(anchor='w')
        self.TargetIndexUpdateButton.pack(anchor='w')
        self.TargetIndexEntry.insert("0.0", api.Targets_Get_CurrentDisplayIndex())

    def update_target_index_callback(self):
        _Targets_Print("Updating Target Index")

        entry = self.TargetIndexEntry.get("0.0", "end").strip('\n')
        
        if entry[0] == '[' and entry[-1] == ']':
            entries = entry[1:-1].split(',')
            index = [int(e) for e in entry[1:-1].strip(' ').split(',')]
        else:
            index = int(entry)

        api.Targets_Set_CurrentDisplayIndex(index)
        self.TargetIndexEntry.insert("0.0", f"{api.Targets_Get_CurrentDisplayIndex()}")

