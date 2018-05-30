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

#test location
'''
with open("data_file.json", "r") as jsonFile:
data = json.load(jsonFile)

tmp = data["location"]
data["location"] = "NewPath"

with open("replayScript.json", "w") as jsonFile:
    json.dump(data, jsonFile)
'''


print('success')
