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
print(arrlinks)
numerosConsulta=[]
for i in arrlinks:
    if("https://www.siass.unam.mx/consulta/" in i ):
        #for j in i:
            #nString=""
            #if (j >= chr(48)) and (j <= chr(57)):
             #   nString += j
        numerosConsulta.append(i)
print(len(numerosConsulta))
print(numerosConsulta)