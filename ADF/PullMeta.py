import json
import pyodbc
import os


script_dir = os.path.dirname('Y:/Code/PacGen/PacGen/_Config/') #<-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, 'SourceConnection.json')
with open(abs_file_path) as f:
    connectionAttributes = json.load(f)

database = 'WideWorldImporters'
table = 'SystemParameters'
instanceName = 'localhost\SQLEXPRESS02_16'
driver = '{SQL Server Native Client 11.0}'

cnxn = pyodbc.connect("Driver=" + connectionAttributes.driver + ";"
                      "Server=" + connectionAttributes.instanceName + ";"
                      "Database=" + connectionAttributes.database + ";"
                      "Trusted_Connection=yes;")
tableCursor = cnxn.cursor()
tables = tableCursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
tableNames = []
for tableRow in tables:
    tableNames.append(tableRow.TABLE_NAME)

columnCursor = cnxn.cursor()
for name in tableNames:
    metaRows = columnCursor.execute("SELECT OBJECT_SCHEMA_NAME(T.object_id) AS schema__name " +
    "    , T.name AS table__name " +
    "    , C.name AS column__name " +
    "    , C.is_identity " +
    "    , Y.name AS data__type " +
    "    , C.is_nullable " +
    "    , C.max_length " +
    "    , C.precision " +
    "    , C.scale " +
    ", C.collation_name " +
    "FROM sys.tables T INNER JOIN sys.columns C " +
    "ON T.object_id = C.object_id " +
    "INNER JOIN sys.types Y " +
    "ON C.system_type_id = Y.system_type_id " +
    "AND C.user_type_id = Y.user_type_id " +
    "WHERE T.name = '" + name + "' ORDER BY C.column_id;")
    print(
        'schema__name, table__name, column__name, is_identity,' +
        ' data__type, is_nullable, max_length, precision, scale')
    for row in metaRows:
        #print(row.column__name + ', ' + row.data__type + ' \n')
        print(row)

#    print(row.TABLE_NAME, end='\n', flush=True)
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
