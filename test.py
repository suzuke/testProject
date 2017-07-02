#!/usr/bin/env python3
# coding=utf-8

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import json
import os
import sys

class CustomWidget(ttk.Frame):
    def __init__(self, parent, n, remove_callback, data="", **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        self.ignore = False
        self.n = n

        self.path = tk.StringVar()
        self.path.trace("w", self.check_path)
        self.path_label_text_map = {0: ("檔案歸檔路徑", "black"),
                                    1: ("檔案歸檔路徑不存在", "red")}

        self.filename = tk.StringVar()
        self.filename.trace("w", self.check_filename)
        self.filename_label_text_map = {0: ("檔案名稱關鍵字", "black"),
                                        1: ("檔案名稱關鍵字不能為空", "red")}

        self.remove_callback = remove_callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.root = ttk.LabelFrame(self, text=self.n)
        self.root.grid(row=0, column=0, padx=1, pady=1, ipadx=1, ipady=1, sticky="EW")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=5)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self.filenameLabel = ttk.Label(self.root,
                                       text=self.filename_label_text_map[0][0],
                                       foreground=self.filename_label_text_map[0][1])
        self.filenameLabel.grid(ipadx=1, padx=2, pady=0, row=0, column=0, sticky="W")

        self.filenameEntry = ttk.Entry(self.root, textvariable=self.filename)
        self.filenameEntry.grid(ipadx=1, padx=2, pady=0, row=1, column=0, sticky="EW")

        self.pathLabel = ttk.Label(self.root,
                                   text=self.path_label_text_map[0][0],
                                   foreground=self.path_label_text_map[0][1])
        self.pathLabel.grid(ipadx=1, padx=2, pady=0, row=0, column=1, sticky="W")

        self.pathEntry = ttk.Entry(self.root, textvariable=self.path)
        self.pathEntry.grid(ipadx=1, padx=2, pady=0, row=1, column=1, sticky="EW")

        self.pathButton = ttk.Button(self.root, text="選擇資料夾", command=self.select_path, width=10)
        self.pathButton.grid(ipadx=10, padx=1, pady=0, row=1, column=2, sticky="EW")

        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('active', 'red'), ('!disabled', "red")],
                  background=[('active', 'white'), ('!disabled', "white")]
                  )

        self.removeButton = ttk.Button(self.root, text="移除", command=self.remove, style="C.TButton", width=5)
        self.removeButton.grid(ipadx=10, padx=0, pady=0, row=1, column=3, sticky="EW")

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

    def set_filename_label(self, msg_code):
        self.filenameLabel.configure(text=self.filename_label_text_map[msg_code][0],
                                     foreground=self.filename_label_text_map[msg_code][1])

    def set_path_label(self, msg_code):
        self.pathLabel.configure(text=self.path_label_text_map[msg_code][0],
                                 foreground=self.path_label_text_map[msg_code][1])

    def remove(self):
        if messagebox.askokcancel("刪除", "是否真的要移除?"):
            self.remove_callback(self)

    def check_path(self, *args):
        _path = self.path.get()
        if os.path.isdir(_path):
            self.set_path_label(0)
            self.ignore = False
        else:
            self.set_path_label(1)
            self.ignore = True

    def check_filename(self, *args):
        _filename = self.filename.get()
        if _filename.strip():
            self.set_filename_label(0)
            self.ignore = False
        else:
            self.set_filename_label(1)
            self.ignore = True

    def need_ignore(self):
        return self.ignore


class scrollableContainer(tk.Frame):
    """A scrollable container that can contain a number of messages"""

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)  # holds canvas & scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        self.vScroll = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.vScroll.grid(row=0, column=1, sticky='ns')
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.configure(yscrollcommand=self.vScroll.set)

        self.frm = tk.Frame(self.canvas, bd=2)  # holds widget
        self.frm.grid_columnconfigure(0, weight=1)

        self.canvas.create_window(0, 0, window=self.frm, anchor='nw', tags='inner')

        self.widgets = []

        self.update_layout()
        self.canvas.bind('<Configure>', self.on_configure)

    def update_layout(self):
        self.frm.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.canvas.yview('moveto', '1.0')
        self.size = self.frm.grid_size()

    def on_configure(self, event):
        w, h = event.width, event.height
        natural = self.frm.winfo_reqwidth()
        self.canvas.itemconfigure('inner', width=w if w > natural else natural)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def add_widget(self, data):
        w = CustomWidget(self.frm, self.size[1] + 1, self.remove, data)
        w.grid(row=self.size[1], column=0, padx=2, pady=2, sticky='we')
        self.widgets.append(w)
        self.update_layout()

    def get_widgets(self):
        return self.widgets

    def remove(self, widget):
        self.widgets.remove(widget)
        widget.grid_forget()
        for i in range(len(self.widgets)):
            self.widgets[i].set_label_n(str(i + 1))
            self.widgets[i].grid(row=(i + 1), column=0, sticky="EW")
        self.update_layout()

    def clear(self):
        for widget in self.widgets:
            widget.grid_forget()
        self.widgets.clear()
        self.update_layout()


