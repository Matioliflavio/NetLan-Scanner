from tkinter import *
from tkinter import filedialog

class FramePortScan(Frame):


    #Fontes
    _font2 = "Tahoma 10"

    def __init__(self, master=None):
        
        #------------------------
        #-------- Janela --------
        #------------------------

        super().__init__()
        self.master.iconbitmap("Icons/NetLan Scanner.ico")
        self.centralizar(300,125)
        self.master.title("Save")
        self.master.resizable(False, False)
        self.pack()

        #--cluster radio 1
        self.frameRd1 = Frame()
        self.frameRd1.pack(side=TOP,fill=X) 
        self.var = StringVar()
        self.txtRd = Radiobutton(self.frameRd1, text="Save as TXT", variable=self.var, value="txt", command=self.radioselect, font=self._font2)
        self.txtRd.pack(side=LEFT, padx=10)
        self.var.set("txt")

        #--cluster radio 2
        self.frameRd2 = Frame()
        self.frameRd2.pack(side=TOP,fill=X) 
        self.csvRd = Radiobutton(self.frameRd2, text="Save as CSV", variable=self.var, value="csv", command=self.radioselect, font=self._font2)
        self.csvRd.pack(side=LEFT, padx=10)

        #--cluster radio 3
        self.frameRd3 = Frame()
        self.frameRd3.pack(side=TOP,fill=X) 
        self.jsonRd = Radiobutton(self.frameRd3, text="Save as JSON", variable=self.var, value="json", command=self.radioselect, font=self._font2)
        self.jsonRd.pack(side=LEFT, padx=10)

        #--cluster botoes
        self.frameBtn = Frame()
        self.frameBtn.pack(side=TOP, fill=X)
        self.btnCancel = Button(self.frameBtn, text="Cancel", width=10, command=self.cancel, font=self._font2)
        self.btnCancel.pack(side=RIGHT, padx=10, pady=10)
        
        self.btnOK = Button(self.frameBtn, text="OK", width=10, command=self.ok, font=self._font2)
        self.btnOK.pack(side=RIGHT, padx=10)


    def radioselect(self):
        print("Item: %s" %self.var.get())

    
    def centralizar(self, larg, alt):
        px=int((self.master.winfo_screenwidth()-larg)/2)
        py=int((self.master.winfo_screenheight()-alt)/2)
        self.master.geometry("{}x{}+{}+{}".format(larg, alt, px, py))

    def cancel(self):
        self.master.destroy()
    
    def ok(self):
        print("ok")
        caminho = filedialog.askdirectory()
        if self.var.get()=="txt":
            print("txt")
        elif self.var.get()=="csv":
            print("csv")
        else:
            print("JSON")
        print(caminho)

def main():
    app = FramePortScan()
    app.mainloop()

main()