import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
from time import time
import pyodbc
import os
import tables
import time
from azure.storage.blob import BlobService
import urllib2
import json

absolute_path = os.path.dirname(os.path.abspath(__file__))
file_path = 'Y:\Code\PacGen\PacGen\_Config\ImportPolybaseMeta-Connection.json'
with open(file_path,'r') as f_obj:
    connectionAttributes = json.load(f_obj)


#Initialize database parameters (CHANGE THIS)
SERVER_NAME   = 'ENTER SERVER_NAME'
DATABASE_NAME = 'ENTER SQLDW DATABASE NAME'
USERID        = 'ENTER DB USERID'
PASSWORD      = 'ENTER DB PASSWORD'
DB_DRIVER     = 'SQL Server Native Client 11.0'

# Specify the Azure Storage Account name where you will have a private blob to copy in the CSV file
STORAGEACCOUNTNAME = "ENTER AZURE STORAGE ACCOUNT NAME"
# Sepcify the storage account key.
# You can retrieve it "Primary Access Key" found on Azure portal Storage account blade by clicking on the "Key" icon.
# More info: https://azure.microsoft.com/en-us/documentation/articles/storage-create-storage-account/#manage-your-storage-access-keys
STORAGEKEY = "ENTER STORAGE ACCOUNT KEY "
#Read dataset
#Dataset is read from a public blob and copied to a private blob to locad it into SQL DW via Polybase

f = urllib2.urlopen('https://cahandson.blob.core.windows.net/nyctaxi/nyctaxipoint1pct.csv')
taxisample = f.read()
blob_service = BlobService(account_name=STORAGEACCOUNTNAME, account_key=STORAGEKEY)
blob_service.create_container('nyctaxinb')
blob_service.put_block_blob_from_bytes(
    'nyctaxinb',
    'nyctaxipoint1pct.csv',
    taxisample
)

# Construct the SQL DW Connection string
driver = 'DRIVER={' + DB_DRIVER + '}'
server = 'SERVER=' + SERVER_NAME
database = 'DATABASE=' + DATABASE_NAME
uid = 'UID=' + USERID
pwd = 'PWD=' + PASSWORD
CONNECTION_STRING = ';'.join([driver,server,database,uid,pwd, 'Encrypt=yes;TrustServerCertificate=no'])
print CONNECTION_STRING

# Connect to the Database. Autocommit needs to turned on for DDL statements
conn = pyodbc.connect(CONNECTION_STRING)
conn.autocommit=True
cursor = conn.cursor()

# Create Schema
q_sch = '''CREATE SCHEMA nyctaxinb'''

q_dbsc_tpl = '''
CREATE DATABASE SCOPED CREDENTIAL AzureStorageCredential
WITH IDENTITY = 'user' ,
Secret = '%s'
'''

q_extds_tpl = '''
CREATE EXTERNAL DATA SOURCE nyctaxi_nb_storage
WITH
(
    TYPE = HADOOP,
    LOCATION ='wasbs://nyctaxinb@%s.blob.core.windows.net',
    CREDENTIAL = AzureStorageCredential
)
'''

q_extff = '''
CREATE EXTERNAL FILE FORMAT nyctaxi_ff
WITH
(
    FORMAT_TYPE = DELIMITEDTEXT,
    FORMAT_OPTIONS
    (
        FIELD_TERMINATOR =',',
        DATE_FORMAT = 'MM/dd/yyyy hh:mm:ss tt',
        USE_TYPE_DEFAULT = TRUE
    )
)
'''

q_exttab = '''
CREATE EXTERNAL TABLE external_nyctaxi_nb
(
    medallion varchar(50) not null,
    hack_license varchar(50) not null,
    vendor_id char(3),
    rate_code char(3),
    store_and_fwd_flag char(3),
    pickup_datetime datetime not null,
    dropoff_datetime datetime not null,
    passenger_count int,
    trip_time_in_secs bigint,
    trip_distance float,
    pickup_longitude varchar(30),
    pickup_latitude varchar(30),
    dropoff_longitude varchar(30),
    dropoff_latitude varchar(30),
    payment_type char(3),
    fare_amount float,
    surcharge float,
    mta_tax float,
    tolls_amount float,
    total_amount float,
    tip_amount float,
    tipped int,
    tip_class int
)
with (
    LOCATION    = '.',
    DATA_SOURCE = nyctaxi_nb_storage,
    FILE_FORMAT = nyctaxi_ff,
    REJECT_TYPE = VALUE,
    REJECT_VALUE = 12
)
'''

q_createtab = '''
CREATE TABLE nyctaxinb.nyctaxi
WITH
(
    CLUSTERED COLUMNSTORE INDEX,
    DISTRIBUTION = HASH(medallion)
)
AS
SELECT *
FROM   external_nyctaxi_nb
'''
q_dbsc = q_dbsc_tpl % (STORAGEKEY)
q_extds = q_extds_tpl % (STORAGEACCOUNTNAME)
#cursor.execute(q_sch)
#cursor.commit()
print q_sch
print q_dbsc
print q_extds
print q_extff
print q_exttab
print q_createtab

#Now execute the queries constructed above

cursor.execute(q_sch)

cursor.execute(q_dbsc)

cursor.execute(q_extds)

cursor.execute(q_extff)

cursor.execute(q_exttab)

cursor.execute(q_createtab)

#Verify the data is loaded

cursor.close()
pd.read_sql('select top 10 * from nyctaxinb.nyctaxi',conn)
