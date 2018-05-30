import json
import pyodbc

'''
data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
'''

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost\SQLEXPRESS02_16;"
                      "Database=PacGenCatalog;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()
#cursor.execute('SELECT * FROM meta.PatternTypes')
#cursor.execute('SELECT name FROM master.sys.databases')
cursor.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'')
for row in cursor:
    print('row = %r' % (row,))
    print('wow')
