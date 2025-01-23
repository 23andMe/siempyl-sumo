# pylint: disable=E1101,C0301
"""
Contains functions used to make signal based requests
    -get_insight() https://api.us2.sumologic.com/docs/sec/#operation/GetInsight
    -get_insights() https://api.us2.sumologic.com/docs/sec/#operation/GetInsights

"""

from .errors import InsightInputError

class InsightOperations:
    """
    InsightOperations class that contains all the operations dealing with Insights
    """
    def insight_input_validation(self, insight_id):
        """
        Insight IDs following the naming convention "INSIGHT-###"
        """
        if not isinstance(insight_id, str):
            raise InsightInputError("A string must be provided for insight ID")
        insight_id = insight_id.upper()
        if "INSIGHT" not in insight_id:
            raise InsightInputError("Insights must be formatted like 'INSIGHT-###'")
        return insight_id

    def insight_status_color_valdation(self, hex_color):
        """
        Insight status colors must be a preset hex value"
        """
        colors = self.get_insight_status_palette()
        for category in colors.values():
            if hex_color.upper() in category:
                return True
        raise InsightInputError("Hex not found. Use CLIENT.get_insight_status_palette() to see valid colors")


    def get_insight(self, insight_id: str):
        """
        Requests Sumo API for a single insight

        Examples:
            client.get_insight("INSIGHT-420")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsight
        """
        insight_id = self.insight_input_validation(insight_id)
        operation = f"insights/{insight_id}"
        response_json = self.request_http_get(operation)
        return response_json['data']

    def get_insights(self, query):
        """
        Requests Sumo API for all insights for given query

        Examples:
            client.get_insights("status='new'")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsights
        """
        operation = "insights"
        returned_data = self.get_paginated_request(operation, query)
        return returned_data

    def get_insight_enrichment(self, insight_id: str):
        """
        Requests Sumo API for enrichment of given insight

        Examples:
            client.get_insight_enrichment("INSIGHT-420")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightEnrichments
        """
        insight_id = self.insight_input_validation(insight_id)
        operation = f"insights/{insight_id}/enrichments"
        returned_data = self.request_http_get(operation)
        return returned_data['data']['enrichments']

    # def get_insights_all(self, query):
    #     """
    #     Requests Sumo API for all insights for given query
    #     This endpoint seems useless given getinsights

    #     Examples:
    #         client.get_insights_all("status='new'")

    #     Notes:
    #         None

    #     Ref:
    #         https://api.us2.sumologic.com/docs/sec/#operation/GetAllInsights
    #     """
    #     operation = "insights/all"
    #     returned_data = self.get_paginated_request(operation, query)
    #     return returned_data

    def get_insight_comments(self, insight_id: str):
        """
        Requests Sumo API for comments of given insight

        Examples:
            client.get_insight_comments("INSIGHT-420")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightComments
        """
        insight_id = self.insight_input_validation(insight_id)
        operation = f"insights/{insight_id}/comments"
        returned_data = self.request_http_get(operation)
        return returned_data['data']['comments']

    def get_insight_history(self, insight_id: str):
        """
        Requests Sumo API for history of given insight

        Examples:
            client.get_insight_history("INSIGHT-420")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightHistory
        """
        insight_id = self.insight_input_validation(insight_id)
        operation = f"insights/{insight_id}/history"
        returned_data = self.request_http_get(operation)
        return returned_data['data']['history']

    def get_insight_involved_entities(self, insight_id: str):
        """
        Requests Sumo API for entities involved with given insight

        Examples:
            client.get_insight_involved_entities("INSIGHT-420")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightRelatedEntities
        """
        insight_id = self.insight_input_validation(insight_id)
        operation = f"insights/{insight_id}/involved-entities"
        returned_data = self.request_http_get(operation)
        return returned_data['data']['involvedEntities']

    def get_custom_insight(self, insight_id: str):
        """
        Retrieves a specific custom insight

        Examples:
            client.get_custom_insight(1)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetCustomInsight
        """
        operation = f"custom-insight/{insight_id}"
        returned_data = self.request_http_get(operation)
        return returned_data['data']

    def get_custom_insights(self, query: str):
        """
        Retrieves a list of custom insights based on a query

        Examples:
            client.get_custom_insights("status=open")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetCustomInsights
        """
        operation = "custom-insights"
        params = {"query": query}
        returned_data = self.request_http_get(operation, params=params)
        return returned_data['data']

    def update_custom_insight(self, insight_id: str, body: dict):
        """
        Updates a specific custom insight

        Examples:
            client.update_custom_insight(1, body)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateCustomInsight
        """
        operation = f"custom-insight/{insight_id}"
        returned_data = self.request_http_put(operation, json=body)
        return returned_data['data']

    def create_custom_insight(self, body: dict):
        """
        Creates a new custom insight

        Examples:
            client.create_custom_insight(body)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/CreateCustomInsight
        """
        operation = "custom-insight"
        returned_data = self.request_http_post(operation, json=body)
        return returned_data['data']

    def delete_custom_insight(self, insight_id: str):
        """
        Deletes a specific custom insight

        Examples:
            client.delete_custom_insight(1)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/DeleteCustomInsight
        """
        operation = f"custom-insight/{insight_id}"
        returned_data = self.request_http_delete(operation)
        return returned_data['data']

    def get_insights_configuration(self):
        """
        Requests Sumo API for insights configurations

        Examples:
            client.get_insights_configuration()

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightsConfiguration
        """
        operation = "insights-configuration"
        returned_data = self.request_http_get(operation)
        return returned_data['data']

    def update_insights_configuration(self, config):
        """
        Updates Sumo API for insights configurations

        Examples:
            client.update_insights_configuration(config)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateInsightConfiguration
        """
        operation = "insights-configuration"
        returned_data = self.request_http_put(operation, payload=config)
        return returned_data['config']

    def get_insight_status(self, insight_id: str):
        """
        Requests Sumo API for status of given insight status

        Examples:
            client.get_insight_history("INSIGHT-420")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightStatus
        """
        insight_id = self.insight_input_validation(insight_id)
        operation = f"insight-status/{insight_id}"
        returned_data = self.request_http_get(operation)
        return returned_data['data']

    def get_insight_statuses(self):
        """
        Requests Sumo API for all insight statuses

        Examples:
            client.get_insight_history("INSIGHT-420")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightStatuses
        """
        operation = "insight-status"
        returned_data = self.request_http_get(operation)
        return returned_data['data']

    def create_insight_status(self, body):
        """
        Creates a custom insight status

        Examples:
            client.create_insight_status(body)

        Notes:
            Body must contain fields:

            body = { 
                "fields": 
                    {
                        "name": "Status Name", #required
                        "description": "Status Description",
                        "color": "#FFC0CB" #must be hex color
                    }
            }

            CLIENT.get_insight_status_palette() to show valid hex options

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/CreateInsightStatus
        """
        operation = "insight-status/"
        self.insight_status_color_valdation(body['fields']['color'])
        returned_data = self.request_http_post(operation, payload=body)
        return returned_data['data']

    def update_insight_status(self, insight_status_id: int, body):
        """
        Updates a custom insight status

        Examples:
            client.update_insight_status(body)

        Notes:
            Body must contain fields:

            body = { 
                "fields": 
                    {
                        "name": "Status Name", #required
                        "description": "Status Description",
                        "color": "#FFC0CB" #must be hex color
                    }
            }

            CLIENT.get_insight_status_palette() to show valid hex options

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateInsightStatusOption
        """
        operation = f"insight-status/{insight_status_id}"
        self.insight_status_color_valdation(body['fields']['color'])
        returned_data = self.request_http_put(operation, payload=body)
        return returned_data['data']

    def delete_insight_status(self, insight_status_id: int):
        """
        Deletes a custom insight status

        Examples:
            client.delete_insight_status(4)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightStatus
        """

        operation = f"insight-status/{insight_status_id}"

        returned_data = self.request_http_delete(operation)

        return returned_data['data']

    def get_insight_resolution(self, insight_id: str):
        """
        Retrieves a specific insight resolution

        Examples:
            client.get_insight_resolution(1)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightResolution
        """
        operation = f"insight-resolution/{insight_id}"
        returned_data = self.request_http_get(operation)
        return returned_data['data']

    def get_insight_resolutions(self):
        """
        Retrieves all insight resolutions

        Examples:
            client.get_insight_resolutions()

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightResolutions
        """
        operation = "insight-resolutions"
        returned_data = self.request_http_get(operation)
        return returned_data['data']

    def update_insight_resolution(self, insight_id: str, payload: dict):
        """
        Updates a specific insight resolution

        Examples:
            client.update_insight_resolution(1, payload)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateInsightResolution
        """
        operation = f"insight-resolution/{insight_id}"
        returned_data = self.request_http_put(operation, json=payload)
        return returned_data['data']

    def add_tag_to_insight(self, insight_id: str, tag: str):
        """
        Adds a tag to an Insight

        Examples:
            client.add_tag_to_insight(1, "tag_name")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/AddTagToInsight
        """
        operation = f"insight/{insight_id}/tag"
        payload = {"tag": tag}
        returned_data = self.request_http_post(operation, json=payload)
        return returned_data['data']

    def create_insight_resolution(self, payload: dict):
        """
        Creates a new insight resolution

        Examples:
            client.create_insight_resolution(payload)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/CreateInsightResolution
        """
        operation = "insight-resolution"
        returned_data = self.request_http_post(operation, json=payload)
        return returned_data['data']

    def create_enrichment_on_insight(self, insight_id: str, payload: dict):
        """
        Creates or updates an enrichment on an Insight

        Examples:
            client.create_enrichment_on_insight(1, payload)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/CreateOrUpdateEnrichmentOnInsight
        """
        operation = f"insight/{insight_id}/enrichment"
        returned_data = self.request_http_post(operation, json=payload)
        return returned_data['data']

    def remove_tag_from_insight(self, insight_id: str, tag: str):
        """
        Removes a tag from an Insight

        Examples:
            client.remove_tag_from_insight(1, "tag_name")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/RemoveTagFromInsight
        """
        operation = f"insight/{insight_id}/tag/{tag}"
        returned_data = self.request_http_delete(operation)
        return returned_data['data']

    def delete_insight_resolution(self, insight_id: str):
        """
        Deletes a specific insight resolution

        Examples:
            client.delete_insight_resolution(1)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/DeleteInsightResolution
        """
        operation = f"insight-resolution/{insight_id}"
        returned_data = self.request_http_delete(operation)
        return returned_data['data']

    def update_insight_assignee(self, insight_id: str, assignee: str):
        """
        Updates the assignee of an Insight

        Examples:
            client.update_insight_assignee(1, "assignee")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateInsightAssignee
        """
        operation = f"insight/{insight_id}/assignee"
        payload = {"assignee": assignee}
        returned_data = self.request_http_put(operation, json=payload)
        return returned_data['data']

    def get_insight_executed_automations(self, insight_id: str):
        """
        Retrieves the executed automations for a specific Insight

        Examples:
            client.get_insight_executed_automations(1)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightExecutedAutomations
        """
        operation = f"insight/{insight_id}/executed-automations"
        returned_data = self.request_http_get(operation)
        return returned_data['data']

    def update_insight_severity(self, insight_id: str, severity: str):
        """
        Updates the severity of an Insight

        Examples:
            client.update_insight_severity(1, "high")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/UpdateInsightSeverity
        """
        operation = f"insight/{insight_id}/severity"
        payload = {"severity": severity}
        returned_data = self.request_http_put(operation, json=payload)
        return returned_data['data']

    def remove_assignee_from_insight(self, insight_id: str):
        """
        Removes the assignee from an Insight

        Examples:
            client.remove_assignee_from_insight(1)

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/RemoveAssigneeFromInsight
        """
        operation = f"insight/{insight_id}/assignee"
        returned_data = self.request_http_delete(operation)
        return returned_data['data']

    def get_insights_count(
        self,
        start_timestamp: str,
        bucket_duration: int,
        end_timestamp: str = None,
        timezone: str = None
        ):
        """
        Gets the count of Insights over time

        Examples:
            client.get_count_of_insights()

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetCountOfInsights
        """

        query = []

        if end_timestamp:
            query.append("&endTimestamp="+end_timestamp)

        if timezone:
            query.append("&timezone="+timezone)

        operation = f"insights/counts?startTimestamp={start_timestamp}&bucketDuration={bucket_duration}" + '&'.join(query)

        response_json = self.request_http_get(operation)

        return response_json['data']

    def add_comment_to_insight(self, insight_id: str, comment: str):
        """
        Adds a new comment on an Insight

        Examples:
            client.add_comment_to_insight(1, "This is a comment")

        Notes:
            None

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/AddCommentToInsight
        """
        operation = f"insight/{insight_id}/comment"
        payload = {"comment": comment}
        returned_data = self.request_http_post(operation, json=payload)
        return returned_data['data']


    def get_insight_status_palette(self):
        """
        Used to return a dict list of all the available colors for Sumo custom insight statuses.
        """

        colors = {
            "reds": {
                "#FFD3D3": "Whispering Blush",
                "#FFB5B5": "Serenade of Rosé",
                "#FF8989": "Velvet Rebellion",
                "#FF5D5D": "Clandestine Scarlet",
                "#DF3D3D": "Tempestuous Garnet",
                "#BF2121": "Forbidden Ember",
                "#991A1A": "Enigmatic Ruby",
                "#731414": "Veiled Merlot"
            },
            "oranges": {
                "#FFD7BB": "Golden Mirage",
                "#FFBC8E": "Sundrenched Sienna",
                "#F7995B": "Burnished Copper",
                "#F0731F": "Autumnal Blaze",
                "#C55033": "Crimson Emberglow",
                "#933C03": "Rustic Ember",
                "#763002": "Molten Earth",
                "#582402": "Obscure Terracotta"
            },
            "yellows": {
                "#F7E9AB": "Elysian Aura",
                "#F2DA73": "Midas Reflection",
                "#DFBE2E": "Gilded Enigma",
                "#B4950C": "Solar Obscura",
                "#8A720B": "Hermetic Ochre",
                "#685500": "Arcane Gold",
                "#534400": "Cryptic Saffron",
                "#3E3300": "Shadowed Mustard"
            },
            "greens": {
                "#DFF9B6": "Ethereal Meadow",
                "#BFF26C": "Verdant Whimsy",
                "#6CAE01": "Enchanted Lime",
                "#578A00": "Hidden Grove",
                "#507A0B": "Mystic Herb",
                "#496917": "Secretive Moss",
                "#3A5412": "Veiled Fern",
                "#2C3F0D": "Obscured Woodland"
            },
            "greens_variant": {
                "#C1F4CB": "Illusory Mint",
                "#98ECA9": "Celestial Aloe",
                "#51D16B": "Elven Grove",
                "#28AA55": "Mythic Jade",
                "#16943E": "Enigma Ivy",
                "#116B25": "Sorcerer's Green",
                "#0E561E": "Ancient Pine",
                "#0A4016": "Hidden Juniper"
            },
            "indigos": {
                "#B4F4E6": "Mystical Lagoon",
                "#82EDD6": "Enchanted Seafoam",
                "#33DEB9": "Celestial Emerald",
                "#24B596": "Abyssal Teal",
                "#079173": "Veiled Aquamarine",
                "#0C6B56": "Secret Sapphire",
                "#0A5645": "Enigmatic Verde",
                "#074034": "Obscured Abyss"
            },
            "blues": {
                "#B9EEFF": "Seraphic Sky",
                "#8BE2FF": "Whispering Azure",
                "#50CAF2": "Celestial Zephyr",
                "#00A0D6": "Deep Cerulean",
                "#007CA6": "Obscure Aegean",
                "#005982": "Abyssal Twilight",
                "#004768": "Mystic Harbor",
                "#00354E": "Enigmatic Ocean"
            },
            "blues_variant": {
                "#C3E5F0": "Ephemeral Mist",
                "#9BD3E6": "Whimsical Cyan",
                "#6FB9D1": "Enchanted River",
                "#4EA0BC": "Ethereal Aqua",
                "#2A84A2": "Obscure Bluejay",
                "#066180": "Midnight Tides",
                "#054E66": "Hidden Lagoon",
                "#043A4D": "Veiled Depths"
            },
            "purples": {
                "#E0D9FF": "Enigmatic Lilac",
                "#CBBFFF": "Whispering Amethyst",
                "#AC99FF": "Velvet Violet",
                "#8D79E8": "Mystic Lavender",
                "#6F5ACC": "Obscure Indigo",
                "#4F3AAB": "Enchanted Aubergine",
                "#3F2E89": "Hidden Plum",
                "#2F2367": "Veiled Mulberry"
            },
            "violets": {
                "#FFD0F5": "Ethereal Petal",
                "#FFB0EE": "Whispering Fuchsia",
                "#F27CD9": "Celestial Orchid",
                "#E058C0": "Enchanted Magenta",
                "#BA36A4": "Enigmatic Rose",
                "#8C1C74": "Obscured Maroon",
                "#70165D": "Veiled Burgundy",
                "#541146": "Hidden Berry"
            },
            "grays": {
                "#FFFFFF": "Void of Light",
                "#E6E6E6": "Phantom Fog",
                "#BFBFBF": "Gossamer Shade",
                "#999999": "Stealthy Ash",
                "#808080": "Obscure Silver",
                "#404040": "Enigmatic Smoke",
                "#000000": "Abyssal Void",
                "#1A1A1A": "Veiled Charcoal"
            }
        }

        return colors
