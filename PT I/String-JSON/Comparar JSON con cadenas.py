import json

#Bloque que lee el archivo JSON y lo almacena en una lista
file_json = open("Placas.json", "r")
content_json =  file_json.read()
jsondecoded = json.loads(content_json)
lista_Placa_json = []
for plates in jsondecoded ["Automoviles"]:
    placa_auto = plates["Placa"]
    lista_Placa_json.append(placa_auto)
    #print("Placa:", placa_auto)#Imprime cada placa 

print("Lista de placas en JSON: ", lista_Placa_json)

#Bloque que lee el archivo txt y guarda cada linea del texto como un elemento dentro de una lista
lista_Placa_txt = []
with open("Placas.txt") as file_txt:
    rows = file_txt.readlines()
    for row in rows:
        content_txt = file_txt.read()
        lista_Placa_txt.append(row.strip('\n'))

print("Lista de placas en txt: ", lista_Placa_txt)

#Bloque para comparar las dos cadenas
comparacion = [item for item in lista_Placa_json if item in lista_Placa_txt]
if len(comparacion) > 0:
    print('Ambas listas contienen estos elementos ')
    for item in comparacion:
        print('%s' % item)
else:
    print('No existe ningun elemento igual en las listas')
