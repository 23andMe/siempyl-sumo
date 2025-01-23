# pylint: disable=E1101,C0301
"""
Contains functions used to make criticality based requests
    -get_entity_criticality_configs() https://api.us2.sumologic.com/docs/sec/#operation/GetEntityCriticalityConfigs
    -get_entity_criticality_config() https://api.us2.sumologic.com/docs/sec/#operation/GetEntityCriticalityConfig
    -update_entity_criticality() https://api.us2.sumologic.com/docs/sec/#operation/UpdateEntityCriticalityConfig
    -create_criticality_configuration() https://api.us2.sumologic.com/docs/sec/#operation/CreateEntityCriticalityConfig
    -delete_criticality_configuration() https://api.us2.sumologic.com/docs/sec/#operation/DeleteEntityCriticalityConfig
"""

class CriticalityOperations:
    """
    CriticalityOperations class that contains all the operations dealing with Criticality
    """

    def get_entity_criticality_configs(self):
        """
        Requests Sumo API for all criticality configs

        Examples:
            client.get_entity_criticality_configs()

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetEntityCriticalityConfigs
        """

        operation = "entity-criticality-configs"

        response_json = self.request_http_get(operation)

        return response_json['data']['objects']

    def get_entity_criticality_config(self, crit_id):
        """
        Requests Sumo API for a specific criticality config given the ID

        Examples:
            client.get_entity_criticality_configs("7")

        Notes:
            The ID of a criticality is a numeric value assigned sequentially upon creation

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetEntityCriticalityConfig
        """

        operation = f"entity-criticality-configs/{crit_id}"

        response_json = self.request_http_get(operation)

        return response_json['data']


    def update_entity_criticality(self, entity_id: str, criticality: str):
        """
        Updates the entity with the given criticality

        Examples:
            client.update_entity_criticality("_username-humanp","Leaver")

        Notes:
            This function requires the entity ID and the criticality name.

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateEntityCriticality
        """

        operation = f"entities/{entity_id}/criticality"

        payload = {
            "criticality": criticality
            }

        response_json = self.request_http_put(operation, payload)

        return response_json

    def update_criticality_configuration(self, crit_id, crit_expression):
        """
        Updates criticality configuration

        Examples:
            client.update_entity_criticality("420","severity + 69")

        Notes:
            This function requires the criticality ID and the criticality severity expression.

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateEntityCriticalityConfig
        """

        operation = f"entity-criticality-configs/{crit_id}"

        payload = {
            "fields":
            {
                "severityExpression": crit_expression
            }
        }

        response_json = self.request_http_put(operation, payload)

        return response_json

    def create_criticality_configuration(self, crit_name, crit_expression):
        """
        Creates criticality configuration

        Examples:
            client.create_criticality_configuration("Nice Criticality","severity + 69")

        Notes:
            Severity expressions format: "severity [+,-,*,/] [int,double]"
            E.g., "severity + 1", "severity * 1.2", "severity / 2"

            "severity" is case sensitive. "Severity + 1" will cause an error

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/CreateEntityCriticalityConfig
        """

        operation = "entity-criticality-configs"

        payload = {
                "fields":
                {
                    "name": crit_name,
                    "severityExpression": crit_expression
                }
            }

        response_json = self.request_http_post(operation, payload)

        return response_json

    def delete_criticality_configuration(self, crit_id):
        """
        Deletes criticality configuration

        Examples:
            client.delete_entity_criticality("420")

        Notes:
            This function requires the entity ID and the criticality name.

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/DeleteEntityCriticalityConfig
        """

        operation = f"entity-criticality-configs/{crit_id}"

        response_json = self.request_http_delete(operation)

        return response_json
