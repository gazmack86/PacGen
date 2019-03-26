import pyodbc
import json
import os


#prompt the user for a file to import
filename = r'Y:\Code\PacGen\PacGen\_Config\Meta-Connection.json'
dirname = os.path.dirname(filename)
if not os.path.exists(dirname):
    os.makedirs(dirname)


with open(filename, 'r') as f:
    Connections = json.load(f)

#if connection['ConnectionType'] = 'Metadata'

MetadataConnections = (connection for connection in Connections if connection['ConnectionType'] == 'Metadata')
for MetadataConnection in MetadataConnections:
    conn = pyodbc.connect('Driver=' + MetadataConnection['Driver'] + ';'
                            'Server=' + MetadataConnection['Server'] + ';'
                            'Database=' + MetadataConnection['Database'] + ';'
                            'Trusted_Connection=' + MetadataConnection['TrustedConnection'] + ';')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [PacGenCatalog].[meta].[ColumnRelationships]')

    for row in cursor:
        print(row)
