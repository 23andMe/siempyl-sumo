# pylint: disable=E1101,C0301
from dataclasses import dataclass
import base64
import time
import random
import os
import pytest

from siempyl_sumo import Client
from siempyl_sumo import errors

ACCESS_ID = os.environ['ACCESS_ID']
ACCESS_KEY = os.environ['ACCESS_KEY']
REGION_CODE = "us2"

@dataclass
class StubbedResponse:
    status_code: int
    json_data: dict

    def json(self):
        return self.json_data


def test_client():
    """Simple test case illustrating basic client functionality works
    """
    client = Client(ACCESS_ID, ACCESS_KEY, REGION_CODE)
    encoded_key = base64.b64encode((f"{ACCESS_ID}:{ACCESS_KEY}").encode('ascii')).decode()
    assert client.region_url == 'https://api.us2.sumologic.com/api/sec/v1/'
    assert client.get_headers() == {'Authorization': f'Basic {encoded_key}'}

def test_client_invalid_region_code():
    """Testing error handling for invalid region code
    """
    client = Client(ACCESS_ID, ACCESS_KEY, "us69")

    with pytest.raises(errors.ApiSyntaxError):
        print(client.region_url)

def test_handle_http_errors():
    """Simple test case for testing handle_http_errors works

    NOTE: Probably want more test cases here to cover different error codes
    """
    client = Client('access-id', 'access-key', 'us2')
    with pytest.raises(errors.ApiSyntaxError):
        client.handle_http_errors('sup', StubbedResponse(500, {'errors': [{'code': 'INTERNAL_SERVER_ERROR'}]}))

def test_get_entity_invalid_entity_type():
    """Simple test case testing valid entity types
    """
    client = Client(ACCESS_ID, ACCESS_KEY, REGION_CODE)

    #providing an invalid entity type
    with pytest.raises(errors.ApiSyntaxError):
        client.get_entity("_badentitytype-humanp")

    #providing no entity type
    with pytest.raises(errors.ApiSyntaxError):
        client.get_entity("humanp")

def test_handle_insight_errors():
    """Simple test case testing valid insights
    """
    client = Client(ACCESS_ID, ACCESS_KEY, REGION_CODE)  

    with pytest.raises(errors.InsightInputError):
        client.get_insight("INSOGHT-123")

    with pytest.raises(errors.InsightInputError):
        body_color_name = {
            "fields": 
                {
                    "name": "Status Name",
                    "description": "Status Description",
                    "color": "PINK" 
                }
        }

        client.create_insight_status(body_color_name)

    with pytest.raises(errors.InsightInputError):
        body_invalid_hex = {
            "fields": 
                {
                    "name": "Status Name",
                    "description": "Status Description",
                    "color": "#AAAAAA" 
                }
        }

        client.create_insight_status(body_invalid_hex)
