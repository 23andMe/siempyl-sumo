# pylint: disable=E1101
"""
Contains functions used to make tag based requests
    -get_match_list_by_id() https://api.us2.sumologic.com/docs/sec/#operation/GetMatchList
    -get_match_lists() https://api.us2.sumologic.com/docs/sec/#operation/GetMatchLists
    -get_match_list_by_name() Uses GetMatchLists but returns single match list
    -update_match_list() https://api.us2.sumologic.com/docs/sec/#operation/UpdateMatchList
    -create_match_list() https://api.us2.sumologic.com/docs/sec/#operation/CreateMatchList
    -delete_match_list() https://api.us2.sumologic.com/docs/sec/#operation/DeleteMatchList
    -get_match_list_item() https://api.us2.sumologic.com/docs/sec/#operation/GetMatchListItem
    -get_match_list_items() https://api.us2.sumologic.com/docs/sec/#operation/GetMatchListItems
    -update_match_list_item() https://api.us2.sumologic.com/docs/sec/#operation/UpdateMatchListItem
    -delete_match_list_item() https://api.us2.sumologic.com/docs/sec/#operation/DeleteMatchListItem
    -get_match_list_item_by_id_manual() the function that no one ased for
"""

import hashlib
from . import errors

class MatchListOperations:
    """
    EntityOperations class that contains all the operations dealing with Match Lists
    """

    def get_match_list_by_id(
        self,
        match_list_id: int
    ):
        """
        Gets a single match list by ID.

        Examples:
            client.get_match_list_by_id(69)

        Notes:
            get_match_lists() or get_match_list_by_name() can be used if you don't know the ID

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetMatchList
        """

        operation = f"match-lists/{match_list_id}"

        response_json = self.request_http_get(operation)

        return response_json['data']

    def get_match_lists(self):
        """
        Gets all match lists.

        Examples:
            client.get_match_lists()

        Notes:


        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetMatchLists
        """

        operation = "match-lists"

        returned_data = self.get_paginated_request(operation)

        return returned_data

    def get_match_list_by_name(
        self,
        match_list_name: str
    ):
        """
        A less efficient way to return a single match list.
        Will use get_match_lists() to get all match lists and
        only return the one matching the provided name.

        Examples:
            client.get_match_list_by_name("My Match List")

        Notes:


        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetMatchLists
        """

        match_lists = self.get_match_lists()

        for match_list in match_lists:
            if match_list['name'] == match_list_name:
                return match_list

        raise errors.MatchListNotFound(f"Match list '{match_list_name}' was not found")

    def update_match_list(
        self,
        match_list_id: int,
        description: str,
        default_ttl: int = None,
        active: bool = None
    ):
        """
        Updates the provided match list with, at minimum a description.
        TTL and active are optional fields.

        Examples:
            client.update_match_list(69, "New Description here")
            client.update_match_list(69, "New Description", 0, True)

        Notes:


        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateMatchList
        """

        payload = {

            "fields": {
                "description": description,
                "defaultTtl": default_ttl,
                "active": active
                }
            }

        operation = f"match-lists/{match_list_id}"

        response_json = self.request_http_put(operation, payload)

        return response_json['data']

    def create_match_list(
        self,
        match_list_name,
        target_column,
        description = None,
        default_ttl = None,
        active = None
    ):
        """
        Updates the provided match list with, at minimum a name and target column.
        Description, TTL and active are optional fields.

        Examples:
            client.create_match_list("My new match list", "Username")
            client.create_match_list("My new match list", "Username", "Description")

        Notes:
            The default Target Columns are:
                Hostname, File Hash, URL, Domain, Username, IP Address,
                IP ASN, IP ISP, IP Organization, Source IP Address,
                Source IP ASN, Source IP ISP, Source IP Organization,
                Destination IP Address, Destination IP ASN,
                Destination IP ISP, Destination IP Organization

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/CreateMatchList
        """

        payload = {
            "fields": {
                "name": match_list_name,
                "description": description,
                "targetColumn": target_column,
                "defaultTtl": default_ttl,
                "active": active
                }
            }

        operation = "match-lists"

        response_json = self.request_http_post(operation, payload)

        return response_json

    def delete_match_list(
        self,
        match_list_id: int
    ):
        """
        Deletes the provided match list.

        Examples:
            client.delete_match_list(69)

        Notes:

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/DeleteMatchList
        """

        operation = f"match-lists/{match_list_id}"

        response_json = self.request_http_delete(operation)

        return response_json

    def get_match_list_item_by_id(
        self,
        match_list_item_id: str
    ):
        """
        Gets a single match list item by ID.

        Examples:
            client.get_match_list_item_by_id("eae6...7374")

        Notes:
            get_match_list_item_by_id_manual() or get_match_list_items()
            can be used if you don't know the ID.

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetMatchListItem
        """

        operation = f"match-list-items/{match_list_item_id}"

        response_json = self.request_http_get(operation)

        return response_json['data']

    def get_match_list_item_by_id_manual(
        self,
        match_list_item_target_column: str,
        match_list_item_value: str,
        match_list_name: str
    ):
        """
        Match list item IDs are encoded in a very peculiar way.
        This function allows you to create the ID manually.
        The ID is made up of the following:
            -Target column of the match list (i.e., entity type)
            -The value of the match list item (e.g., domain.com)
            -Name of the match list

        Example:

        CLIENT.get_match_list_item_by_id_manual(
            "Domain",
            "testdomain.su",
            "Test Match List")
        """

        #Gets the MD5 hash for the first two values and hex value for the third
        match_list_item_target_column_md5 = hashlib.md5(
            match_list_item_target_column.encode()).hexdigest()

        match_list_item_value_md5 = hashlib.md5(
            match_list_item_value.encode()).hexdigest()

        match_list_name_hex = match_list_name.encode().hex()

        #Applied a substitution to two chars in the hash
        match_list_item_target_column_md5_encoded = self.encode_hash(
            match_list_item_target_column_md5)

        match_list_item_value_md5_encoded = self.encode_hash(
            match_list_item_value_md5)

        #Concatenates the three values to assemble the id
        match_list_item_id = (
            match_list_item_target_column_md5_encoded +
            match_list_item_value_md5_encoded +
            match_list_name_hex
            )

        #Gets the match list item with the assembled id
        response_json = self.get_match_list_item_by_id(match_list_item_id)

        return response_json

    def encode_hash(
        self,
        hashed_value: str
    ):
        """
        The MD5 hashes used in the match list item ID have encoded characters
        If the 13th char in the hash is not a 3, it becomes a 3
        The 17th char in the hash is set to the value of ((char % 4) + 8)

        This encoding method is arbitrary and seemingly pointless
        """

        hashed_value_list = list(hashed_value)

        if hashed_value_list[12] != '3':
            hashed_value_list[12] = '3'

        hex_substitute = f'{((int(hashed_value_list[16],16) % 4) + 8):x}'

        hashed_value_list[16] = str(hex_substitute)

        hashed_value = "".join(hashed_value_list)

        return hashed_value

    def get_match_list_items(
        self,
        query: str = None
    ):
        """
        Requests Sumo API for all match list items, or those matching a query, if given

        Examples:
            client.get_match_list_items(query = 'listName:"My Match List"')
            client.get_match_list_items(query = 'targetColumn:"Username"')

        Note:
            Target Column is case sensitive
            The default Target Columns are:
                Hostname, File Hash, URL, Domain, Username, IP Address,
                IP ASN, IP ISP, IP Organization, Source IP Address,
                Source IP ASN, Source IP ISP, Source IP Organization,
                Destination IP Address, Destination IP ASN,
                Destination IP ISP, Destination IP Organization

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetMatchListItems
        """

        operation = "match-list-items"

        returned_data = self.get_paginated_request(operation, query)

        return returned_data

    def get_match_list_item_by_value(
        self,
        match_list_item_value: str
    ):
        """
        Returns the match list item by value, works by performing a query.
        Custom queries can be done with get_match_list_items()

        Examples:
            client.get_match_list_item_by_value("testdomain.com")

        Note:

        Ref:

        """

        match_list_item = self.get_match_list_items(f"'value:{match_list_item_value}'")

        if not match_list_item:
            raise errors.MatchListNotFound(f"Match list item '{match_list_item_value}' was not found")

        return match_list_item

    def update_match_list_item(
        self,
        match_list_item_id: str,
        description: str,
        active: bool,
        expiration: str = None
    ):
        """
        Updates the provided match list item with, at minimum a description and active.
        Expiration is an optional field.

        Examples:
            client.update_match_list_item("1111....ffff", "New Description here", True)

        Notes:


        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateMatchListItem
        """

        operation = f"match-list-items/{match_list_item_id}"

        payload = {
            "fields": {
                "active": active,
                "expiration": expiration,
                "description": description
            }
        }

        response_json = self.request_http_put(operation, payload)

        return response_json['data']

    def delete_match_list_item(
        self,
        match_list_item_id: int
    ):
        """
        Deletes a match list item given a match list item id

        Examples:
            client.delete_match_list_item("1111....ffff")

        Notes:


        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/DeleteMatchListItem
        """

        operation = f"match-list-items/{match_list_item_id}"

        response_json = self.request_http_delete(operation)

        return response_json

    def add_match_list_items_to_match_list(
        self,
        match_list_id : int,
        items : list
    ):
        """
        Adds match list items given a match list item id

        Examples:
            items_to_add = [
                {
                    "value": "domain.com",
                    "active": True,
                    "expiration": "2024-12-31T23:59:59Z",
                    "description": "string"
                },
                {
                    "value": "domain.net",
                    "active": True,
                    "expiration": "2024-12-31T23:59:59Z",
                    "description": "string"
                },
                ...
            ]
            client.add_match_list_item(69, items_to_add)

        Notes:
            Items must follow this structure:
                {
                    "value": "string",
                    "active": True,
                    "expiration": "2023-07-24T15:49:41Z",
                    "description": "string"
                }

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/DeleteMatchListItem
        """

        operation = f"match-lists/{match_list_id}/items"

        payload = {
            "items": items
            }

        response_json = self.request_http_post(operation, payload)

        return response_json
