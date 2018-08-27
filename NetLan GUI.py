from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter import messagebox as mbox
import datetime


class FramePrincipal(Frame):
    
    #data
    _data = datetime.date.today()

    #Cores
    _cinza = "#d9d9d9"
    _preto = "#000000"
    _branco = "#FFFFFF"
    _marinho = "#101E63"

    #Fontes
    _font1 = "Tahoma 9 "
    _font2 = "Tahoma 10"
    _font3 = "Tahoma 13"
    _font4 = "Tahoma 18"

    #Strings
    _version = "0.01b"

    _columns = ('IP', 'Macaddress', 'Vendor', 'Hostname', 'Ports')

    def __init__(self, master=None):
        
        #------------------------
        #-------- Janela --------
        #------------------------
        super().__init__()
        self.master.iconbitmap("Icons/NetLan Scanner.ico")
        self.centralizar(900,600)
        self.master.title("Net Lan Scanner    *V" + str(self._version))
        self.master.resizable(True, True)
        self.master.minsize(width=900, height=300)
        self.master["bg"] = self._branco
        self.pack()

        #--cluster Botôes
        self.frameBtns = Frame( bg=self._marinho, height=80)
        self.frameBtns.pack(side=TOP,fill=X) 

        self.btnScan = Button(self.frameBtns, width=78, height=30)
        self.imgScan = PhotoImage(file="Icons/Scan.png")
        self.btnScan.config(image=self.imgScan)
        self.btnScan.pack(side=LEFT, padx=5, pady=10)  

        self.btnClear = Button(self.frameBtns, width=78, height=30)
        self.imgClear = PhotoImage(file="Icons/Clear2.png")
        self.btnClear.config(image=self.imgClear)
        self.btnClear.pack(side=LEFT, padx=5, pady=10)
    
        self.btnRange = Button(self.frameBtns, text="IP Range: 192.168.200.254 - 192.168.200.254", font=self._font3, justify=LEFT, width=40, height=1)
        self.btnRange.pack(side=LEFT, padx=5, pady=10)
    
        self.btnPort = Button(self.frameBtns, width=78, height=30)
        self.imgPort = PhotoImage(file="Icons/Port.png")
        self.btnPort.config(image=self.imgPort)
        self.btnPort.pack(side=LEFT, padx=5, pady=10)

        self.progress = ttk.Progressbar(self.frameBtns, orient="horizontal", length=140, mode="determinate")
        self.progress.pack(side=LEFT, padx=5, pady=10)

        self.btnSave = Button(self.frameBtns, width=78, height=30)
        self.imgSave = PhotoImage(file="Icons/Save.png")
        self.btnSave.config(image=self.imgSave)
        self.btnSave.pack(side=LEFT, padx=5, pady=10)

        self.frameTabela = Frame()#height=550
        self.frameTabela.pack(fill="both", expand=True) 

        self.tabela = ttk.Treeview()
        self.tabela["columns"] = ('IP', 'Macaddress', 'Vendor', 'Hostname', 'Ports')
        self.scrollTab = Scrollbar(orient=VERTICAL, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=self.scrollTab.set)
        self.tabela.grid(column=0, row=0, sticky="nsew", in_=self.frameTabela)
        self.scrollTab.grid(column=1, row=0, sticky='ns', in_=self.frameTabela)
        
        self.frameTabela.grid_columnconfigure(0, weight=1)
        self.frameTabela.grid_rowconfigure(0, weight=1)

        #self.CreateUI()

        for n in range(50):
            self.tabela.insert('', 'end', text=n, values=(10+n,'MAC', 'VENDOR'+str(n), "Hosrname"+str(n), "Ports"))
        
    # ------------------------------------------------------------------------------------------
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNÇÕES GERAIS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # ------------------------------------------------------------------------------------------ 
    def centralizar(self, larg, alt):
        px=int((self.master.winfo_screenwidth()-larg)/2)
        py=int((self.master.winfo_screenheight()-alt)/2)
        self.master.geometry("{}x{}+{}+{}".format(larg, alt, px, py))
    
    def CreateUI(self):
        
        tv = ttk.Treeview(self.frameTabela, height=40)
        self.scrollTab = Scrollbar(self.frameTabela, orient=VERTICAL)
        tv['yscrollcommand'] = self.scrollTab.set
        tv['columns'] = ('IP', 'Macaddress', 'Vendor', 'Hostname', 'Ports')
        tv.heading("#0", text='N°', anchor='w')
        tv.column("#0", anchor="center",width=40, minwidth=40)
        tv.heading('IP', text='IP')
        tv.column('IP', anchor='center', width=130, minwidth=130)
        tv.heading('Macaddress', text='Mac Address')
        tv.column('Macaddress', anchor='center', width=140, minwidth=140)
        tv.heading('Vendor', text='Vendor')
        tv.column('Vendor', anchor='center', width=230)
        tv.heading('Hostname', text='Host Name')
        tv.column('Hostname', anchor='center', width=240)
        tv.heading('Ports', text='Scaned Ports')
        tv.column('Ports', anchor='center', width=100)
        tv.pack(fill="both")
        self.scrollTab["command"] = tv.yview
        self.scrollTab.pack(side=RIGHT, fill="both")
        self.treeview = tv

    #funções a serem ajustadas: sortby e build tree
    def sortby(tree, col, descending):
        """Sort tree contents when a column is clicked on."""
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        tree.heading(col,
            command=lambda col=col: sortby(tree, col, int(not descending)))

    def _build_tree(self):
        for col in tree_columns:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # XXX tkFont.Font().measure expected args are incorrect according
            #     to the Tk docs
            self.tree.column(col, width=tkinter.font.Font().measure(col.title()))

        for item in tree_data:
            self.tree.insert('', 'end', values=item)

            # adjust columns lenghts if necessary
            for indx, val in enumerate(item):
                ilen = tkinter.font.Font().measure(val)
                if self.tree.column(tree_columns[indx], width=None) < ilen:
                    self.tree.column(tree_columns[indx], width=ilen)


def main():
    app = FramePrincipal()
    app.mainloop()

main()

