from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter import messagebox as mbox
from multiprocessing.dummy import Pool as ThreadPool 
from getmac import get_mac_address
import ipaddress
import socket
import json
import csv
import os
import struct

#before to start, install lib getmac: pip install get-mac

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
    _version = "0.40b"

    _columns = ('IP', 'Macaddress', 'Vendor', 'Hostname', 'Ports')

    listCount = 1

    scanResult = []

    scannedPorts = []

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

        super().__init__()
        self.master.iconbitmap("Icons/NetLan Scanner.ico")
        self.center(900,300) #(900, 600)
        self.master.title("Net Lan Scanner   >" + str(self.hostIP) + " - " + str(self.hostName) + " <   "+ "*V" + str(self._version))
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
        self.startIP.bind("<Return>", self.funcBtnScan)

        self.to = Label(self.frameBtns, text="to:", font=self._font3, bg=self._marinho, fg=self._branco)
        self.to.pack(side=LEFT, padx=1, pady=10)

        self.endIPaddr = StringVar()
        self.endIP = Entry(self.frameBtns, textvariable=self.endIPaddr, font=self._font3, width=14)
        self.endIP.pack(side=LEFT, padx=3, pady=10)
        self.endIP.bind("<Return>", self.funcBtnScan)

        self.getLocalIP()
    
        self.btnPort = Button(self.frameBtns, width=78, height=30, command=self.funcBtnPort)
        self.imgPort = PhotoImage(file="Icons/Port.png")
        self.btnPort.config(image=self.imgPort)
        self.btnPort.pack(side=LEFT, padx=5, pady=10)

        #self.progress = ttk.Progressbar(self.frameBtns, orient="horizontal", length=132, mode="determinate")
        self.status = StringVar()
        self.progress = Entry(self.frameBtns, textvariable=self.status, font=self._font3, width=14, state=DISABLED)
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
    def center(self, larg, alt):
        px=int((self.master.winfo_screenwidth()-larg)/2)
        py=int((self.master.winfo_screenheight()-alt)/2)
        self.master.geometry("{}x{}+{}+{}".format(larg, alt, px, py))

    def sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.sort_column(tv, col, not reverse))
    
    def showMsg(self, title, msg):
        mbox.showinfo(title, msg)
    
    def getLocalIP(self):
        self.startIPaddr.set(socket.gethostbyname(socket.gethostname()))
        if self.startIPaddr.get() == "127.0.0.1":
            self.showMsg("Alert", "You aren´t connected to a network.\nVerify your conectcion!")
        try: 
            ipRange= self.hostIP.split(".")
            self.startIPaddr.set(".".join(ipRange[:3])+".1")
            self.endIPaddr.set(".".join(ipRange[:3])+".254") 
        except: 
            print("Unable to get Hostname and IP")

    def funcBtnClear(self):
        self.scanResult.clear()
        self.status.set("")
        for i in self.tabela.get_children():
            self.tabela.delete(i)

    def funcBtnScan(self, event=None):
        
        self.funcBtnClear()
        self.status.set("Scaning..Wait!")
        l = self.buildIpList(self.startIPaddr.get(), self.endIPaddr.get())
        if l == None: 
            return
        else:
            result = self.multiThreadScan(l)

        if result:
            self.printTable(result)
        self.status.set("Done!")

    def funcBtnPort(self):
        print("Port")
        port = None
        try:
            selectedRow = self.tabela.item(self.tabela.focus())["values"]
            print(selectedRow)
            ip = selectedRow[1]
            port = FramePortScan(self, ip).show()
            self.tabela.delete("I"+str(selectedRow[0]).zfill(3))    
            self.tabela.insert('', selectedRow[0] - 1 , values=(str(selectedRow[0]).zfill(2), selectedRow[1], selectedRow[2], selectedRow[3], selectedRow[4], port), tags=("par" if selectedRow[0] % 2 == 0 else "impar",))
        except:
            self.showMsg("Error", "Select one item to scan ports!")

    def funcBtnSave(self):
        print("Save")
        if self.scanResult:
            self.janelaSave = Toplevel(self.master)
            self.appSave = FrameSave(self.janelaSave, self.scanResult)
        else:
            self.showMsg("Atention", "Start scan before save results!")
    #--------------------------------------------------
    #--- Funções do scaner ----------------------------
    #--------------------------------------------------

    def scan(self, ip):
        print("start scan %s" %ip)
        ping = "ping -n 1 -i 1 -w 1000 " + str(ip)
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

    def buildIpList(self, startIP, endIP):
        try:
            socket.inet_aton(startIP)
            start = startIP.split(".")
        except socket.error:
            print("StartIP NOT VALID")
            self.showMsg("Scan Error", "Check Start IP. \nIt´s not valid IP address!")
            return
        try:
            socket.inet_aton(endIP)
        except socket.error:
            print("END IP NOT VALID")
            self.showMsg("Scan Error", "Check End IP. \n It´s not valid IP address!")
            return
        #qtd = int(ipaddress.IPv4Address(endIP)) - int(ipaddress.IPv4Address(startIP)) + 1
        l=[]
        #adiciona uns broadcast pra melhorar o resultado?!
        for i in range(2):
            l.append(str(start[0]) + "." + str(start[1]) + "." + str(start[2]) + ".255")
       
        start = struct.unpack('>I', socket.inet_aton(startIP))[0]
        end = struct.unpack('>I', socket.inet_aton(endIP))[0]
        for i in range(start, end):
            l.append(socket.inet_ntoa(struct.pack('>I', i)))
        l.append(endIP)
        return l

    def multiThreadScan(self, ipRange):
        print("Start Multithread")
        pool = ThreadPool(50) 
        result = pool.map(self.scan, ipRange) 
        pool.close() 
        return result

    def printTable(self, data):
        print("print Table")
        self.listCount = 1
        for n in data:
            if n:
                ip = {}
                ip["id"] = str(self.listCount).zfill(2)
                ip["ip"] = n[0]
                ip["macaddress"] = n[1]
                ip["vendor"] = n[2]
                ip["hostname"] = n[3]
                self.scanResult.append(ip)
                self.tabela.insert('', 'end', text=n, values=(str(self.listCount).zfill(2), n[0],  n[1], n[2], n[3]), tags=("par" if self.listCount % 2 == 0 else "impar",) )
                self.listCount += 1
        self.tabela.tag_configure("par", background=self._agua)
        self.tabela.tag_configure("impar", background=self._branco)
        self.showMsg("Done", "Scan Complete!")
        print(self.scanResult)

    

