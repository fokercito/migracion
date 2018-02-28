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
        #for j in i:
            #nString=""
            #if (j >= chr(48)) and (j <= chr(57)):
             #   nString += j
            numerosConsulta.append(i.replace("https://www.siass.unam.mx/consulta/",""))
"""


linkstemp=[]
linkstemporales=[]
numerosConsulta=[]
for i in arrlinks:
    print("entre al arrlinks")
    if("https://www.siass.unam.mx/consulta?" in i):
        linkstemp.append(i)
print(linkstemp)
for x in linkstemp:
    linkstemporales.append(x.replace("https://www.siass.unam.mx/consulta?numero_cuenta=311004739&sistema_pertenece=dgae&facultad_id=6&carrera_id=55&page=", ""))
print(linkstemporales)
z = int(linkstemporales[1])
linkstemporales[0] =0
max = 0
for j in linkstemporales:
    if (int(j)>z):
        max = int(j)
    if int(j)>max:
        max = int(j)
print(max)


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