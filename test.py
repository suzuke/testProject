#!/usr/bin/env python
#coding=utf-8

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import json
import os

class CustomWidget(ttk.Frame):
    def __init__(self, parent, n, remove_callback, data="", **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        self.path = tk.StringVar()
        self.filename = tk.StringVar()
        self.n = n
        self.path_label_text_map = {0: ("檔案歸檔路徑", "black"),
                                    1: ("檔案歸檔路徑不存在", "red")}

        self.remove_callback = remove_callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.root = ttk.LabelFrame(self, text=self.n)
        self.root.grid(row=0, column=0, padx=1, pady=1, ipadx=1, ipady=1, sticky="EW")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.filenameLabel = ttk.Label(self.root, text="檔案名稱")
        self.filenameLabel.grid(ipadx=1, padx=5, pady=0, row=0, column=0, sticky="W")

        self.filenameEntry = ttk.Entry(self.root, textvariable=self.filename)
        self.filenameEntry.grid(ipadx=1, padx=5, pady=0, row=1, column=0, sticky="EW")

        self.pathLabel = ttk.Label(self.root,
                                   text=self.path_label_text_map[0][0],
                                   foreground=self.path_label_text_map[0][1])
        self.pathLabel.grid(ipadx=1, padx=5, pady=0, row=0, column=1, sticky="W")

        self.pathEntry = ttk.Entry(self.root, textvariable=self.path)
        self.pathEntry.grid(ipadx=1, padx=5, pady=0, row=1, column=1, sticky="EW")

        self.pathButton = ttk.Button(self.root, text="選擇資料夾", command=self.select_path, width=10)
        self.pathButton.grid(ipadx=10, padx=1, pady=0, row=1, column=2)

        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('active', 'red'), ('!disabled', "red")],
                  background=[('active', 'white'), ('!disabled', "white")]
                  )

        self.removeButton = ttk.Button(self.root, text="移除", command=self.remove, style="C.TButton", width=5)
        self.removeButton.grid(ipadx=10, padx=0, pady=0, row=1, column=3)

        self.restore(data)

    def select_path(self):
        path_ = askdirectory()
        self.path.set(path_)
        if os.path.isdir(path_):
            self.set_path_label(0)
        else:
            self.set_path_label(1)

    def get_filename(self):
        return self.filename.get()

    def get_path(self):
        return self.path.get()

    def set_label_n(self, n):
        self.root.config(text=n)
        self.n = n

    def get_label_n(self):
        return self.n

    def get_json_string(self):
        data = [{"n": self.n,
                 "value": (self.filename.get(), self.path.get())
                 }]
        return json.dumps(data)

    def restore(self, json_string):
        if json_string is "":
            return
        data = json.loads(json_string)
        self.set_label_n(data[0]["n"])
        self.filenameEntry.delete(0, tk.END)
        self.filenameEntry.insert(0, data[0]["value"][0])
        self.pathEntry.delete(0, tk.END)
        self.pathEntry.insert(0, data[0]["value"][1])

    def set_path_label(self, error_code):
        self.pathLabel.configure(text=self.path_label_text_map[error_code][0],
                                 foreground=self.path_label_text_map[error_code][1])

    def remove(self):
        if messagebox.askokcancel("刪除", "是否真的要移除?"):
            self.remove_callback(self)

class scrollableContainer(tk.Frame):
    """A scrollable container that can contain a number of messages"""

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs) #holds canvas & scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canv = tk.Canvas(self, bd=0, highlightthickness=0)
        self.vScroll = ttk.Scrollbar(self, orient='vertical', command=self.canv.yview)
        self.vScroll.grid(row=0, column=1, sticky='ns')
        self.canv.grid(row=0, column=0, sticky='nsew')
        self.canv.configure(yscrollcommand=self.vScroll.set)

        self.frm = tk.Frame(self.canv, bd=2) #holds widget
        self.frm.grid_columnconfigure(0, weight=1)

        self.canv.create_window(0, 0, window=self.frm, anchor='nw', tags='inner')

        self.widgets = []

        self.update_layout()
        self.canv.bind('<Configure>', self.on_configure)

    def update_layout(self):
        self.frm.update_idletasks()
        self.canv.configure(scrollregion=self.canv.bbox('all'))
        self.canv.yview('moveto', '1.0')
        self.size = self.frm.grid_size()

    def on_configure(self, event):
        w, h = event.width, event.height
        natural = self.frm.winfo_reqwidth()
        self.canv.itemconfigure('inner', width=w if w > natural else natural)
        self.canv.configure(scrollregion=self.canv.bbox('all'))

    def add_widget(self, data):
        w = CustomWidget(self.frm, self.size[1]+1, self.remove, data)
        w.grid(row=self.size[1], column=0, padx=2, pady=2, sticky='we')
        self.widgets.append(w)
        self.update_layout()

    def get_widgets(self):
        return self.widgets

    def remove(self, widget):
        self.widgets.remove(widget)
        widget.grid_forget()
        for i in range(len(self.widgets)):
            self.widgets[i].set_label_n(str(i+1))
            self.widgets[i].grid(row=(i+1), column=0, sticky="EW")
        self.update_layout()

    def clear(self):
        for widget in self.widgets:
            widget.grid_forget()
        self.update_layout()

