import pandas as pd

g=open("diccionario.txt","r",encoding="utf8")
#Desde aqui haremos la migracion del diccionario a la tabla con pandas

contenedor = pd.ExcelWriter("contenedorprueba.xlsx",engine="xlsxwriter")

for linea in g.readlines():
    linea.to_excel(contenedor,sheet_name="Hoja1")
g.close()
contenedor.save()