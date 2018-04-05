# -*- coding: utf-8 -*-
import bs4 as bs #biblioteca de beautifull soup para web ecraping
import urllib3 #biblioteca para el uso de dominios y extraer el código html de los sitios web
import pandas as pd #biblioteca para insertar tablas y datos en xls, json, sql
import json #biblioteca para trabajar json en python
import xlwt #biblioteca para crear archivos de excel

#9 para electricos
#10 para computacion
#11 para telecomunicaciones

def recolectarrep(noCuenta,idCarrera):
    http=urllib3.PoolManager()
    url='https://www.siass.unam.mx/consulta?numero_cuenta='+noCuenta+'&sistema_pertenece=dgae&facultad_id=11&carrera_id='+idCarrera
    r=http.request('GET',url)
    r.status
    soup=bs.BeautifulSoup(r.data,'html.parser')
    link=soup.find_all('a') #obtenemos todos las etiquetas <a> para obtener los links

    arrlinks=[] # creamos un arreglo para guardar todos lon links en las etiquetas
    for i in link:
        arrlinks.append(i['href']) # guardamos el link de las etiquetas <a> en arraylinks

    linkstemp=[] #guardamos los links que NO dirigen al contenido de descripción d elos servicios sociales
    linkstemporales=[]#guardamos los links de las pestañas que enumeran el contenido de las páginas 1 2 3 4....
    numerosConsulta=[] #guardamos sólo el numero de los links
    for i in arrlinks:
        #print("entre al arrlinks")
        if("https://www.siass.unam.mx/consulta?" in i):
            linkstemp.append(i)
    #print(linkstemp)
    for x in linkstemp:
        linkstemporales.append(x.replace("https://www.siass.unam.mx/consulta?numero_cuenta="+noCuenta+"&sistema_pertenece=dgae&facultad_id=11&carrera_id="+idCarrera+"&page=", ""))#reemplazamos todo el url para obtener solo el número de la página a la que va el link
    #en las siguientes líneas de código determinamos el número de páginas obteniento el mayor en la lista "linkstemporales"
    z = int(linkstemporales[1])
    linkstemporales[0] =0
    max = 0
    for j in linkstemporales:
        if (int(j)>z):
            max = int(j)
        if int(j)>max:
            max = int(j)
    #aquí ya tenemos el numero máximo
    numerosConsulta=[]#aquí guardaremos todos lor número de consulta (es decir los últimos numeros de los links que contienen la descripción de los servicios)
    arregloDic=[] #aquí guardaremos los diccionarios que se generarán en el webscraping
    contenedorxl = pd.ExcelWriter('pruebaexcelxlsx', engine='xlsxwriter')
########################3
    url='https://www.siass.unam.mx/consulta?numero_cuenta='+noCuenta+'&sistema_pertenece=dgae&facultad_id=11&carrera_id='+idCarrera
    r=http.request('GET',url)
    r.status
    soup=bs.BeautifulSoup(r.data,'html.parser')
    link=soup.find_all('a')#obtenemos todas las etiquetas <a> de html
    arrlinks=[]
    for i in link:
        arrlinks.append(i['href']) #obtenemos todos los links en las etiquetas <a>
    
    for i in arrlinks:
        if("https://www.siass.unam.mx/consulta/" in i ):
                numerosConsulta.append(i.replace("https://www.siass.unam.mx/consulta/",""))#obtenemos solo los números

#########################

    for e in range (2,max):#recorremos todas la pestañas de la pagina del siass
        #sobreescribiremos nuestras variables, ya que obtuvimos lo necesario para recorrer la página
        url='https://www.siass.unam.mx/consulta?numero_cuenta='+noCuenta+'&sistema_pertenece=dgae&facultad_id=11&carrera_id='+idCarrera+'&page='+ str(e)
        r=http.request('GET',url)
        r.status
        soup=bs.BeautifulSoup(r.data,'html.parser')
        link=soup.find_all('a')#obtenemos todas las etiquetas <a> de html
        arrlinks=[]
        for i in link:
            arrlinks.append(i['href']) #obtenemos todos los links en las etiquetas <a>
        
        for i in arrlinks:
            if("https://www.siass.unam.mx/consulta/" in i ):
                    numerosConsulta.append(i.replace("https://www.siass.unam.mx/consulta/",""))#obtenemos solo los números
    for r in numerosConsulta:#recorremos la descripción de todos los servicios sociales que nuestro usuario puede ver            
        url2='https://www.siass.unam.mx/consulta/' + str(r)
        r=http.request('GET',url2)
        r.status
        diccionario = {}
        soup=bs.BeautifulSoup(r.data,'html.parser')
        tabla=soup.find_all('tr')
        f=open("diccionario.txt","a",encoding="utf8")#abrimos un archivo para guardar los diccionarios que crearemos para pasar despues a la base de datos
        for i in tabla:#creamos y llenamos un diccionario con el contenido de las tablas
            for a in i.find_all('td'):
                for z in i.find_all('th'):
                    print(" ".join( z.text.split()),"<----------->"," ".join( a.text.split()))
                    llave= " ".join( z.text.split())
                    valor = " ".join( a.text.split())
                    diccionario[llave] = valor
        arregloDic.append(diccionario)
        f.write(str(diccionario) + "\n")
        f.close()        
    toJson = json.dumps(arregloDic)
    dfPrueba = pd.read_json(toJson)

    #Esta parte permite generar archivos de cada una de las carreras

    if idCarrera == '10':
        dfPrueba.to_excel('programascompu.xls', index=False)
    elif idCarrera == '11':
        dfPrueba.to_excel('programastelecom.xls', index=False)
    elif idCarrera == '9':
        dfPrueba.to_excel('programaselectr.xls', index=False)
    contenedorxl.save()