class FrameSave(Frame):

    #Fontes
    _font2 = "Tahoma 10"

    def __init__(self, master, data):
        
        super().__init__()
        self.data = data
        self.master = master
        #self.master.geometry("300x125")
        self.center(300,125)
        self.master.resizable(False,False)
        self.master.iconbitmap("Icons/NetLan Scanner.ico")
        self.master.title("Save")
        self.pack()

        #--cluster radio 1
        self.frameRd1 = Frame(self.master)
        self.frameRd1.pack(side=TOP,fill=X) 
        self.var = StringVar()
        self.txtRd = Radiobutton(self.frameRd1, text="Save as TXT", variable=self.var, value="txt", command=self.radioselect, font=self._font2)
        self.txtRd.pack(side=LEFT, padx=10)
        self.var.set("txt")

        #--cluster radio 2
        self.frameRd2 = Frame(self.master)
        self.frameRd2.pack(side=TOP,fill=X) 
        self.csvRd = Radiobutton(self.frameRd2, text="Save as CSV", variable=self.var, value="csv", command=self.radioselect, font=self._font2)
        self.csvRd.pack(side=LEFT, padx=10)

        #--cluster radio 3
        self.frameRd3 = Frame(self.master)
        self.frameRd3.pack(side=TOP,fill=X) 
        self.jsonRd = Radiobutton(self.frameRd3, text="Save as JSON", variable=self.var, value="json", command=self.radioselect, font=self._font2)
        self.jsonRd.pack(side=LEFT, padx=10)

        #--cluster botoes
        self.frameBtn = Frame(self.master)
        self.frameBtn.pack(side=TOP, fill=X)
        self.btnCancel = Button(self.frameBtn, text="Cancel", width=10, command=self.cancel, font=self._font2)
        self.btnCancel.pack(side=RIGHT, padx=10, pady=10)
        
        self.btnOK = Button(self.frameBtn, text="OK", width=10, command=self.ok, font=self._font2)
        self.btnOK.pack(side=RIGHT, padx=10)


    def radioselect(self):
        print("Item: %s" %self.var.get())

    
    def center(self, larg, alt):
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
            try:
                f = open(caminho + os.sep + "ScanResult.txt", "w")
                for iten in self.data:
                    f.writelines("ID: " + str(iten["id"]) + 
                                "\tIP: " + str(iten["ip"]) + 
                                "\tMacAddress: " +  str(iten["macaddress"]) + 
                                "\tVendor: " +  str(iten["vendor"]) + 
                                "\tHostName: " +  str(iten["hostname"]) + "\n")
                f.close()
            except:
                mbox.showinfo("Error", "Can´t save file!")
        elif self.var.get()=="csv":
            print("csv")
            try:
                f = open(caminho + os.sep + "ScanResult.csv", "w")
                columns = ["id", "ip", "macaddress", "vendor", "hostname"]
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                for data in self.data:
                    writer.writerow(data)
                f.close()
            except:
                mbox.showinfo("Error", "Can´t save file!")
        else:
            print("JSON")
            try:
                f = open(caminho + os.sep + "ScanResult.json", "w")
                json.dump(self.data, f, sort_keys=True, indent=4)
                f.close()
            except:
                mbox.showinfo("Error", "Can´t save file!")
        mbox.showinfo("Export", "File Saved!")        
        self.master.destroy()



