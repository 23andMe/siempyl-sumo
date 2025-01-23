# pylint: disable=E0401
"""
Contains functions needed to create an API client
"""
import base64
import re

import requests

from . import errors
from .entity_operations import EntityOperations
from .tag_operations import TagOperations
from .match_list_operations import MatchListOperations
from .criticality_operations import CriticalityOperations
from .insight_operations import InsightOperations
from .signal_operations import SignalOperations

class Client(
    EntityOperations,
    TagOperations,
    MatchListOperations,
    CriticalityOperations,
    InsightOperations,
    SignalOperations):
    """
    Class that represents API client, used to make REST requests
    str - access_id
    str - access_key
    str - region_code (e.g. us1, us2, au, jp, in, eu, de, ca, fed)
    """

    def __init__(
        self,
        access_id:str,
        access_key:str,
        region_code:str
    ):
        self.access_id = access_id
        self.access_key = access_key
        self.region_code = region_code

    @property
    def region_url(self):
        """Returns the appropiate URL for given region"""

        #The only valid region codes mapped to their URL
        region_to_url = {
            "us2": "https://api.us2.sumologic.com/api/sec/v1/",
            "au": "https://api.au.sumologic.com/api/sec/v1/",
            "us1": "https://api.sumologic.com/api/sec/v1/",
            "jp": "https://api.jp.sumologic.com/api/sec/v1/",
            "in": "https://api.in.sumologic.com/api/sec/v1/",
            "eu": "https://api.eu.sumologic.com/api/sec/v1/",
            "de": "https://api.de.sumologic.com/api/sec/v1/",
            "ca": "https://api.ca.sumologic.com/api/sec/v1/",
            "fed": "https://api.fed.sumologic.com/api/sec/v1/",
        }

        try:
            return region_to_url[self.region_code]
        except KeyError:
            raise errors.ApiSyntaxError(
                f"'{self.region_code}' is not a valid code. "
                f"The only valid codes are: {', '.join(region_to_url.keys())}"
            )

    def request_http_get(self, operation):
        """Makes HTTP GET requests"""

        url = f"{self.region_url}{operation}"
        headers = self.get_headers()

        response_json = self.request_http("GET", url, headers)

        return response_json

    def request_http_post(self, operation, payload = None):
        """Makes HTTP POST requests"""

        url = f"{self.region_url}{operation}"
        headers = self.get_headers()

        response_json = self.request_http("POST", url, headers, payload)

        return response_json

    def request_http_delete(self, operation, payload = None):
        """Makes HTTP DELETE requests"""

        url = f"{self.region_url}{operation}"
        headers = self.get_headers()

        response_json = self.request_http("DELETE", url, headers, payload)

        return response_json

    def request_http_put(self, operation, payload = None):
        """Makes HTTP PUT requests"""

        url = f"{self.region_url}{operation}"
        headers = self.get_headers()

        response_json = self.request_http("PUT", url, headers, payload)

        return response_json

    def request_http(self, method, url, headers, payload = None):
        """Handles errors from HTTP requests"""

        #Try/except to raise various HTTP related errors
        try:
            #If statement for each REST type used
            if method == "GET":
                response = requests.get(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=60)
            elif method == "PUT":
                response = requests.put(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=60)
            elif method == "POST":
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=60)
            elif method == "DELETE":
                response = requests.delete(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=60)
            else:
                raise Exception(f"Invalid method {method}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as error_http:
            if response.text:
                print(response.text)
            raise error_http
        except requests.exceptions.ConnectionError as error_connection:
            raise error_connection
        except requests.exceptions.Timeout as error_timeout:
            raise error_timeout
        except requests.exceptions.RequestException as error:
            raise error

        return response.json()

    def get_headers(self):
        """Crafts the headers used for the API calls"""

        #Retrieves the Access ID and Access Key fron environmental variables and concatenates them
        encoded_key = f"{self.access_id}:{self.access_key}"

        #Encodes the value as ascii in preparation for further encoding
        encoded_key = encoded_key.encode('ascii')

        #Encodes the value into base64
        #THIS IS NOT ENCRPYTION
        encoded_key = base64.b64encode(encoded_key)

        #Converts the value into a string to be passed into header
        #(will appear as b'bGlnbWEgbG1hbw==', e.g., otherwise)
        encoded_key = encoded_key.decode()

        headers = {
            'Authorization': f'Basic {encoded_key}'
        }

        return headers

    def get_paginated_request(self, operation, query = None, expand = False):
        """
        Used to handle operations that respond with multipage results
        """
        headers = self.get_headers()

        url_base = f"{self.region_url}{operation}?" #Creates the base URL request

        if query: #If a query is specified, adds it to the URL
            url_base += f"q={query}&"

        if expand: #If expand is required, adds it to the URL
            url_base += "expand=inventory&"

        has_next_page = True  #Flag used to track if API query results return more than 50 records
        offset = 0  #When results return more than 50, the offset needs to be specified
        limit = 50  #Ensures that results do not return more than 50 to consistently return pages
        returned_data = []   #Empty list that will be used to store all pages of returned data
        total_records = -1  #Total records in query, used to verify all records have been returned

        while has_next_page: #Responses with less than 50 records will set this to False

            #Variables will modify the offset for pagination
            url_offset = f"offset={offset}&limit={limit}"
            url_requested = url_base + url_offset

            response = requests.get(url_requested, headers=headers, timeout=60)

            self.handle_http_errors(url_requested, response)

            #Response has a boolean for whether or not there is a next page
            has_next_page = response.json()['data']['hasNextPage']

            #Response includes a total field that shows how many unique records are being returned
            total_records = response.json()['data']['total']

            #Stores the data from 'objects' into a seperate array
            for request_object in response.json()['data']['objects']:
                returned_data.append(request_object)

            offset += limit #Moves the offset over by 50, to return the next page

        self.handle_pagination_errors(len(returned_data), total_records)

        return returned_data

    def handle_http_errors(self, url, response):
        """
        Used to handle errors provided by API endpoint
        Handled errors:
            400's:
                - Invalid API key
            500's:
                - Invalid entity ID
        """

        valid_entity_types = ["_ip", "_username", "_hostname"]

        #Handles 400's based HTTP codes
        if str(response.status_code)[0] == '4':

            #Response.json() could contain multiple errors
            if response.json()['errors']:
                for error in response.json()['errors']:

                    #"unauthorized" in response typically means API key issues
                    if error['code'] == 'unauthorized':
                        raise errors.ApiPermissionError(error['message'])

        #Handles 500's based HTTP codes
        elif str(response.status_code)[0] == '5':

            #Response.json() could contain multiple errors
            if response.json()['errors']:
                for error in response.json()['errors']:

                    #"INTERNAL_SERVER_ERROR" typically means malformed search query
                    if error['code'] == 'INTERNAL_SERVER_ERROR':

                        #If entity type is missing from query, that is likely the cause
                        if any(entity_type not in url for entity_type in valid_entity_types):
                            raise errors.ApiSyntaxError('Entity type not specified in query.')

                        #Used for unknown issue causing this error
                        raise errors.ApiSyntaxError(error['message'])

    def handle_pagination_errors(self, length_returned_data, total_records):
        """
        Used to handle errors regarding pagination
        Handled errors:
            -Record mismatch
        """

        #Check to see if count of returned records equals record count reported by API
        if length_returned_data != total_records:
            raise errors.ApiPaginationError("Count of returned data does not equal total records")

    def validate_entity_type(self, entity_id):
        """Used to ensure that provided entity type is valid"""

        valid_entity_types = ["_ip", "_username", "_hostname"]

        #Splits the entity once at the first single hyphen and returns a list
        entity_split = re.split(r'(?<!\-)\-(?!\-)',entity_id,1)
        entity_type = entity_split[0]

        if len(entity_split) == 1 or not entity_type:
            raise errors.ApiSyntaxError("No entity type provided")

        if entity_type not in valid_entity_types:
            raise errors.ApiSyntaxError(f'"{entity_type}" is an invalid entity type')

        return True

    def validate_entity(self, response_json):
        """Used to ensure that returned entity exists"""

        if (not response_json['data']['lastSeen'] and
            not response_json['data']['firstSeen']):
            raise errors.EntityNotFound(f"{response_json['data']['id']}")

        return True
