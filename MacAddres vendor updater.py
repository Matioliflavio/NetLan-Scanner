import requests
import csv
import json

url = "https://standards.ieee.org/develop/regauth/oui/oui.csv"
print("Obtendo arquivo")
download = requests.get(url)
download = download.content.decode('utf-8')
arquivo = csv.reader(download.splitlines(), delimiter=',')
lista = list(arquivo)
print("Arquivo Obtido")

print("criando lista json")
jsonList = {}
for row in lista:
    jsonList[str(row[1])] = str(row[2])

print("Criando json")
f = open("MacAddressVendor.json", "w")
json.dump(jsonList, f, sort_keys=True, indent=4)
f.close()
print("Feito!!")

