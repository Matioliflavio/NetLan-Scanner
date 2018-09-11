from multiprocessing.dummy import Pool as ThreadPool 
import os
import socket
from getmac import get_mac_address
import json

#carrega vendor json list
f = open("MacAddressVendor.json", "r")
vendorDataTable = json.load(f)
f.close()

def scan(ip):
      ping = "ping -n 1 -i 1 -w 500 " + str(ip)
      if os.system(ping) == 0:
            #Mac Address
            try:
                  macaddress = get_mac_address(ip=str(ip))
                  vendor = vendorDataTable[macaddress[:9].replace(":", "").upper()]
            except:
                  macaddress = None
                  vendor = None

            #Host Name
            try:
                  hostname = socket.gethostbyaddr("10.0.1." + str(n))
            except:
                  hostname = None
                  print("erro ao tentar resolver hostName")
            if macaddress:
                  return ip, macaddress, vendor, hostname
            else:
                  return
      else:
            return 

def montaListaIp(startIP, endIP):
      l = []

      print("a")

def multiThreadScan(ipRange):
      
      i=[]
      for n in range(254): 
            i.append("10.0.1." + str(n))
            
      pool = ThreadPool() 
      result = pool.map(scan, i) 
      pool.close() 
      count = 0
      return result