class FramePortScan(Frame):
    
    #Fontes
    _font1 = "Tahoma 9 "
    _font2 = "Tahoma 10"

    # 21 FTP / 22 SSH / 23 TELNET / 25 SMTP / 53 DNS / 80 HTTP / 110 POP3 / 115 SFTP / 135 RPC
    # 139 NetBIOS / 143 IMAP / 194 IRC / 443 SSL / 445 SMB / 1433 MSSQL / 3306 MySQL / 3389 Remote Desktop
    # 5632 PCAnywhere / 5900 VNC / 6112 Warcraft III  
    _common = [21, 22, 23, 25, 53, 80, 110, 115, 135, 139, 143, 194, 443, 445, 1433, 3306, 3389, 5632, 5900, 6112]

    _portResult = []

    def __init__(self, master, data):

        self.data = data
        self.toplevel = tk.Toplevel(master)
        self.center(320,150)
        self.toplevel.iconbitmap(bitmap="Icons/NetLan Scanner.ico")
        self.toplevel.title("Port Scan")
        self.toplevel.resizable(False, False)
        
        #--cluster radio 1
        self.frameRd1 = Frame(self.toplevel)
        self.frameRd1.pack(side=TOP,fill=X) 
        self.var = StringVar()
        self.commomRd = Radiobutton(self.frameRd1, text="Scan Common Ports. 1 min", variable=self.var, value="Common", command=self.radioselect, font=self._font2)
        self.commomRd.pack(side=LEFT)
        self.var.set("Common")

        #--cluster radio 2
        self.frameRd2 = Frame(self.toplevel)
        self.frameRd2.pack(side=TOP,fill=X) 
        self.commomRd = Radiobutton(self.frameRd2, text="Scan All Ports.  5 min", variable=self.var, value="All", command=self.radioselect, font=self._font2)
        self.commomRd.pack(side=LEFT)

        #--cluster radio 3
        self.frameRd3 = Frame(self.toplevel)
        self.frameRd3.pack(side=TOP,fill=X) 
        self.commomRd = Radiobutton(self.frameRd3, text="Scan slected port range:", variable=self.var, value="Range", command=self.radioselect, font=self._font2)
        self.commomRd.pack(side=LEFT)
        
        self.frameRange = Frame(self.toplevel)
        self.frameRange.pack(side=TOP, fill=X)
        self.endPort = Entry(self.frameRange, width=10, state=DISABLED, font=self._font2)
        self.endPort.pack(side=RIGHT, padx=5)

        self.lblTo = Label(self.frameRange, text=" to ", font=self._font2)
        self.lblTo.pack(side=RIGHT)

        self.startPort = Entry(self.frameRange, width=10, state=DISABLED, font=self._font2)
        self.startPort.pack(side=RIGHT, padx=5)
        self.lblp = Label(self.frameRange, text="min= 0 max= 48151", font=self._font1)
        self.lblp.pack(side=LEFT, padx=5)
        
        #--cluster botoes
        self.frameBtn = Frame(self.toplevel)
        self.frameBtn.pack(side=TOP, fill=X)
        self.btnCancel = Button(self.frameBtn, text="Cancel", width=10, command=self.cancel, font=self._font2)
        self.btnCancel.pack(side=RIGHT, padx=10, pady=10)
        
        self.btnOK = Button(self.frameBtn, text="OK", width=10, command=self.ok, font=self._font2)
        self.btnOK.pack(side=RIGHT, padx=10)

    def center(self, larg, alt):
        px=int((self.toplevel.winfo_screenwidth()-larg)/2)
        py=int((self.toplevel.winfo_screenheight()-alt)/2)
        self.toplevel.geometry("{}x{}+{}+{}".format(larg, alt, px, py))

    def radioselect(self):
        print("Item: %s" %self.var.get())
        if self.var.get()=="Range":
            self.startPort["state"]= NORMAL
            self.endPort["state"]= NORMAL
        else:
            self.startPort["state"]= DISABLED
            self.endPort["state"]= DISABLED

    def cancel(self):
        self.toplevel.destroy()
    
    def ok(self):
        print("ok")
        result = None
        if self.var.get()=="Range":
            print("Range")
            r = []
            for i in range(int(self.startPort.get()), (int(self.endPort.get()) + 1)):
                r.append(i)   
            result = self.multiThreadScan(r)
        elif self.var.get()=="All":
            print("All")
            allPorts = []
            for n in range(48152):
                allPorts.append(n)
            result = self.multiThreadScan(allPorts)
        else:
            print("Common")
            result = self.multiThreadScan(self._common)
        for n in result:
            if n:
                self._portResult.append(n)
        print(self._portResult)
        self.toplevel.destroy()

    def portScan(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.data, port))
            return port
        except:
            return None

    def multiThreadScan(self, portRange):
        print("Start Multithread")
        pool = ThreadPool(1000) 
        result = pool.map(self.portScan, portRange) 
        pool.close() 
        return result

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        value = self._portResult
        print("show")
        print(value)
        return value

def main():
    app = FramePrincipal()
    app.mainloop()

main()