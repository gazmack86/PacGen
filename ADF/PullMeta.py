#import json
import pyodbc


database = 'WideWorldImporters'
table = 'SystemParameters'
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost\SQLEXPRESS02_16;"
                      "Database=" + database + ";"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
tables = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")

for tableRow in tables:
    print(tableRow)

for tableRow in tables:
    tableName = tableRow.TABLE_NAME
    metaRows = cursor.execute(
        "SELECT OBJECT_SCHEMA_NAME(T.object_id) AS schema__name " +
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
        "WHERE T.name = '" + tableName + "' ORDER BY C.column_id;"
    )
    print(
        'schema__name, table__name, column__name, is_identity,' +
        ' data__type, is_nullable, max_length, precision, scale'
    )
    for row in metaRows:
        print(row)
    print("\n End List  \n")

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
