from tkinter import *

class FramePortScan(Frame):
    
    #Cores
    _cinza = "#d9d9d9"
    _preto = "#000000"
    _branco = "#FFFFFF"
    _marinho = "#101E63"
    _agua = "#f2f7ff"

    #Fontes
    _font1 = "Tahoma 9 "
    _font2 = "Tahoma 10"
    _font3 = "Tahoma 13"
    _font4 = "Tahoma 18"
    _font5 = "Tahoma 13 Bold"

    def __init__(self, master=None):
        
        #------------------------
        #-------- Janela --------
        #------------------------

        super().__init__()
        self.master.iconbitmap("Icons/NetLan Scanner.ico")
        self.centralizar(300,140)
        self.master.title("Port Scan")
        self.master.resizable(False, False)
        self.master["bg"] = self._branco
        self.pack()

        #--cluster radio 1
        self.frameRd1 = Frame()
        self.frameRd1.pack(side=TOP,fill=X) 
        self.var = StringVar()
        self.commomRd = Radiobutton(self.frameRd1, text="Scan Common Ports", variable=self.var, value="Common", command=self.radioselect)
        self.commomRd.pack(side=LEFT)
        self.var.set("Common")

        #--cluster radio 2
        self.frameRd2 = Frame()
        self.frameRd2.pack(side=TOP,fill=X) 
        self.commomRd = Radiobutton(self.frameRd2, text="Scan All Ports", variable=self.var, value="All", command=self.radioselect)
        self.commomRd.pack(side=LEFT)

        #--cluster radio 3
        self.frameRd3 = Frame()
        self.frameRd3.pack(side=TOP,fill=X) 
        self.commomRd = Radiobutton(self.frameRd3, text="Scan slected port range:", variable=self.var, value="Range", command=self.radioselect)
        self.commomRd.pack(side=LEFT)
        

        self.frameRange = Frame()
        self.frameRange.pack(side=TOP, fill=X)
        self.endtPort = Entry(self.frameRange, width=10, state=DISABLED)
        self.endtPort.pack(side=RIGHT, padx=5)

        self.lblTo = Label(self.frameRange, text=" to ")
        self.lblTo.pack(side=RIGHT)

        self.startPort = Entry(self.frameRange, width=10, state=DISABLED)
        self.startPort.pack(side=RIGHT, padx=5)
        self.lblp = Label(self.frameRange, text="min= 0  max= 48151")
        self.lblp.pack(side=LEFT, padx=5)
        

        #--cluster botoes
        self.frameBtn = Frame()
        self.frameBtn.pack(side=TOP, fill=X)
        self.btnCancel = Button(self.frameBtn, text="Cancel", width=10, command=self.cancel)
        self.btnCancel.pack(side=RIGHT, padx=10, pady=10)
        
        self.btnOK = Button(self.frameBtn, text="OK", width=10, command=self.ok)
        self.btnOK.pack(side=RIGHT, padx=10)


    def radioselect(self):
        print("Item: %s" %self.var.get())
        if self.var.get()=="Range":
            self.startPort["state"]= NORMAL
            self.endtPort["state"]= NORMAL
        else:
            self.startPort["state"]= DISABLED
            self.endtPort["state"]= DISABLED

    
    def centralizar(self, larg, alt):
        px=int((self.master.winfo_screenwidth()-larg)/2)
        py=int((self.master.winfo_screenheight()-alt)/2)
        self.master.geometry("{}x{}+{}+{}".format(larg, alt, px, py))

    def cancel(self):
        self.master.destroy()
    
    def ok(self):
        print("ok")

def main():
    app = FramePortScan()
    app.mainloop()

main()