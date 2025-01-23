# pylint: disable=E1101
"""
Contains functions used to make tag based requests
    -add_entity_tag() https://api.us2.sumologic.com/docs/sec/#operation/AddEntityTags
    -remove_entity_tag() https://api.us2.sumologic.com/docs/sec/#operation/RemoveEntityTags
    -add_insight_tag() https://api.us2.sumologic.com/docs/sec/#operation/AddTagToInsight
    -remove_insight_tag() https://api.us2.sumologic.com/docs/sec/#operation/RemoveTagFromInsight
    -bulk_add_entity_tag() https://api.us2.sumologic.com/docs/sec/#operation/BulkAddEntityTags
    -bulk_update_entity_tag() https://api.us2.sumologic.com/docs/sec/#operation/BulkUpdateEntityTags
    -bulk_remove_entity_tag() https://api.us2.sumologic.com/docs/sec/#operation/BulkRemoveEntityTags
"""

class TagOperations:
    """
    Tag class that covers all tag operations
    """

    def add_entity_tag(self, entity_id, tag):
        """Adds provided tag (string or list) to given entity_id"""

        #Ensures that entity type (e.g., _hostname) is present and valid
        self.validate_entity_type(entity_id)

        operation = f"entities/{entity_id}/tags"

        payload = {
            "tags": tag
            }

        response_json = self.request_http_post(operation, payload)

        return response_json['data']

    def remove_entity_tag(self, entity_id, tag):
        """Removes provided tag (string or list) from given entity_id"""

        #Ensures that entity type (e.g., _hostname) is present and valid
        self.validate_entity_type(entity_id)

        operation = f"entities/{entity_id}/tags"

        payload = {
            "tags": tag
            }

        response_json = self.request_http_delete(operation, payload)

        return response_json['data']

    def add_insight_tag(self, insight_id, tag):
        """Adds provided tag (string or list) to given insight_id"""

        operation = f"insights/{insight_id}/tags"

        payload = {
            "tagName": tag
            }

        response_json = self.request_http_post(operation, payload)

        return response_json

    def remove_insight_tag(self, insight_id, tag):
        """Removes provided tag from given insight_id"""

        operation = f"insights/{insight_id}/tags/{tag}"

        response_json = self.request_http_delete(operation)

        return response_json['data']

    def bulk_update_entity_tag(self, entity_ids, tags):
        """Performs a bulk update on a list of entities with a list of tags"""

        #Ensures that entity type (e.g., _hostname) is present and valid
        for entity_id in entity_ids:
            self.validate_entity_type(entity_id)

        operation = "entities/bulk-update-tags"

        payload = {
            "entityIds": entity_ids,
            "tags": tags
            }

        response_json = self.request_http_post(operation, payload)

        return response_json['data']

    def bulk_add_entity_tag(self, entity_ids, tags):
        """Performs a bulk add on a list of entities with a list of tags"""

        #Ensures that entity type (e.g., _hostname) is present and valid
        for entity_id in entity_ids:
            self.validate_entity_type(entity_id)

        operation = "entities/bulk-add-tags"

        payload = {
            "entityIds": entity_ids,
            "tags": tags
            }

        response_json = self.request_http_post(operation, payload)

        return response_json['data']

    def bulk_remove_entity_tag(self, entity_ids, tags):
        """Performs a bulk remove on a list of entities with a list of tags"""

        #Ensures that entity type (e.g., _hostname) is present and valid
        for entity_id in entity_ids:
            self.validate_entity_type(entity_id)

        operation = "entities/bulk-remove-tags"

        payload = {
            "entityIds": entity_ids,
            "tags": tags
            }

        response_json = self.request_http_post(operation, payload)

        return response_json['data']
