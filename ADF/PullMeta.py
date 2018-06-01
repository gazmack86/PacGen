import json
import pyodbc
import os

absolute_path = os.path.dirname(os.path.abspath(__file__))
file_path = 'Y:\Code\PacGen\PacGen\_Config\ImportSource-Connection.json'
with open(file_path,'r') as f_obj:
    connectionAttributes = json.load(f_obj)

cnxn = pyodbc.connect("Driver=" + connectionAttributes['driver'] + ";" +
                      "Server=" + connectionAttributes['instanceName'] + ";" +
                      "Database=" + connectionAttributes['database'] + ";" +
                      "Trusted_Connection=yes;")

tableCursor = cnxn.cursor()
tables = tableCursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
tableNames = []
for tableRow in tables:
    tableNames.append(tableRow.TABLE_NAME)

mergeCursor = cnxn.cursor()
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
        print(row)
