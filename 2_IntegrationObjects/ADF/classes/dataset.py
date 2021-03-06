from enum import Enum
class objectType(Enum):
     File = 1
     Table = 2
     AzureBlob = 3

class Dataset:

    # Initializer / Instance Attributes
    def __init__(self, name, objectType):
        self.name = name
        self.objectType = objectType


class linkedService:

    # Initializer / Instance Attributes
    def __init__(self, name, objectType):
        self.name = name
        self.objectType = objectType


class typeProperties:

    # Initializer / Instance Attributes
    def __init__(self, folderPath, Filename):
        self.folderPath = folderPath
        self.Filename = Filename

class format:

    # Initializer / Instance Attributes
    def __init__(self, type, NestedSeperator):
        self.type = type
        self.NestedSeperator = NestedSeperator


'''
{
"name": "MyDataset",
"properties": {
"type": "AzureBlob",
	"linkedService": {
		"referenceName": "StorageLinkedService",
		"type": "LinkedServiceReference"
	},
	"typeProperties": {
		"folderPath":"container/folder",
		"Filename": "file.json",
		"format":{
			"type":"JsonFormat"
			"nestedSeperator": ","
		}
	}
}}

{
    "name": "<name of dataset>",
    "properties": {
        "type": "<type of dataset: AzureBlob, AzureSql etc...>",
        "linkedServiceName": {
                "referenceName": "<name of linked service>",
                 "type": "LinkedServiceReference",
        },
        "structure": [
            {
                "name": "<Name of the column>",
                "type": "<Name of the type>"
            }
        ],
        "typeProperties": {
            "<type specific property>": "<value>",
            "<type specific property 2>": "<value 2>",
        }
    }
}
'''
# Instantiate the Dog object
philo = Dataset("Philo", ObjectType.File)
mikey = DoDatasetg("Mikey", ObjectType.AzureBlob)

# Access the instance attributes
#print("{} is {} and {} is {}.".format(
#    philo.name, philo.age, mikey.name, mikey.age))

# Is Philo a mammal?
#if philo.species == "mammal":
#    print("{0} is a {1}!".format(philo.name, philo.species))

'''
For columns in ADF

name:	Name of the column.
type:	allowed values: Int16, Int32, Int64, Single, Double, Decimal, Byte[],
Boolean, String, Guid, Datetime, Datetimeoffset, and Timespan
culture:	.NET-based culture to be used when the type is a .NET type: Datetime or Datetimeoffset.
The default is en-us
format	Format string to be used when the type is a .NET type: Datetime or Datetimeoffset.
Refer to Custom Date and Time Format Strings on how to format datetime.
'''

'''
import json
import shutil

data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)

shutil.move("data_file.json", "JSON\data_file.json")

print('success')
'''
