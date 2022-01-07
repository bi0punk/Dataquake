from datetime import MINYEAR
from flask import Flask, render_template, request, redirect, url_for, flash
from matplotlib.figure import Figure
from flask_mysqldb import MySQL
from folium.map import Popup
from io import BytesIO
from typing import Text
import pandas as pd 
import requests
import base64
import json
import bs4
import re
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io




import folium

app = Flask(__name__)

#conexion base da datos
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
mysql = MySQL(app)


app.secret_key = "mysecretkey"


# ~ @app.route('/')
# ~ def Index():
    # ~ cur = mysql.connection.cursor()
    # ~ cur.execute('SELECT * FROM sismos')
    # ~ data = cur.fetchall()
    # ~ print(data)
    # ~ cur.close()
    # ~ return render_template('index.html', sismo = data)



@app.route("/")
def sismos():
    img = io.BytesIO()
    cabezeras= []
    fuente_dat = 'http://www.sismologia.cl/ultimos_sismos.html'
    page = requests.get(fuente_dat)
    sopa = bs4.BeautifulSoup(page.text, 'lxml')
    tabla = sopa.find('table')
    

    for i in tabla.find_all('th'):
        title = i.text.strip()
        cabezeras.append(title)
        df = pd.DataFrame(columns = cabezeras )
        

    for filas in tabla.find_all('tr')[1:]:
        info = filas.find_all('td')
        filas_info = [td.text.strip() for td in info]
        length = len(df)
        df.loc[length] = filas_info

    #nombres de lugares sismos dashboard
    ref_geo = (df['Referencia GeogrÃ¡fica'])
    lug_ult_reg = (df['Referencia GeogrÃ¡fica'][0]) 

    
    """ Convertimos algunos elemeneyos del dataframe a numeros para operar con ellos
    ya que estan como string """


    df['Latitud'] = df['Latitud'].astype(float)
    df['Longitud'] = df['Longitud'].astype(float)
    df['Profundidad [Km]'] = df['Profundidad [Km]'].astype(float)

    print(df)



    """ convertimos columna magnitud a lista, para poder obtener solo  numeros flotantes
    ya que muestra en la tabla tiene el siguiente formato 3.2 Ml """



    max_mag_list = df["Magnitud"].tolist() 
    flotantes = [float(re.findall("\d+\.\d+", i)[0]) for i in max_mag_list]    #usando expresiones regulares, obtenemos float
    flotantes.sort()



    #  LOGICA ULTIMO REGISTRADO #


    ult_sis = ''
    ult_sis = max_mag_list[0]                     

    #  LOGICA MENOS PROFUNDO #
    
    min_prof = ''
    min_prof = df['Profundidad [Km]'].min()

    km = 'Kilómetros'

    #  LOGICA MAGNITUD MAS BAJA #
    min_reg = ''
    min_reg = flotantes[0]

    #  LOGICA MAGNITUD MAS ALTA #
    max_reg= ''
    max_reg = flotantes[-1]

    
   
    # ciclo if para determinar unidad de medidad depediendo de magntiud del sismo
    
    if max_reg >= 6.0:
        magnitud = 'Mw'   #Magnitud de momento
    else:
        magnitud = 'Ml'   #Magnitud local
    
    
    max_reg_unit = (str(max_reg) + ' ' + magnitud)
    min_reg_unit = (str(min_reg) + ' ' + magnitud)



    map = folium.Map(location=[-34.007, -70.307],popup = 'Epicentro' ,tiles="Stamen Terrain", zoom_start=10)
    

    return render_template('index.html',
    
    map=map._repr_html_(),
    ult_sis = ult_sis,
    lug_ult_reg = lug_ult_reg , 
    min_prof  = min_prof, 
    min_reg_unit = min_reg_unit,
    max_reg_unit = max_reg_unit,



    tables=[df.to_html(classes='data', header="false")])

    








if __name__=="__main__":
    app.run(debug=True)


""" print(min_prof)  """



""" transformamos columna magnitud a lista para poder quitar cadenas """