import json
import pyodbc
import os

absolute_path = os.path.dirname(os.path.abspath(__file__))
file_path = 'Y:\Code\PacGen\PacGen\_Config\SourceConnection.json'
with open(file_path,'r') as f_obj:
    connectionAttributes = json.load(f_obj)

#database = 'WideWorldImporters'
#table = 'SystemParameters'
#instanceName = 'localhost\SQLEXPRESS02_16'
#driver = '{SQL Server Native Client 11.0}'

print(connectionAttributes['driver'])
