import json

#Bloque que convierte el JSON en un valor de Python (objeto)
def jsonToPython():
    jsonData = '{"Placa": "CVL 657 18", "Modelo" : "Cruze", "Color": "Rojo"}' #Definimos el objeto JSON.
    json_Python = json.loads (jsonData)#Parsea el objeto JSON mediante método json.loads ()., lo convierte en un diccionario o lista de Python.
    return json_Python   
print("Json to Python:", jsonToPython())

#Bloque que codifica un valor de Python a JSON
def pythonToJson():
    pythonDictionary = {"Placa": "CVL 657 18", "Modelo" : "Cruze", "Color": "Rojo"} #Diccionario Python
    dictionaryToJson = json.dumps(pythonDictionary)#Convierte un objeto Python en una cadena JSON mediante el método json.dumps ().
    return dictionaryToJson
print ("Python to Json:", pythonToJson())