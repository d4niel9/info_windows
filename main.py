import csv
import json
import os
from datetime import datetime
import time


def info_json_empty():
    info_labels = """
    {
    "Número serie": null,
    "Nombre de host": null,
    "Nombre del sistema operativo": null,
    "Fabricante del sistema operativo": null,  
    "Propiedad de": null,
    "Organización registrada": null,
    
    "Fecha de instalación original": null,
    "Fabricante del sistema": null,
    "Modelo el sistema":null,
    "Tipo de sistema": null,
    "Procesador(es)": null,
    "Versión del BIOS": null,
    "Cantidad total de memoria física":null,
    "Dominio": null,
    "Servidor de inicio de sesión": null
    }
    """
    info_labels = json.loads(info_labels)
    return info_labels


def console_commands():
    try:
        command = "wmic bios get SerialNumber /VALUE"
        response = os.popen(command).read()
        # cleaning response
        response = response.replace("SerialNumber=", '"')
        response = response.replace("\n", "")
        response = '' + response + '",'
        # write response in file csv
        with open("data.csv","w", encoding="utf-8") as f:
            f.writelines(response)
            f.close()
    except Exception as excpt:
        print("*File creation error " + str(excpt))

    try:
        command = "systeminfo /FO CSV /NH"
        response = os.popen(command).read()
        with open("data.csv","a", encoding="utf-8") as f:
            f.writelines(response)
            f.close()
    except Exception as excpt:
        print("*File creation error " + str(excpt))


def read_info_csv():
    try:
        with open('data.csv', "r", encoding="utf-8") as File:  
            reader = csv.reader(File)
            for row in reader:
                lista = row
        return lista
    except FileNotFoundError as err:
        print(err)


def select():
    try:
        lista = read_info_csv()
        new = []
        yes = [0,1,2,4,7,8,10,12,13,14,15,16,23,29,30] #add 9 for "Id. del producto": null,
        i = 0
        for elemento in lista:
            #print(i, elemento)
            if i in yes:
                new.append(elemento)
            i += 1
        return new
    except Exception as err:
        print(err)


def json_file():
    info_labels = info_json_empty()
    data = select()

    # add values from csv to info in json
    i= 0
    for key, value in info_labels.items():
        info_labels[key] = data[i]
        i += 1

    with open('data.json', 'a', encoding="utf-8") as file_json:
        json.dump(info_labels, file_json, ensure_ascii=False, indent=4)
    

def run():

    console_commands()
    json_file()


if __name__ == "__main__":
    run()