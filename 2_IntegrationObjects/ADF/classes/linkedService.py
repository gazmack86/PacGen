class linkedService:

    # Initializer / Instance Attributes
    def __init__(self, name, objectType):
        self.name = name
        self.objectType = objectType





'''{
    "name": "<Name of the linked service>",
    "properties": {
        "type": "<Type of the linked service>",
        "typeProperties": {
              "<data store or compute-specific type properties>"
        },
        "connectVia": {
            "referenceName": "<name of Integration Runtime>",
            "type": "IntegrationRuntimeReference"
        }
    }
}'''
