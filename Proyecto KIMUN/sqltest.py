# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import pyodbc

server = 'servidorkimun.database.windows.net'
database = 'KimunDase_2018-12-14T03 -37Z'
username = 'Marcela'
password = 'Adelina1988'
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
