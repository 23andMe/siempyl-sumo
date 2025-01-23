"""
Example for usage

Ensure you've installed the library with PIP
pip3 install git+https://github.com/23andMe/siempyl-sumo
"""
import os
from siempyl_sumo import Client

#Change this if you are in a different region
#Regions: us1, us2, au, jp, in, eu, de, ca, fed
API_REGION = "us2"

#Will read the environmental variables and save the contents as a global variable
ACCESS_ID = os.environ['ACCESS_ID']
ACCESS_KEY = os.environ['ACCESS_KEY']

#Create API client with ID, key, and region
CLIENT = Client(
    ACCESS_ID,
    ACCESS_KEY,
    API_REGION)

def get_entity_example():
    """
    Use get_entity() to return a single record
    You can specify if you want to expand inventory
    Don't forget to escape the dash if it is found in the entity name
    E.g., entity username 'human-person' becomes '_username-human--person'
    """

    username = "humanp" #Change this to return another entity
    entity_type = "_username" #Change this to return another type

    entity = CLIENT.get_entity(f"{entity_type}-{username}") #CLIENT.get_entitiy("_username-humanp")
    entity = CLIENT.get_entity(f"{entity_type}-{username}", expand=True)

    #Prints the name of the entity as stored in SIEM
    print(entity['name'])

    #Prints the employee ID found in inventory
    #Inventory is only returned if 'expand' is True
    print(entity['name']['inventory'][0]['metadata']['profile']['employeeNumber'])

def get_entities_example():
    """
    Use get_entities() to return a multiple records
    You can specify if you want to expand inventory
    You should provide a query
    Don't forget to escape the dash if it is found in the entity name
    E.g., entity username 'human-person' becomes '_username-human--person'
    """

    #Returns a single record that matches an ID query
    username = "humanp" #Change this to return another entity
    entity_type = "_username" #Change this to return another type
    entities = CLIENT.get_entities(query=f'id:"{entity_type}-{username}"') #CLIENT.get_entitiy(query="id:_username-humanp")
    print(entities)

    #Returns multiple records that matches a tag query
    watchlist = "Watchlist:Engineers"
    entities = CLIENT.get_entities(query=f'tag:"{watchlist}"', expand=True) #CLIENT.get_entitiy(query="tag:Watchlist:Engineers")
    print(entities)
