import tkinter as tk
from tkinter import ttk

def UnderConstruction(window):
    tk.Label(window, text='UNDER CONSTRUCTION', font=('Arial', 14, ('bold')),
             anchor='center').grid(row=0, column=0, sticky='EW')

def myLabelFrame(f, row, col, txt,stick='NEWS', py=5, span=1, pad=(5, 5, 5, 5)):
    l = ttk.LabelFrame(f, text=txt, padding=pad)
    l.grid(row=row, column=col, sticky=stick, columnspan=span, pady=py)
    return l

def myEntryFrame(f, width, row, col, stick, span):
    entryTxt = tk.Entry(f, width=width)
    entryTxt.grid(row=row, column=col, sticky=stick, columnspan=span)
    return entryTxt

def myTextFrame(f,row,col,width,height,stick,span,bg=None,fg=None,bd=None,font=None,yscrollcommand=None,xscrollcommand=None):
    textTxt = tk.Text(f, width=width,height=height,bg=bg,fg=fg,bd=bd,font=font,yscrollcommand=yscrollcommand,xscrollcommand=xscrollcommand)
    textTxt.grid(row=row, column=col, sticky=stick, columnspan=span)
    return textTxt

def myButton(f,row,col,command,rowspan,sticky,text,bg=None,fg=None,font=None,bd=None,relief=None):
    myButton = tk.Button(f,text=text,command=command,bg=bg,fg=fg,font=font,bd=bd,relief=relief)
    myButton.grid(row=row,column=col,rowspan=rowspan,sticky=sticky)
    return myButton