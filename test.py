import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory


class CustomWidget(tk.Frame):
    def __init__(self, parent, n):
        tk.Frame.__init__(self, parent)

        self.path = tk.StringVar()
        self.filename = tk.StringVar()

        self.root = ttk.LabelFrame(self, text=n)
        self.root.grid(padx=30, pady=10, ipadx=0)

        self.filenameLabel = ttk.Label(self.root, text="檔案名稱")
        self.filenameLabel.grid(ipadx=10, padx=10, pady=0, row=0, column=0)

        self.filenameEntry = ttk.Entry(self.root, textvariable=self.filename)
        self.filenameEntry.grid(ipadx=10, padx=10, pady=0, row=1, column=0)

        self.pathLabel = ttk.Label(self.root, text="檔案歸檔路徑")
        self.pathLabel.grid(ipadx=10, padx=10, pady=0, row=0, column=1)

        self.pathEntry = ttk.Entry(self.root, textvariable=self.path)
        self.pathEntry.grid(ipadx=10, padx=1, pady=0, row=1, column=1)

        self.pathButton = ttk.Button(self.root, text="路徑選擇", command=self.selectPath)
        self.pathButton.grid(ipadx=10, padx=1, pady=0, row=1, column=2)

        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('active', 'red'), ('!disabled', "red")],
                  background=[('active', 'white'), ('!disabled', "white")]
                  )

        self.removeButton = ttk.Button(self.root, text="移除", command=self.remove, style="C.TButton")
        self.removeButton.grid(ipadx=10, padx=0, pady=0, row=1, column=3)

    def selectPath(self):
        path_ = askdirectory()
        self.path.set(path_)

    def remove(self):
        print("remove this")

    def getFilename(self):
        return self.filename

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.applicationRoot = ttk.Frame(self)
        self.applicationRoot.grid(row=0, column=0)

        for i in range(1, 3, 1):
            self.e = CustomWidget(self.applicationRoot, str(i))
            self.e.grid(row=i-1, column=0, sticky="EW")
            self.grid_rowconfigure(i-1, weight=0)

if __name__ == "__main__":
    root = tk.Tk()
    Application(root).place(x=0, y=0, relwidth=1, relheight=1)
    root.mainloop()