# -*- coding: utf-8 -*-
import bs4 as bs #biblioteca de beautifull soup para web ecraping
import urllib3 #biblioteca para el uso de dominios y extraer el código html de los sitios web
import pandas as pd #biblioteca para insertar tablas y datos en xls, json, sql
import json #biblioteca para trabajar json en python
import xlwt #biblioteca para crear archivos de excel
import re #para permitir el uso de expresiones regulares
from tkinter import * #interfaz grafica
from tkinter.filedialog import * #explorador de archivos
from datetime import date
#9 para electricos
#10 para computacion
#11 para telecomunicaciones

class main:
    def __init__(self,master):
    	# Window 
        self.master = master
        # Some Usefull variables
        self.numCta = StringVar()
        self.carrera = StringVar()
        self.capturaCarrera = StringVar()
        #Create Widgets
        self.widgets()

    def widgets(self):
        self.logf = Frame(self.master,padx =10,pady = 10)
        Label(self.logf,text = 'Numero de cuenta: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.numCta,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Carrera: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        opciones = ["Computacion","Electrica","Telecom"]
        OptionMenu(self.logf,self.capturaCarrera,*opciones).grid(row=1,column=1)
        #Entry(self.logf,textvariable = self.carrera,).grid(row=1,column=1)
        Button(self.logf,text = ' Realizar Scraping ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.recolectarrep).grid(columnspan=2)
        Label(self.logf,text = 'Instrucciones: \n1)Ingresa un numero de cuenta valido\n 2)Selecciona una carrera\n 3)Al dar click se solicitara la carpeta donde quieras el archivo de excel',font = ('',9),pady=5,padx=5).grid(columnspan=2)
        self.logf.pack()
    
    def recolectarrep(self):
        localtime = str(date.today())
        urllib3.disable_warnings()
        if self.capturaCarrera.get() == "Computacion":
            self.carrera.set('10')
        elif self.capturaCarrera.get() == "Electrica":
            self.carrera.set('9')
        elif self.capturaCarrera.get() == "Telecom":
            self.carrera.set('11')
        rutadeldirectorio= askdirectory()
        http=urllib3.PoolManager()
        url='https://www.siass.unam.mx/consulta?numero_cuenta='+str(self.numCta.get())+'&sistema_pertenece=dgae&facultad_id=11&carrera_id='+str(self.carrera.get())
        r=http.request('GET',url)
        r.status
        soup=bs.BeautifulSoup(r.data,'html.parser')
        link=soup.find_all('a') #obtenemos todos las etiquetas <a> para obtener los links
        arrlinks=[] # creamos un arreglo para guardar todos lon links en las etiquetas
        for i in link:
            arrlinks.append(i['href']) # guardamos el link de las etiquetas <a> en arraylinks
        linkstemp=[] #guardamos los links que NO dirigen al contenido de descripción de los servicios sociales
        linkstemporales=[]#guardamos los links de las pestañas que enumeran el contenido de las páginas 1 2 3 4....
        numerosConsulta=[] #guardamos sólo el numero de los links
        for i in arrlinks:
            if("&page=" in i):
                linkstemp.append(i)
        
        for x in linkstemp:
            linkstemporales.append(x.replace("http://www.siass.unam.mx/consulta?numero_cuenta="+self.numCta.get()+"&sistema_pertenece=dgae&facultad_id=11&carrera_id="+self.carrera.get()+"&page=", ""))#reemplazamos todo el url para obtener solo el número de la página a la que va el link
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
        for e in range (2,max):#recorremos todas la pestañas de la pagina del siass
            #sobreescribiremos nuestras variables, ya que obtuvimos lo necesario para recorrer la página
            url='https://www.siass.unam.mx/consulta?numero_cuenta='+self.numCta.get()+'&sistema_pertenece=dgae&facultad_id=11&carrera_id='+self.carrera.get()+'&page='+ str(e)
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
            links = soup.find_all('li')#encuentra todas las etiquetas li
            divs = soup.find_all("div",{"id":re.compile('carrera_*')})#todas la etiquetas con un id que inicie con carrera
            dias = soup.find_all('label', {"class":"btn btn-success disabled"})#saca los dias y los turnos del servicio social
            tablaActividades = soup.find_all('table',{ "class":"table table-striped table-bordered"})#actividades de servicio social
            for a in dias:
                diccionario[a.text.replace(" ","").replace("\n","")]="x" # obtenemos los dias que se laboran en el servicio social y quitamos los espacios y saltos de linea
            for i in links:
                for a in i.find_all('a',href = re.compile('#carrera_*')):#obtenemos todas las etiquetas d ela carrera
                    for j in divs:
                        for b in j.find_all('p',{"class":"alert alert-info"}):#otenemos el texto de las etiquetas que tienen la carrera
                            diccionario[(a.text.replace("  ","").replace("\n",""))] = (b.text.replace("  ","").replace("\n",""))#crea un elemento del diccionario con el contenido de la etiqueta de la carrera y la etiqueta que contiene los prestadores
                        for b in tablaActividades:#iniciamos a leer las actividades
                            columna = b.find_all('td',{"style":"padding-left: 20px;"})#extraemos solo la tabla de actividades de cada carrera
                            texto = ""
                            for c in columna:
                                texto = texto + c.text.replace("  ","").replace("\n\n","") 
                                diccionario["Actividad " +(a.text.replace("  ","").replace("\n",""))] = texto
            for i in tabla:#creamos y llenamos un diccionario con el contenido de las tablas
                for a in i.find_all('td'):
                    for z in i.find_all('th'):
                        llave= " ".join( z.text.split())
                        valor = " ".join( a.text.split())
                        if llave in diccionario:
                            diccionario[llave+" jefe directo"]=valor
                        else:
                            diccionario[llave] = valor
            arregloDic.append(diccionario)
            f.write(str(diccionario) + "\n")
            f.close()        
        toJson = json.dumps(arregloDic)
        dfPrueba = pd.read_json(toJson)
        #Esta parte permite generar archivos de cada una de las carreras
        if self.carrera.get() == "10":
            dfPrueba.to_excel( rutadeldirectorio+'/programascompu'+ localtime+'.xls', index=False)
        elif self.carrera.get() == '11':
            dfPrueba.to_excel( rutadeldirectorio+'/programastelecom'+localtime +'.xls', index=False)
        elif self.carrera.get() == '9':
            dfPrueba.to_excel( rutadeldirectorio+'/programaselectr'+localtime+'.xls', index=False)
        contenedorxl.save()


if __name__ == '__main__':
	#Create Object
	#and setup window
    root = Tk()
    root.title('Scraping a SIASS')
    root.geometry('500x350+300+300')
    main(root)
    root.mainloop()