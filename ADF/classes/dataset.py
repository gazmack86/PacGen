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
