# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import bs4 as bs
import pandas as pd #biblioteca para insertar tablas y datos en xls, json, sql
import json #biblioteca para trabajar json en python
import xlwt
import csv
import re
arregloDic=[]
# permite crear una lista de todos los archivos en la carpeta que se ejecute el script
def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
arregloArchivos = ls()
for archivo in arregloArchivos:
    with open(archivo, "r", encoding="utf8") as f:
        contents = f.read()
        soup = bs.BeautifulSoup(contents ,'html.parser')
        tabla = soup.find_all('tr')
        diccionario = {}
        links = soup.find_all('li')#encuentra todas las etiquetas li
        divs = soup.find_all("div",{"id":re.compile('carrera_*')})#todas la etiquetas con un id que inicie con carrera
        dias = soup.find_all('label', {"class":"btn btn-success disabled"})#saca los dias y los turnos del servicio social
        tablaActividades = soup.find_all('table',{ "class":"table table-striped table-bordered"})#actividades de servicio social
        for a in dias:
            diccionario[a.text.replace(" ","").replace("\n","")]="x"
        for i in links:
            for a in i.find_all('a',href = re.compile('#carrera_*')):
                for j in divs:
                    for b in j.find_all('p',{"class":"alert alert-info"}):
                        diccionario[(a.text.replace("  ","").replace("\n",""))] = (b.text.replace("  ","").replace("\n",""))#crea un elemento del diccionario con el contenido de la etiqueta de la carrera y la etiqueta que contiene los prestadores
                    for b in tablaActividades:#iniciamos a leer las actividades
                        columna = b.find_all('td',{"style":"padding-left: 20px;"})
                        texto = ""
                        for c in columna:
                            texto = texto + c.text.replace("  ","").replace("\n\n","") 
                            diccionario["Actividad " +(a.text.replace("  ","").replace("\n",""))] = texto
                        
        for i in tabla:#creamos y llenamos un diccionario con el contenido de las tablas
            for a in i.find_all('td'):
                for z in i.find_all('th'):
                    print(" ".join( z.text.split()),"<----------->"," ".join( a.text.split()))
                    llave= " ".join( z.text.split())
                    valor = " ".join( a.text.split())
                    if llave in diccionario:
                        diccionario[llave+"2"]=valor
                    else:
                        diccionario[llave] = valor
            #print(diccionario)
        arregloDic.append(diccionario)
toJson = json.dumps(arregloDic)
dfPrueba = pd.read_json(toJson)
dfPrueba.to_excel('servicios.xls', index=False)