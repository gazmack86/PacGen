import json
import pyodbc
import os

with open('Y:\Code\PacGen\PacGen\_Config\ImportSource-Connection.json','r') as f_obj:
    connectionAttributes = json.load(f_obj)

cnxn = pyodbc.connect("Driver=" + connectionAttributes['driver'] + ";" +
                      "Server=" + connectionAttributes['instanceName'] + ";" +
                      "Database=" + connectionAttributes['database'] + ";" +
                      "Trusted_Connection=yes;")

with open('Y:\Code\PacGen\PacGen\_Config\Meta-Connection.json','r') as f_obj:
    metaConnectionAttributes = json.load(f_obj)

mcnxn = pyodbc.connect("Driver=" + metaConnectionAttributes['driver'] + ";" +
                      "Server=" + metaConnectionAttributes['instanceName'] + ";" +
                      "Database=" + metaConnectionAttributes['database'] + ";" +
                      "Trusted_Connection=yes;")

tableCursor = cnxn.cursor()
tables = tableCursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE=\'BASE TABLE\'')
tableNames = []
for tableRow in tables:
    tableNames.append(tableRow.TABLE_NAME)

mergeCursor = mcnxn.cursor()
mergeCursor.execute('IF OBJECT_ID(\'tempdb..#ColumnMetaTemp\') IS NOT NULL DROP TABLE #ColumnMetaTemp;')
mergeCursor.execute('SELECT TOP 1 * INTO #ColumnMetaTemp FROM [PacGenCatalog].[meta].[Columns];')
mergeCursor.execute('TRUNCATE TABLE #ColumnMetaTemp;')

columnCursor = cnxn.cursor()
for name in tableNames:
    metaRows = columnCursor.execute('SELECT OBJECT_SCHEMA_NAME(T.object_id) AS [SchemaName]' +
    '    , T.name AS [TableName]' +
    '    , C.name AS [ColumnName]' +
    '    , C.is_identity AS [IsIdentity]' +
    '    , Y.name AS [DataType]' +
    '    , C.is_nullable AS [Nullable]' +
    '    , C.max_length AS [Length]' +
    '    , C.precision AS [precision]' +
    '    , C.scale AS [Scale]' +
    '   , C.collation_name AS [collation]' +
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
        #print(row)
        mergeCursor.execute('INSERT INTO #ColumnMetaTemp (SchemaName, TableName, ColumnName, IsIdentity, DatNullableaType, IsUniqueKey, DataTypeId, StringLength, ) VALUES (1, table__name, column__name, 0, is_identity, 0, data__type, 0,  ...);')


#mergeCursor.execute(
#MERGE Production.ProductInventory AS target
#USING (SELECT ProductID, SUM(OrderQty) FROM Sales.SalesOrderDetail AS sod
#    JOIN Sales.SalesOrderHeader AS soh
#    ON sod.SalesOrderID = soh.SalesOrderID
#    AND soh.OrderDate = @OrderDate
#    GROUP BY ProductID) AS source (ProductID, OrderQty)
#ON (target.ProductID = source.ProductID)
#WHEN MATCHED AND target.Quantity - source.OrderQty <= 0
#    THEN DELETE
#WHEN MATCHED
#    THEN UPDATE SET target.Quantity = target.Quantity - source.OrderQty,
#                    target.ModifiedDate = GETDATE()
#OUTPUT $action, Inserted.ProductID, Inserted.Quantity,
#    Inserted.ModifiedDate, Deleted.ProductID,
#    Deleted.Quantity, Deleted.ModifiedDate;
#)


        #INSERT INTO table_name ([ColumnID]
          #,[ObjectID]
          #,[ObjectName]
          #,[ColumnName]
          #,[IsBusinessKey]
          #,[IsPrimaryKey]
          #,[IsUniqueKey]
          #,[DataTypeID]
          #,[StringLength]
          #,[NumericLenth]
          #,[Scale]
          #,[Precision]
          #,[CustomSQL]
          #,[CustomSSIS])
        #VALUES (value1, value2, value3, ...);)
