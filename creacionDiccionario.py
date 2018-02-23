import bs4 as bs
import urllib3
import pandas as pd
http=urllib3.PoolManager()
url='https://www.siass.unam.mx/consulta/494290'
r=http.request('GET',url)
r.status
diccionario = {}
soup=bs.BeautifulSoup(r.data,'html.parser')
tabla=soup.find_all('tr')
for i in tabla:
    for a in i.find_all('td'):
        for z in i.find_all('th'):
            print(" ".join( z.text.split()),"<----------->"," ".join( a.text.split()))
            llave= " ".join( z.text.split())
            valor = " ".join( a.text.split())
            diccionario[llave] = valor
            
print("<============Diccionario=============>")
print(diccionario)  