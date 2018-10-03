from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter import messagebox as mbox
from multiprocessing.dummy import Pool as ThreadPool
import threading 
from getmac import get_mac_address
import ipaddress
import socket
import json
import csv
import os
import struct

#before to start, install lib getmac: pip install get-mac

class MainFrame(Frame):
    
    #Color
    _white = "#FFFFFF"
    _marine = "#101E63"
    _water = "#f2f7ff"
    _red = "#FF0000"

    #Font
    _font1 = "Tahoma 9 "
    _font2 = "Tahoma 10"
    _font3 = "Tahoma 13"

    #Variables
    _version = "0.80b"

    _columns = ('IP', 'Macaddress', 'Vendor', 'Hostname', 'Ports')

    _listCount = 1

    _scanResult = []

    try: 
        _hostName = socket.gethostname() 
        _hostIP = socket.gethostbyname(_hostName)  
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
        self.center(900,600)
        self.master.title("Net Lan Scanner   > " + str(self._hostIP) + " - " + str(self._hostName) + " <   "+ "*V" + str(self._version))
        self.master.resizable(True, True)
        self.master.minsize(width=900, height=300)
        self.master["bg"] = self._white
        self.pack()

        #------Buttons------
        self.frameBtns = Frame( bg=self._marine, height=80)
        self.frameBtns.pack(side=TOP,fill=X)

        #-Button Scan
        self.btnScan = Button(self.frameBtns, width=78, height=30, command=self.funcBtnScan)
        self.imgScan = PhotoImage(file="Icons/Scan.png")
        self.btnScan.config(image=self.imgScan)
        self.btnScan.pack(side=LEFT, padx=5, pady=10)  

        #-Button Clear
        self.btnClear = Button(self.frameBtns, width=78, height=30, command=self.funcBtnClear)
        self.imgClear = PhotoImage(file="Icons/Clear2.png")
        self.btnClear.config(image=self.imgClear)
        self.btnClear.pack(side=LEFT, padx=5, pady=10)

        #-IP Range
        self.ipRange = Label(self.frameBtns, text="IP Range:", font=self._font3, bg=self._marine, fg=self._white)
        self.ipRange.pack(side=LEFT, padx=3, pady=10)

        self.startIPaddr = StringVar()
        self.startIP = Entry(self.frameBtns, textvariable=self.startIPaddr, font=self._font3, width=14)
        self.startIP.pack(side=LEFT, padx=1, pady=10)
        self.startIP.bind("<Return>", self.funcBtnScan)

        self.to = Label(self.frameBtns, text="to:", font=self._font3, bg=self._marine, fg=self._white)
        self.to.pack(side=LEFT, padx=1, pady=10)

        self.endIPaddr = StringVar()
        self.endIP = Entry(self.frameBtns, textvariable=self.endIPaddr, font=self._font3, width=14)
        self.endIP.pack(side=LEFT, padx=3, pady=10)
        self.endIP.bind("<Return>", self.funcBtnScan)

        self.getLocalIP()
    
        #-Button Port Scan
        self.btnPort = Button(self.frameBtns, width=78, height=30, command=self.funcBtnPort)
        self.imgPort = PhotoImage(file="Icons/Port.png")
        self.btnPort.config(image=self.imgPort)
        self.btnPort.pack(side=LEFT, padx=5, pady=10)

        #-Status Mensage
        self.status = StringVar()
        self.progress = Entry(self.frameBtns, textvariable=self.status, disabledforeground=self._red, font=self._font3, width=14, state=DISABLED)
        self.progress.pack(side=LEFT, padx=5, pady=10)

        #-Button Save
        self.btnSave = Button(self.frameBtns, width=78, height=30, command=self.funcBtnSave)
        self.imgSave = PhotoImage(file="Icons/Save.png")
        self.btnSave.config(image=self.imgSave)
        self.btnSave.pack(side=LEFT, padx=5, pady=10)

        #------TreeView------
        self.frameTable = Frame()
        self.frameTable.pack(fill="both", expand=True) 

        self.table = ttk.Treeview(show="headings")
        self.table["columns"] = ("N°", "IP", "Macaddress", "Vendor", "Hostname", "Ports")
        self.scrollTab = Scrollbar(orient=VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollTab.set)
        self.table.grid(column=0, row=0, sticky="nsew", in_=self.frameTable)
        self.scrollTab.grid(column=1, row=0, sticky='ns', in_=self.frameTable)
        
        self.table.heading("N°", text='N°', anchor='w', command=lambda: self.sort_column(self.table, "N°", 1))
        self.table.column("N°", anchor="center", width=20, minwidth=20)
        self.table.heading('IP', text='IP', command=lambda: self.sort_column(self.table, "IP", 1))
        self.table.column('IP', anchor='center', width=130, minwidth=130)
        self.table.heading('Macaddress', text='Mac Address', command=lambda: self.sort_column(self.table, "Macaddress", 1))
        self.table.column('Macaddress', anchor='center', width=140, minwidth=140)
        self.table.heading('Vendor', text='Vendor', command=lambda: self.sort_column(self.table, "Vendor", 1))
        self.table.column('Vendor', anchor='center', width=230, minwidth=230)
        self.table.heading('Hostname', text='Host Name', command=lambda: self.sort_column(self.table, "Hostname", 1))
        self.table.column('Hostname', anchor='center', width=240, minwidth=240)
        self.table.heading('Ports', text='Scaned Ports', command=lambda: self.sort_column(self.table, "Ports", 1))
        self.table.column('Ports', anchor='center', width=100, minwidth=100)
        
        self.frameTable.grid_columnconfigure(0, weight=1)
        self.frameTable.grid_rowconfigure(0, weight=1)
        
    #  ------------------------------------------------------------------------------------------
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GENERAL FUNCTIONS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #  ------------------------------------------------------------------------------------------ 
    #centralize window
    def center(self, larg, alt):
        px=int((self.master.winfo_screenwidth()-larg)/2)
        py=int((self.master.winfo_screenheight()-alt)/2)
        self.master.geometry("{}x{}+{}+{}".format(larg, alt, px, py))

    #sort treeview column
    def sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.sort_column(tv, col, not reverse))
    
    #alert mensages
    def showMsg(self, title, msg):
        mbox.showinfo(title, msg)
    
    #get machine IP and define start and end ip
    def getLocalIP(self):
        self.startIPaddr.set(socket.gethostbyname(socket.gethostname()))
        if self.startIPaddr.get() == "127.0.0.1":
            self.showMsg("Alert", "You are not connected to a network.\nVerify your connection!")
        try: 
            ipRange= self._hostIP.split(".")
            self.startIPaddr.set(".".join(ipRange[:3])+".1")
            self.endIPaddr.set(".".join(ipRange[:3])+".254") 
        except: 
            print("Unable to get Hostname and IP")

    #button clear function
    def funcBtnClear(self):
        self._scanResult.clear()
        self.status.set("")
        for i in self.table.get_children():
            self.table.delete(i)

    #button scan function
    def funcBtnScan(self, event=None):
        self.status.set("Scaning...Wait!")
        self.after(500, self.start)

    #start scan procedure
    def start(self):
        self.funcBtnClear()
        l = self.buildIpList(self.startIPaddr.get(), self.endIPaddr.get())
        if l == None: 
            return
        else:
            result = self.multiThreadScan(l)

        if result:
            self.printTable(result)
            self.showMsg("Done", "Scan Complete!")

        self.status.set("")

    #button port scan function
    def funcBtnPort(self):
        print("Port")
        port = None
        try:
            selectedRow = self.table.item(self.table.focus())["values"]
            
        except:
            self.showMsg("Error", "Select one item to scan ports!")

        try:
            ip = selectedRow[1]
            #start port scan class
            port = FramePortScan(self, ip).show()
            self.table.delete("I"+str(selectedRow[0]).zfill(3))    
            self.table.insert('', selectedRow[0] - 1 , values=(str(selectedRow[0]).zfill(2), selectedRow[1], selectedRow[2], selectedRow[3], selectedRow[4], port), tags=("even" if selectedRow[0] % 2 == 0 else "odd",))
            self._scanResult[selectedRow[0]-1]["ports"] = port
        except:
            self.showMsg("Error", "Can´t scan ports!")

    #button save function
    def funcBtnSave(self):
        print("Save")
        if self._scanResult:
            self.janelaSave = Toplevel(self.master)
            #start save class
            self.appSave = FrameSave(self.janelaSave, self._scanResult)
        else:
            self.showMsg("Atention", "Start scan before save results!")
    #--------------------------------------------------
    #--- Scanner Functions ----------------------------
    #--------------------------------------------------
        
    #Step 1
    def buildIpList(self, startIP, endIP):
        try:
            socket.inet_aton(startIP)
            start = startIP.split(".")
        except socket.error:
            print("Start IP NOT VALID")
            self.showMsg("Scan Error", "Check Start IP. \nIt´s not valid IP address!")
            return
        try:
            socket.inet_aton(endIP)
        except socket.error:
            print("END IP NOT VALID")
            self.showMsg("Scan Error", "Check End IP. \n It´s not valid IP address!")
            return
        l=[]

        for i in range(2):
            l.append(str(start[0]) + "." + str(start[1]) + "." + str(start[2]) + ".255")
       
        start = struct.unpack('>I', socket.inet_aton(startIP))[0]
        end = struct.unpack('>I', socket.inet_aton(endIP))[0]
        for i in range(start, end):
            l.append(socket.inet_ntoa(struct.pack('>I', i)))
        l.append(endIP)
        return l
    
    #Step 2
    def multiThreadScan(self, ipRange):
        print("Start Multithread")
        pool = ThreadPool(50) 
        result = pool.map(self.scan, ipRange) 
        pool.close() 
        return result

    #Step 3
    def scan(self, ip):
        print("start scan %s" %ip)
        ping = "ping -n 1 -i 1 -w 1000 " + str(ip)
        if os.system(ping) == 0:
            #Mac Address
            try:
                macaddress = get_mac_address(ip=str(ip))
                #Vendor
                vendor = self._vendorList[macaddress[:9].replace(":", "").upper()]
            except:
                macaddress = None
                vendor = None

            #Host Name
            try:
                hostname = socket.gethostbyaddr(str(ip))[0]
            except:
                hostname = None
                print("Unable to get Hostname")

            return ip, macaddress, vendor, hostname
        else:
            return

    #Step 4
    def printTable(self, data):
        print("print Table")
        self._listCount = 1
        for n in data:
            if n:
                ip = {}
                ip["id"] = str(self._listCount).zfill(2)
                ip["ip"] = n[0]
                ip["macaddress"] = n[1]
                ip["vendor"] = n[2]
                ip["hostname"] = n[3]
                ip["ports"] = None
                self._scanResult.append(ip)
                self.table.insert('', 'end', text=n, values=(str(self._listCount).zfill(2), n[0],  n[1], n[2], n[3]), tags=("even" if self._listCount % 2 == 0 else "odd",) )
                self._listCount += 1
        self.table.tag_configure("even", background=self._water)
        self.table.tag_configure("odd", background=self._white)
        print(self._scanResult)

