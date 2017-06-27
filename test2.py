#!/bin/env python
# -*- coding: utf-8 -*-

'''
Demo about tkinter's .grid() method <ipadx, padx>
'''

import tkinter as tk
import tkinter.ttk as ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master, width=800, height=400)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.grid_propagate(0)
        self.label()
        self.label2()
        self.label3()
        self.grid_info()

    def label(self):
        lf = ttk.Labelframe(self, text='label')
        lf.grid(padx=(30, 30), pady=(20, 0), ipadx=70)

        quitButton = ttk.Button(lf, text='Quit',
            command=self.quit)
        quitButton.grid(ipadx=(30), padx=(30, 30), pady=(20, 20))

        print('---1---')
        quitButton.update()
        print(quitButton.winfo_width(), quitButton.winfo_height(), lf.winfo_width())

    def label2(self):
        lf = ttk.Labelframe(self, text='label2')
        lf.grid(padx=(30, 30), pady=(20, 0), ipadx=100)

        quitButton = ttk.Button(lf, text='Quit',
            command=self.quit)
        quitButton.grid(padx=(30, 30), pady=(20, 20))
        print('---2---')
        quitButton.update()
        print(quitButton.winfo_width(), quitButton.winfo_height(), lf.winfo_width())


    def label3(self):
        lf = ttk.Labelframe(self, text='label3')
        lf.grid(padx=(30, 30), pady=(20, 0), sticky=tk.W)

        quitButton = ttk.Button(lf, text='Quit',
            command=self.quit)
        quitButton.grid(padx=(30, 30), pady=(20, 20))
        print('---3---')
        quitButton.update()
        print(quitButton.winfo_width(), quitButton.winfo_height(), lf.winfo_width())


    def grid_info(self):

        print(self.grid_size())


app = Application()
app.master.title('Sample Application')
app.mainloop()