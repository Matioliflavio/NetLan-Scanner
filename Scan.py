from multiprocessing.dummy import Pool as ThreadPool 
import os
import socket


def scan2(ip):
      ping = "ping -w 1 -n 1 -i 1 " + str(ip)
      if os.system(ping) == 0:
            try:
                  hostname = socket.gethostbyaddr("10.0.1." + str(n))
            except:
                  hostname = None
                  print("erro ao tentar resolver hostName")
            
            #aqui entra o get macaddress
            arp = Popen(["arp", "-n", ip], stdout=PIPE)
            s = arp.communicate()[0]
            macaddress = re.search(r'(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})', s).groups()[0]

            #aqui entra o resolve vendorName
            
            return ip, hostmane, macaddress, vendor
      else:
            return None, None, None, None