class FrameSave(Frame):

    #Font
    _font2 = "Tahoma 10"

    def __init__(self, master, data):
        
        super().__init__()
        self.data = data
        self.master = master
        self.center(300,125)
        self.master.resizable(False,False)
        self.master.iconbitmap("Icons/NetLan Scanner.ico")
        self.master.title("Save")
        self.pack()

        #Radio button TXT
        self.frameRd1 = Frame(self.master)
        self.frameRd1.pack(side=TOP,fill=X) 
        self.var = StringVar()
        self.txtRd = Radiobutton(self.frameRd1, text="Save as TXT", variable=self.var, value="txt", command=self.radioselect, font=self._font2)
        self.txtRd.pack(side=LEFT, padx=10)
        self.var.set("txt")

        #Radio button CSV
        self.frameRd2 = Frame(self.master)
        self.frameRd2.pack(side=TOP,fill=X) 
        self.csvRd = Radiobutton(self.frameRd2, text="Save as CSV", variable=self.var, value="csv", command=self.radioselect, font=self._font2)
        self.csvRd.pack(side=LEFT, padx=10)

        #Radio button JSON
        self.frameRd3 = Frame(self.master)
        self.frameRd3.pack(side=TOP,fill=X) 
        self.jsonRd = Radiobutton(self.frameRd3, text="Save as JSON", variable=self.var, value="json", command=self.radioselect, font=self._font2)
        self.jsonRd.pack(side=LEFT, padx=10)

        #Buttons
        self.frameBtn = Frame(self.master)
        self.frameBtn.pack(side=TOP, fill=X)
        self.btnCancel = Button(self.frameBtn, text="Cancel", width=10, command=self.cancel, font=self._font2)
        self.btnCancel.pack(side=RIGHT, padx=10, pady=10)
        
        self.btnOK = Button(self.frameBtn, text="OK", width=10, command=self.ok, font=self._font2)
        self.btnOK.pack(side=RIGHT, padx=10)

    def radioselect(self):
        print("Item: %s" %self.var.get())

    #Center Window
    def center(self, larg, alt):
        px=int((self.master.winfo_screenwidth()-larg)/2)
        py=int((self.master.winfo_screenheight()-alt)/2)
        self.master.geometry("{}x{}+{}+{}".format(larg, alt, px, py))
    
    #Cancel Button
    def cancel(self):
        self.master.destroy()
    
    #OK Button
    def ok(self):
        print("ok")
        caminho = filedialog.askdirectory()
        #Save to TXT
        if self.var.get()=="txt":
            print("txt")
            try:
                f = open(caminho + os.sep + "ScanResult.txt", "w")
                for iten in self.data:
                    f.writelines("ID: " + str(iten["id"]) + 
                                "\tIP: " + str(iten["ip"]) + 
                                "\tMacAddress: " +  str(iten["macaddress"]) + 
                                "\tVendor: " +  str(iten["vendor"]) + 
                                "\tHostName: " +  str(iten["hostname"]) + 
                                "\tPorts: " + str(iten["ports"]) + "\n")
                f.close()
            except:
                mbox.showinfo("Error", "Can´t save file!")
        #Save TO CSV
        elif self.var.get()=="csv":
            print("csv")
            try:
                f = open(caminho + os.sep + "ScanResult.csv", "w")
                columns = ["id", "ip", "macaddress", "vendor", "hostname", "ports"]
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                for data in self.data:
                    writer.writerow(data)
                f.close()
            except:
                mbox.showinfo("Error", "Can´t save file!")
        #Save to JSON
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
    
    #Font
    _font1 = "Tahoma 9 "
    _font2 = "Tahoma 10"

    #Common PORTS from yougetsignal.com/tools/open-ports
    # 21 FTP            / 22 SSH                / 23 TELNET         / 25 SMTP      / 53 DNS 
    # 80 HTTP           /110 POP3               / 115 SFTP          / 135 RPC      / 139 NetBIOS   
    # 143 IMAP          / 194 IRC               / 443 SSL           / 445 SMB      / 1433 MSSQL 
    # 3306 MySQL        / 3389 Remote Desktop   /5632 PCAnywhere    / 5900 VNC  
    # 6112 Warcraft III  

    _common = [21, 22, 23, 25, 53, 80, 110, 115, 135, 139, 143, 194, 443, 445, 1433, 3306, 3389, 5632, 5900, 6112]

    _portResult = []

    def __init__(self, master, data):

        self.data = data
        self.toplevel = tk.Toplevel(master)
        self.center(320,150)
        self.toplevel.iconbitmap(bitmap="Icons/NetLan Scanner.ico")
        self.toplevel.title("Port Scan")
        self.toplevel.resizable(False, False)
        
        #radio button 1
        self.frameRd1 = Frame(self.toplevel)
        self.frameRd1.pack(side=TOP,fill=X) 
        self.var = StringVar()
        self.commomRd = Radiobutton(self.frameRd1, text="Scan Common Ports. 1 min", variable=self.var, value="Common", command=self.radioselect, font=self._font2)
        self.commomRd.pack(side=LEFT)
        self.var.set("Common")

        #radio button 2
        self.frameRd2 = Frame(self.toplevel)
        self.frameRd2.pack(side=TOP,fill=X) 
        self.commomRd = Radiobutton(self.frameRd2, text="Scan All Ports.  5 min", variable=self.var, value="All", command=self.radioselect, font=self._font2)
        self.commomRd.pack(side=LEFT)

        #radio button 3
        self.frameRd3 = Frame(self.toplevel)
        self.frameRd3.pack(side=TOP,fill=X) 
        self.commomRd = Radiobutton(self.frameRd3, text="Scan slected port range.  All day long", variable=self.var, value="Range", command=self.radioselect, font=self._font2)
        self.commomRd.pack(side=LEFT)
        
        #Port range 
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

        #Buttons
        self.frameBtn = Frame(self.toplevel)
        self.frameBtn.pack(side=TOP, fill=X)
        self.btnCancel = Button(self.frameBtn, text="Cancel", width=10, command=self.cancel, font=self._font2)
        self.btnCancel.pack(side=RIGHT, padx=10, pady=10)
        
        self.btnOK = Button(self.frameBtn, text="OK", width=10, command=self.ok, font=self._font2)
        self.btnOK.pack(side=RIGHT, padx=10)

    #Center Window
    def center(self, larg, alt):
        px=int((self.toplevel.winfo_screenwidth()-larg)/2)
        py=int((self.toplevel.winfo_screenheight()-alt)/2)
        self.toplevel.geometry("{}x{}+{}+{}".format(larg, alt, px, py))

    #When select any radio
    def radioselect(self):
        print("Item: %s" %self.var.get())
        if self.var.get()=="Range":
            self.startPort["state"]= NORMAL
            self.endPort["state"]= NORMAL
        else:
            self.startPort["state"]= DISABLED
            self.endPort["state"]= DISABLED
    
    #Button Cancel
    def cancel(self):
        self.toplevel.destroy()
    
    #Button OK
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

    #Port Scan Step 1
    def multiThreadScan(self, portRange):
        print("Start Multithread")
        pool = ThreadPool(1000) 
        result = pool.map(self.portScan, portRange) 
        pool.close() 
        return result

    #Port Scan Step 2
    def portScan(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.data, port))
            return port
        except:
            return None

    #Run and wait window
    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        value = self._portResult
        return value

def main():
    app = MainFrame()
    app.mainloop()

main()