class Application(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super(Application, self).__init__(parent, **kwargs)

        self.version = "版本: v0.1"

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
                               2: ("歸類處理的資料夾為空", "red")}

        self.label = ttk.Label(self.first, text="")
        self.label.grid(row=0, column=0, sticky="EW")

        self.workingDirectoryPath = tk.StringVar()
        self.workingDirectoryPath.trace("w", self.check_working_path)
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
        self.second.grid_rowconfigure(3, weight=1)

        self.saveButton = ttk.Button(self.second, text=" 儲存設定", command=self.save)
        self.saveButton.grid(row=0, column=0, sticky="EW")

        self.loadButton = ttk.Button(self.second, text=" 載入設定", command=self.load)
        self.loadButton.grid(row=1, column=0, sticky="EW")

        self.addSettingButton = ttk.Button(self.second, text="+新増歸類檔案項目", command=self.add)
        self.addSettingButton.grid(row=2, column=0, sticky="EW")

        self.clearSettingButton = ttk.Button(self.second, text="清除所有歸類檔案項目", command=self.clear_all)
        self.clearSettingButton.grid(row=3, column=0, sticky="EW")

        # third
        self.third = ttk.LabelFrame(self, text="歸類檔案項目")
        self.third.grid(row=2, column=0, padx=10, pady=5, ipadx=1, ipady=1, sticky="NSEW")
        self.third.grid_columnconfigure(0, weight=1)
        self.third.grid_rowconfigure(0, weight=1)

        self.sc = scrollableContainer(self.third, bd=2)
        self.sc.grid(row=0, column=0, sticky="NSEW")

        # fourth
        self.versionLabel = ttk.Label(self, text=self.version)
        self.versionLabel.grid(row=3, column=0, padx=10, pady=2, ipadx=1, ipady=1, sticky="E")

    def select_working_path(self):
        path_ = askdirectory()
        self.workingDirectoryPath.set(path_)
        if os.path.isdir(path_):
            self.set_label(0)
        else:
            self.set_label(1)

    def classify(self, files, keyword, from_folder, to_folder):
        done = True
        for file in files:
            if keyword in file:
                done = self.move_to(file, from_folder, to_folder)
        return done

    def start(self):
        check_ok = True
        done = True
        working_directory = self.workingDirectoryPath.get()
        if os.path.isdir(working_directory):
            widgets = self.sc.get_widgets()

            if len(widgets) == 0:
                messagebox.showerror("提示訊息", "歸檔項目為空，請至少新增一項歸檔項目。")
                return

            # single core
            for widget in widgets:

                widget.check_path()
                widget.check_filename()
                if widget.need_ignore():
                    check_ok = False
                    continue

                keyword = widget.get_filename()
                to_folder = widget.get_path()

                if not os.path.isdir(to_folder):
                    widget.set_path_label(1)
                    check_ok = False

                if check_ok:
                    files = [x for x in os.listdir(working_directory) if not x.startswith('.')]
                    done = self.classify(files, keyword, working_directory, to_folder)

            if check_ok:
                messagebox.showinfo("提示訊息", "已完成檔案歸類。")
            else:
                messagebox.showerror("提示訊息", "部分設定有誤，請檢查設定再試一次。")
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

    def clear_all(self):
        self.sc.clear()

    def move_to(self, filename, from_folder, to_folder):
        from_file = os.path.join(from_folder, filename)
        to_file = os.path.join(to_folder, filename)
        if not to_file == from_file:
            if os.path.isfile(from_file):
                if os.path.exists(to_folder):
                    os.rename(from_file, to_file)
                    return True
        return False

    def check_working_path(self, *args):
        _path = self.workingDirectoryPath.get()
        if os.path.isdir(_path):
            self.set_label(0)
        else:
            self.set_label(1)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("檔案歸類")
    root.geometry('800x600')
    root.iconbitmap(resource_path("icon.ico"))
    root.minsize(width=600, height=600)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    app = Application(root)
    app.grid(row=0, column=0, pady=10, sticky="NSEW")

    # def on_close():
    #    app.save()
    #    root.destroy()
    # root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
