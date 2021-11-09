import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction
import	tkinter.messagebox as MessageBox

class HistoryNotepage(tk.Frame):
    def __init__(self, parent,fileTranslation, camera=None, cancel=None, ok=None,
                 rowconfig=False, colconfig=True, data=None, ):
        ttk.Frame.__init__(self, parent, padding=(10, 10, 10, 10))
        self.grid(sticky='NSEW')
        if colconfig is True:
            self.columnconfigure(0, weight=1)
        if rowconfig is True:
            self.rowconfigure(0, weight=1)
        self.parent = parent
        self.CancelButton = cancel
        self.OkButton = ok
        self.data = data
        self.init = True  # disable SomethingChanged
        self.BuildPage(fileTranslation)
        self.init = False
        self.Changed = False

    def BuildPage(self,fileTranslation):  # MUST Overide this!
        UnderConstruction(self)

    def SomethingChanged(self, val):  # Can override but call super!
        if self.init: return
        self.Changed = True
        if self.CancelButton != None:
            self.CancelButton.config(state='normal')  # '!disabled')
            if self.OkButton != None:
                self.OkButton.config(text='Save')

    def SaveChanges(self):  # MUST override this!
        MessageBox.showwarning("SaveChanges", "SaveChanges not implemented!")