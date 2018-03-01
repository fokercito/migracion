import bs4 as bs
import urllib3
import pandas as pd
http=urllib3.PoolManager()
url='https://www.siass.unam.mx/consulta?numero_cuenta=311004739&sistema_pertenece=dgae&facultad_id=6&carrera_id=55'
r=http.request('GET',url)
r.status
soup=bs.BeautifulSoup(r.data,'html.parser')
link=soup.find_all('a')

arrlinks=[]
for i in link:
    arrlinks.append(i['href'])
"""
manda una lista de todos los numeros d elos links
print(arrlinks)
numerosConsulta=[]
for i in arrlinks:
    if("https://www.siass.unam.mx/consulta/" in i ):
            numerosConsulta.append(i.replace("https://www.siass.unam.mx/consulta/",""))
"""


linkstemp=[]
linkstemporales=[]
numerosConsulta=[]
for i in arrlinks:
    #print("entre al arrlinks")
    if("https://www.siass.unam.mx/consulta?" in i):
        linkstemp.append(i)
#print(linkstemp)
for x in linkstemp:
    linkstemporales.append(x.replace("https://www.siass.unam.mx/consulta?numero_cuenta=311004739&sistema_pertenece=dgae&facultad_id=6&carrera_id=55&page=", ""))
#print(linkstemporales)
z = int(linkstemporales[1])
linkstemporales[0] =0
max = 0
for j in linkstemporales:
    if (int(j)>z):
        max = int(j)
    if int(j)>max:
        max = int(j)
#print(max)
numerosConsulta=[]
arregloDic=[]
for e in range (2,max):
    url='https://www.siass.unam.mx/consulta?numero_cuenta=311004739&sistema_pertenece=dgae&facultad_id=6&carrera_id=55&page='+ str(e)
    r=http.request('GET',url)
    r.status
    soup=bs.BeautifulSoup(r.data,'html.parser')
    link=soup.find_all('a')

    arrlinks=[]
    for i in link:
        arrlinks.append(i['href'])
    
    for i in arrlinks:
        if("https://www.siass.unam.mx/consulta/" in i ):
                numerosConsulta.append(i.replace("https://www.siass.unam.mx/consulta/",""))

    for r in numerosConsulta:            
        url2='https://www.siass.unam.mx/consulta/' + r
        r=http.request('GET',url2)
        r.status
        diccionario = {}
        soup=bs.BeautifulSoup(r.data,'html.parser')
        tabla=soup.find_all('tr')
        f=open("diccionario.txt","w")
        for i in tabla:
            for a in i.find_all('td'):
                for z in i.find_all('th'):
                    print(" ".join( z.text.split()),"<----------->"," ".join( a.text.split()))
                    llave= " ".join( z.text.split())
                    valor = " ".join( a.text.split())
                    diccionario[llave] = valor
        arregloDic.append(diccionario)
        f.write(str(diccionario) + "\n")
        f.close()        
print(arregloDic)
f=open("listadiccionario.txt","a")
f.write(arregloDic)
f.close()
#print(numerosConsulta)


"""
intento de recorrer la pagina
        url= i
        r=http.request('GET',url)
        r.status
        soup=bs.BeautifulSoup(r.data,'html.parser')
        linkstemp=soup.find_all('a')
        for i in linkstemp:
            linkstemporales.append(i['href'])
        for j in linkstemporales:
            print("entre al ciclo de link temporal")
            if("https://www.siass.unam.mx/consulta/" in j ):  
                print("encontre un numero de consulta")
                numerosConsulta.append(i.replace("https://www.siass.unam.mx/consulta/","")
print(numerosConsulta)
#print(len(numerosConsulta))
#print(numerosConsulta)

"""