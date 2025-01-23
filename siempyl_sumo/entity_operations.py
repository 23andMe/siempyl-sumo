# pylint: disable=E1101
"""
Contains functions used to make entity based requests
    -get_entity() https://api.us2.sumologic.com/docs/sec/#operation/GetEntity
    -get_entities() https://api.us2.sumologic.com/docs/sec/#operation/GetEntities

"""

class EntityOperations:
    """
    EntityOperations class that extends Client

    Contains all the operations dealing with Entities
    """

    def get_entity(self, entity_id: str, expand=False):
        """
        Requests Sumo API for a specific entity given the ID

        Examples:
            client.get_entities("_username-humanp")
            client.get_entities("_hostname-computer", expand=True)

        Notes:
            Dashes in the entity name need to be escaped
            Entity username "human-person" becomes "_username-human--person"

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetEntity
        """

        if not self.validate_entity_type(entity_id):
            raise Exception(f"Invalid entity type: {entity_id}")

        operation = f"entities/{entity_id}?"

        if expand:
            operation += "expand=inventory"

        response_json = self.request_http_get(operation)

        return response_json['data']

    def get_entities(self, query = None, expand = False):
        """
        Requests Sumo API for all entities, or entities matching a query, if given

        Examples:
            client.get_entities(query = 'id:"_username-humanp"')
            client.get_entities(query = 'tag:"Watchlist:VIPs"', expand = True)

        Notes:
            Dashes in the entity name need to be escaped
            Entity "human-person" becomes "_username-human--person"

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetEntities
        """

        operation = "entities"

        returned_data = self.get_paginated_request(operation, query, expand)

        return returned_data
