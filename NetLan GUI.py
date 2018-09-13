from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter import messagebox as mbox
from multiprocessing.dummy import Pool as ThreadPool 
from getmac import get_mac_address
import ipaddress
import socket
import json
import os
import SaveGUI as save
import PortScanGUI as pscan

class FramePrincipal(Frame):
    
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

    #Strings
    _version = "0.11b"

    _columns = ('IP', 'Macaddress', 'Vendor', 'Hostname', 'Ports')

    _datatable = []

    try: 
        hostName = socket.gethostname() 
        hostIP = socket.gethostbyname(hostName)  
    except: 
        print("Unable to get Hostname and IP")

    #vendor list
    f = open("MacAddressVendor.json", "r")
    _vendorList = json.load(f)
    print("Vendor list Loaded")
    f.close()

    def __init__(self, master=None):
        
        #------------------------
        #-------- Janela --------
        #------------------------

        super().__init__()
        self.master.iconbitmap("Icons/NetLan Scanner.ico")
        self.centralizar(900,300) #(900, 600)
        self.master.title("Net Lan Scanner   >" + str(self.hostIP) + " " + str(self.hostName) + "<   "+ "*V" + str(self._version))
        self.master.resizable(True, True)
        self.master.minsize(width=900, height=300) #(width=900, height=300)
        self.master["bg"] = self._branco
        self.pack()

        #--cluster Botôes
        self.frameBtns = Frame( bg=self._marinho, height=80)
        self.frameBtns.pack(side=TOP,fill=X) 

        self.btnScan = Button(self.frameBtns, width=78, height=30, command=self.funcBtnScan)
        self.imgScan = PhotoImage(file="Icons/Scan.png")
        self.btnScan.config(image=self.imgScan)
        self.btnScan.pack(side=LEFT, padx=5, pady=10)  

        self.btnClear = Button(self.frameBtns, width=78, height=30, command=self.funcBtnClear)
        self.imgClear = PhotoImage(file="Icons/Clear2.png")
        self.btnClear.config(image=self.imgClear)
        self.btnClear.pack(side=LEFT, padx=5, pady=10)

        self.ipRange = Label(self.frameBtns, text="IP Range:", font=self._font3, bg=self._marinho, fg=self._branco)
        self.ipRange.pack(side=LEFT, padx=3, pady=10)

        self.startIPaddr = StringVar()
        self.startIP = Entry(self.frameBtns, textvariable=self.startIPaddr, font=self._font3, width=14)
        self.startIP.pack(side=LEFT, padx=1, pady=10)

        self.to = Label(self.frameBtns, text="to:", font=self._font3, bg=self._marinho, fg=self._branco)
        self.to.pack(side=LEFT, padx=1, pady=10)

        self.endIPaddr = StringVar()
        self.endIP = Entry(self.frameBtns, textvariable=self.endIPaddr, font=self._font3, width=14)
        self.endIP.pack(side=LEFT, padx=3, pady=10)

        self.getLocalIP()
    
        self.btnPort = Button(self.frameBtns, width=78, height=30, command=self.funcBtnPort)
        self.imgPort = PhotoImage(file="Icons/Port.png")
        self.btnPort.config(image=self.imgPort)
        self.btnPort.pack(side=LEFT, padx=5, pady=10)

        self.progress = ttk.Progressbar(self.frameBtns, orient="horizontal", length=132, mode="indeterminate")
        self.progress.pack(side=LEFT, padx=5, pady=10)

        self.btnSave = Button(self.frameBtns, width=78, height=30, command=self.funcBtnSave)
        self.imgSave = PhotoImage(file="Icons/Save.png")
        self.btnSave.config(image=self.imgSave)
        self.btnSave.pack(side=LEFT, padx=5, pady=10)

        self.frameTabela = Frame()#height=550
        self.frameTabela.pack(fill="both", expand=True) 

        self.tabela = ttk.Treeview(show="headings")
        self.tabela["columns"] = ("N°", "IP", "Macaddress", "Vendor", "Hostname", "Ports")
        self.scrollTab = Scrollbar(orient=VERTICAL, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=self.scrollTab.set)
        self.tabela.grid(column=0, row=0, sticky="nsew", in_=self.frameTabela)
        self.scrollTab.grid(column=1, row=0, sticky='ns', in_=self.frameTabela)
        
        self.tabela.heading("N°", text='N°', anchor='w', command=lambda: self.sort_column(self.tabela, "N°", 1))
        self.tabela.column("N°", anchor="center", width=20, minwidth=20)
        self.tabela.heading('IP', text='IP', command=lambda: self.sort_column(self.tabela, "IP", 1))
        self.tabela.column('IP', anchor='center', width=130, minwidth=130)
        self.tabela.heading('Macaddress', text='Mac Address', command=lambda: self.sort_column(self.tabela, "Macaddress", 1))
        self.tabela.column('Macaddress', anchor='center', width=140, minwidth=140)
        self.tabela.heading('Vendor', text='Vendor', command=lambda: self.sort_column(self.tabela, "Vendor", 1))
        self.tabela.column('Vendor', anchor='center', width=230, minwidth=230)
        self.tabela.heading('Hostname', text='Host Name', command=lambda: self.sort_column(self.tabela, "Hostname", 1))
        self.tabela.column('Hostname', anchor='center', width=240, minwidth=240)
        self.tabela.heading('Ports', text='Scaned Ports', command=lambda: self.sort_column(self.tabela, "Ports", 1))
        self.tabela.column('Ports', anchor='center', width=100, minwidth=100)
        
        self.frameTabela.grid_columnconfigure(0, weight=1)
        self.frameTabela.grid_rowconfigure(0, weight=1)

        
    # ------------------------------------------------------------------------------------------
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNÇÕES GERAIS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # ------------------------------------------------------------------------------------------ 
    def centralizar(self, larg, alt):
        px=int((self.master.winfo_screenwidth()-larg)/2)
        py=int((self.master.winfo_screenheight()-alt)/2)
        self.master.geometry("{}x{}+{}+{}".format(larg, alt, px, py))

    def sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.sort_column(tv, col, not reverse))
    
    def getLocalIP(self):
        self.startIPaddr.set(socket.gethostbyname(socket.gethostname()))
        try: 
            ipRange= self.hostIP.split(".")
            self.startIPaddr.set(".".join(ipRange[:3])+".1")
            self.endIPaddr.set(".".join(ipRange[:3])+".254") 
        except: 
            print("Unable to get Hostname and IP")


    def funcBtnClear(self):
        for i in self.tabela.get_children():
            self.tabela.delete(i)

    def funcBtnScan(self):
        self.funcBtnClear()
        
        l = self.montaListaIp(self.startIPaddr.get(), self.endIPaddr.get())
        if l == None: 
            return
        else:
            result = self.multiThreadScan(l)
            print(result)
        if result:
            count = 1
            for n in result:
                if n:
                    self.tabela.insert('', 'end', text=n, values=(str(count).zfill(2), n[0],  n[1], n[2], n[3]), tags=("par" if count % 2 == 0 else "impar",) )
                    count += 1

        '''
        #provisorio so pra encher tabela! kkk
        for n in range(50):
            self.tabela.insert('', 'end', text=n, values=(str(n+1).zfill(2), 10+n,'MAC'+str(n).zfill(2), 'VENDOR'+str(n), "Hosrname"+str(n), "Ports"+str(n)), tags=("par" if n%2 == 0 else "impar",) )
        '''
        self.tabela.tag_configure("par", background=self._agua)
        self.tabela.tag_configure("impar", background=self._branco)


    def funcBtnPort(self):
        print("Port")
        print(self.tabela.get_children())
        
    
    def funcBtnSave(self):
        print("Save")
        self.app = save.main("teste")

    #--------------------------------------------------
    #--- Funções do scaner ----------------------------
    #--------------------------------------------------

    def scan(self, ip):
        print("start scan %s" %ip)
        ping = "ping -n 1 -i 1 -w 500 " + str(ip)
        
        if os.system(ping) == 0:
            #Mac Address
            try:
                macaddress = get_mac_address(ip=str(ip))
                vendor = self._vendorList[macaddress[:9].replace(":", "").upper()]
            except:
                macaddress = None
                vendor = None

            #Host Name
            try:
                hostname = socket.gethostbyaddr(str(ip))[0]
            except:
                hostname = None
                print("erro ao tentar resolver hostName")

            return ip, macaddress, vendor, hostname
        else:
            return
        

    def montaListaIp(self, startIP, endIP):
        try:
            socket.inet_aton(startIP)
            start = startIP.split(".")
        except socket.error:
            print("StartIP NOT VALID")
            return
        try:
            socket.inet_aton(endIP)
            end = endIP.split(".")
        except socket.error:
            print("END IP NOT VALID")
            return
        qtd = int(ipaddress.IPv4Address(endIP)) - int(ipaddress.IPv4Address(startIP)) + 1
        l=[]
        for i in range(3):
            l.append(str(start[0]) + "." + str(start[1]) + "." + str(start[2]) + ".255")
       
        for n in range(qtd):
            l.append(str(start[0]) + "." + str(start[1]) + "." + str(start[2]) + "." + str(n+1))
        
        return l



    def multiThreadScan(self, ipRange):
        print("Start Multithread")
        pool = ThreadPool(4) 
        result = pool.map(self.scan, ipRange) 
        pool.close() 
        return result

def main():
    app = FramePrincipal()
    app.mainloop()

main()