class Application(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super(Application, self).__init__(parent, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.data = os.getcwd() + "\data"

        # first
        self.first = ttk.LabelFrame(self, text="選擇要歸類處理的資料夾")
        self.first.grid(row=0, column=0, padx=10, pady=1, ipadx=0, ipady=1, sticky="NEW")
        self.first.grid_columnconfigure(0, weight=1)
        self.first.grid_rowconfigure(0, weight=1)
        self.first.grid_rowconfigure(1, weight=1)
        self.first.grid_rowconfigure(2, weight=1)

        self.label_text_map = {0: ("", "black"),
                               1: ("歸類處理的資料夾不存在", "red"),
                               2: ("歸類處理的資料夾為空", "red"),
                               3: ("歸類檔案項目為空，請新增項目", "red")}
        self.label = ttk.Label(self.first, text="")
        self.label.grid(row=0, column=0, sticky="EW")

        self.workingDirectoryPath = tk.StringVar()
        self.workingDirectoryPathEntry = ttk.Entry(self.first, textvariable=self.workingDirectoryPath)
        self.workingDirectoryPathEntry.grid(row=1, column=0, sticky="EW")

        self.workingDirectoryPathButton = ttk.Button(self.first, text="選擇資料夾", command=self.select_working_path)
        self.workingDirectoryPathButton.grid(row=1, column=1, sticky="EW")

        self.startButton = ttk.Button(self.first, text="一鍵歸類", command=self.start)
        self.startButton.grid(row=2, column=0, sticky="EWNS", columnspan=2)

        # second
        self.second = ttk.LabelFrame(self, text="歸類檔案項目設定")
        self.second.grid(row=1, column=0, padx=10, pady=5, ipadx=1, ipady=1, sticky="EW")
        self.second.grid_columnconfigure(0, weight=1)
        self.second.grid_rowconfigure(0, weight=1)
        self.second.grid_rowconfigure(1, weight=1)
        self.second.grid_rowconfigure(2, weight=1)

        self.addSettingButton = ttk.Button(self.second, text=" 儲存設定", command=self.save)
        self.addSettingButton.grid(row=0, column=0, sticky="EW")

        self.addSettingButton = ttk.Button(self.second, text=" 載入設定", command=self.load)
        self.addSettingButton.grid(row=1, column=0, sticky="EW")

        self.addSettingButton = ttk.Button(self.second, text="+新増歸類檔案項目", command=self.add)
        self.addSettingButton.grid(row=2, column=0, sticky="EW")

        # third
        self.third = ttk.LabelFrame(self, text="歸類檔案項目")
        self.third.grid(row=2, column=0, padx=10, pady=5, ipadx=1, ipady=1, sticky="NSEW")
        self.third.grid_columnconfigure(0, weight=1)
        self.third.grid_rowconfigure(0, weight=1)

        self.sc = scrollableContainer(self.third, bd=2)
        self.sc.grid(row=0, column=0, sticky="NSEW")

    def select_working_path(self):
        path_ = askdirectory()
        self.workingDirectoryPath.set(path_)
        if os.path.isdir(path_):
            self.set_label(0)
        else:
            self.set_label(1)

    def classify(self, file):
        file_path = os.path.join(self.workingDirectoryPath.get(), file)
        if os.path.isfile(file_path):

            widgets = self.sc.get_widgets()
            if len(widgets) == 0:
                self.set_label(3)

            for widget in widgets:
                if widget.get_filename() in file:
                    to_folder = widget.get_path()
                    if os.path.isdir(to_folder):
                        widget.set_path_label(0)
                        self.moveto(file, self.workingDirectoryPath.get(), to_folder)
                    else:
                        widget.set_path_label(1)

    def start(self):
        working_directory = self.workingDirectoryPath.get()
        if os.path.isdir(working_directory):
            files = [x for x in os.listdir(working_directory) if not x.startswith('.')]
            if len(files) == 0:
                self.set_label(2)

            #single core
            for file in files:
                self.classify(file)

            messagebox.showinfo("提示訊息", "已完成檔案歸類")
        else:
            self.set_label(1)

    def set_label(self, error_code):
        self.label.configure(text=self.label_text_map[error_code][0],
                             foreground=self.label_text_map[error_code][1])

    def save(self):
        with open(self.data, "w") as f:
            f.write(json.dumps([{"path": self.workingDirectoryPath.get()}]) + "\n")
            widgets = self.sc.get_widgets()
            for widget in widgets:
                f.write(widget.get_json_string() + "\n")

    def load(self):
        self.sc.clear()
        with open(self.data, "r") as f:
            line = f.readline()
            if line is not "":
                data = json.loads(line)
                self.workingDirectoryPathEntry.delete(0, tk.END)
                self.workingDirectoryPathEntry.insert(0, data[0]["path"])
            for line in f:
                self.add(line)

    def add(self, data=""):
        self.sc.add_widget(data)

    def moveto(self, filename, from_folder, to_folder):
        from_file = os.path.join(from_folder, filename)
        to_file = os.path.join(to_folder, filename)
        if not to_file == from_file:
            if os.path.isfile(from_file):
                if not os.path.exists(to_folder):
                    os.makedirs(to_folder)
                os.rename(from_file, to_file)

if __name__ == "__main__":
    root = tk.Tk()
    #root.resizable(False, False)
    root.title("檔案歸類")
    root.iconbitmap("office.ico")
    root.geometry('800x600')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    app = Application(root)
    app.grid(row=0, column=0, pady=10, sticky="NSEW")

    #def on_close():
    #    app.save()
    #    root.destroy()
    #root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
