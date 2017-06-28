import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory

class CustomWidget(tk.Frame):
    def __init__(self, parent, n, remove_callback):
        tk.Frame.__init__(self, parent)

        self.path = tk.StringVar()
        self.filename = tk.StringVar()

        self.root = ttk.LabelFrame(self, text=n)
        self.root.grid(padx=1, pady=5, ipadx=1, ipady=1, sticky="EW")

        self.filenameLabel = ttk.Label(self.root, text="檔案名稱")
        self.filenameLabel.grid(ipadx=10, padx=10, pady=0, row=0, column=0)

        self.filenameEntry = ttk.Entry(self.root, textvariable=self.filename, width=10)
        self.filenameEntry.grid(ipadx=10, padx=10, pady=0, row=1, column=0)

        self.pathLabel = ttk.Label(self.root, text="檔案歸檔路徑")
        self.pathLabel.grid(ipadx=10, padx=10, pady=0, row=0, column=1)

        self.pathEntry = ttk.Entry(self.root, textvariable=self.path, width=35)
        self.pathEntry.grid(ipadx=10, padx=1, pady=0, row=1, column=1)

        self.pathButton = ttk.Button(self.root, text="選擇資料夾", command=self.select_path, width=10)
        self.pathButton.grid(ipadx=10, padx=1, pady=0, row=1, column=2)

        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('active', 'red'), ('!disabled', "red")],
                  background=[('active', 'white'), ('!disabled', "white")]
                  )

        self.removeButton = ttk.Button(self.root, text="移除", command=lambda: remove_callback(self), style="C.TButton", width=5)
        self.removeButton.grid(ipadx=10, padx=0, pady=0, row=1, column=3)

    def select_path(self):
        path_ = askdirectory()
        self.path.set(path_)

    def get_filename(self):
        return self.filename

    def set_label_n(self, n):
        self.root.config(text=str(n))


class Application(ttk.Frame):
    def __init__(self, parent):
        super(Application, self).__init__(parent, width=800, height=400)

        self.applicationRoot = ttk.Frame(self)
        self.applicationRoot.grid(row=0, column=0, padx=30, pady=5)

        # first
        self.first = ttk.LabelFrame(self.applicationRoot, text="A.選擇要歸類處理的資料夾")
        self.first.grid(row=0, column=0, padx=1, pady=5, ipadx=171, ipady=1)
        self.first.grid_columnconfigure(0, weight=1)
        self.first.grid_rowconfigure(0, weight=1)

        self.workingDirectoryPath = tk.StringVar()
        self.workingDirectoryPathEntry = ttk.Entry(self.first, textvariable=self.workingDirectoryPath)
        self.workingDirectoryPathEntry.grid(row=0, column=0, sticky="EW")

        self.workingDirectoryPathButton = ttk.Button(self.first, text="選擇資料夾", command=self.select_working_path)
        self.workingDirectoryPathButton.grid(row=0, column=1, sticky="EW")

        self.startButton = ttk.Button(self.first, text="一鍵歸類", command=self.start)
        self.startButton.grid(row=1, column=0, sticky="EWNS", columnspan=2)

        # second
        self.second = ttk.LabelFrame(self.applicationRoot, text="B.歸類檔案項目設定")
        self.second.grid(row=1, column=0, padx=1, pady=5, ipadx=230, ipady=1)
        self.second.grid_columnconfigure(0, weight=1)
        self.second.grid_rowconfigure(0, weight=1)

        self.addSettingButton = ttk.Button(self.second, text="+新増歸類檔案項目", command=self.add)
        self.addSettingButton.grid(row=0, column=0, sticky="EW")

        # third
        self.third = ttk.LabelFrame(self.applicationRoot, text="C.歸類檔案項目")
        self.third.grid(row=2, column=0, padx=1, pady=5, ipadx=1, ipady=1, sticky="EW")
        self.third.grid_columnconfigure(0, weight=1)
        self.third.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.third, borderwidth=0)
        self.canvas.grid(row=0, column=0, sticky="NSWE")

        self.frame = tk.Frame(self.canvas)

        self.vsb = ttk.Scrollbar(self.third, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky="NS")
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.customWidgetList = []

    def select_working_path(self):
        path_ = askdirectory()
        self.workingDirectoryPath.set(path_)

    def start(self):
        print("Start...")

    def add(self):
        i = len(self.customWidgetList) + 1
        print("add %d" % i)
        widget = CustomWidget(self.frame, str(i), self.remove)
        self.customWidgetList.append(widget)
        widget.grid(row=i, column=0, sticky="EW")
        self.grid_rowconfigure(i - 1, weight=1)

    def remove(self, custom_widget):
        self.customWidgetList.remove(custom_widget)
        custom_widget.grid_forget()
        for i in range(len(self.customWidgetList)):
            self.customWidgetList[i].set_label_n(i+1)
            self.customWidgetList[i].grid(row=(i+1), column=0, sticky="EW")

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    root.title("檔案自動分類")
    app = Application(root)
    app.grid(row=0, column=0)
    root.mainloop()
