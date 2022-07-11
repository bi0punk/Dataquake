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

@app.route("/")
def sismos():

    table_MN = pd.read_html('http://www.sismologia.cl/index.html')

    print(table_MN)