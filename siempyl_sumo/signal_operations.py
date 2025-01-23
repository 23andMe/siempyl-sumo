# pylint: disable=E1101,C0301
"""
Contains functions used to make signal based requests
    -get_signal() https://api.us2.sumologic.com/docs/sec/#operation/GetSignal
    -get_signals() https://api.us2.sumologic.com/docs/sec/#operation/GetAllSignals
    -get_signal_enrichment() https://api.us2.sumologic.com/docs/sec/#operation/GetSignalEnrichments
    -create_insight_from_signals() https://api.us2.sumologic.com/docs/sec/#operation/CreateInsightFromSignals
    -update_create_signal_enrichment() https://api.us2.sumologic.com/docs/sec/#operation/SaveSignalEnrichment
    -add_signals_to_insight() https://api.us2.sumologic.com/docs/sec/#operation/AddSignalsToInsight
    -delete_signals_from_insight() https://api.us2.sumologic.com/docs/sec/#operation/RemoveSignalsFromInsight
    -get_signals_count() https://api.us2.sumologic.com/docs/sec/#operation/GetInsightCounts

"""

from . import errors

class SignalOperations:
    """
    SignalOperations class that contains all the operations dealing with Signal
    """
    def get_signal(self, signal_id: str):
        """
        Requests Sumo SIEM API for a specific signal given its ID.

        Examples:
            client.get_signal("01189998-8199-9119-7253-uhzruJ0BzoI")

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetSignal
        """

        operation = f"signals/{signal_id}"

        response_json = self.request_http_get(operation)

        return response_json['data']

    def get_signals_query(self, query: str = None):
        """
        Requests Sumo SIEM API for all signals, or signals matching a query, if given

        Examples:
            client.get_signals(query='entity.id:"_username-humanp"')

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetAllSignals
        """
        operation = "signals/"

        returned_data = self.get_paginated_request(operation, query)

        return returned_data

    def get_signal_enrichments(self, signal_id: str):
        """
        Requests Sumo SIEM API for enrichment data from a specific signal

        Examples:
            client.get_signals_enrichments(signal_id="01189998-8199-9119-7253-uhzruJ0BzoI")
        
        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetSignalEnrichments

        """

        operation = f"signals/{signal_id}/enrichments"

        response_json = self.request_http_get(operation)

        return response_json['data']

    def create_insight_from_signals(self, signal_ids: str):
        """
        Creates an insight from a list of signals. Signals must share an entity

        Examples:
            client.create_insight_from_signals(signal_ids=["12345678-1234-1234-1234-uhzruJ0BzoI", "12345678-1234-1234-1234-arhqyB3AbmY"])

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/CreateInsightFromSignals
        """

        operation = "insights"

        #Validate signals before creating insights
        entity_ids = []
        for signal_id in signal_ids:
            entity_id = self.get_signal(signal_id)['entity']['id']
            entity_ids.append(entity_id)

            if not entity_ids.count(entity_ids[0]) == len(entity_ids):
                raise errors.SignalEntityMismatch(f"Entities {entity_ids} do not match")

        payload = {

            "signalIds": signal_ids

        }

        response_json = self.request_http_post(operation, payload)

        return response_json['data']

    def update_create_signal_enrichment(
        self,
        signal_id: str,
        enrichment_type: str,
        detail: str,
        raw: str = None,
        expire_at: str = None,
        reputation: str = None,
        external_url: str = None
    ):
        """
        Updates or Creates enrichment data for a signal

        Eaxample:
            client.update_create_signal_enrichment(signal_id="01189998-8199-9119-7253-uhzruJ0BzoI", enrichment_type="humanp", detail="humanp", reputation="Suspicious", expire_at="2024-05-17T20:44:24Z")

        Notes:
            
            Payload:
                enrichment_type is the title of the enrichment
                reputation can only use one of the following: Malicous, Not Flagged, Suspicous     

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/SaveSignalEnrichment
        """

        operation = f"signals/{signal_id}/enrichments/{enrichment_type}"

        payload = {
            "detail": f"{{{detail}}}",
            "raw": raw,
            "expiresAt": expire_at,
            "reputation": reputation,
            "externalUrl": external_url
        }

        response_json = self.request_http_put(operation, payload)

        return response_json['data']


    def add_signals_to_insight(self, insight_id: str, signal_ids: str):
        """
        Adds a list of sginals to an insight

        Example:
            client.add_signals_to_insight(insight_id="INSIGHT-9000", signal_ids=["01189998-8199-9119-7253-uhzruJ0BzoI"])

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/AddSignalsToInsight
        """

        operation = f"insights/{insight_id}/signals"

        #Validate signals before creating insights
        #TODO add get.entity()['entity']['id']
        entity_ids = []
        for signal_id in signal_ids:
            entity_id = self.get_signal(signal_id)['entity']['id']
            entity_ids.append(entity_id)

            if not entity_ids.count(entity_ids[0]) == len(entity_ids):
                raise errors.SignalEntityMismatch(f"Entities {entity_ids} do not match")

        payload = {
            "signalIds": signal_ids

                }

        response_json = self.request_http_put(operation, payload)

        return response_json['data']

    def delete_signals_from_insight(self, insight_id: str, signal_ids: str):
        """
        Removes a signal from an insight

        Example:
            client.delete_signals_from_insight(signal_ids=["01189998-8199-9119-7253-uhzruJ0BzoI"], insight_id="INSIGHT-9000")

        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/RemoveSignalsFromInsight
        """

        operation = f"insights/{insight_id}/signals"

        payload = {
            "signalIds": signal_ids

                }

        response_json = self.request_http_delete(operation, payload)

        return response_json['data']


    def get_signals_count(
        self,
        start_timestamp: str,
        bucket_duration: int,
        end_timestamp: str = None,
        timezone: str = None
        ):
        """
        Get the count of Insights over time. Bucket must be provided in seconds (integer)
        Example:
            client.get_signals_count(start_timestamp="2024-05-15T20:44:24Z", bucket_duration=60)
        Ref:
            https://api.us2.sumologic.com/docs/sec/#operation/GetInsightCounts
            https://api.us2.sumologic.com/api/sec/v1/signals/counts?startTimestamp=2024-05-15T20:44:24Z&bucketDuration=1
        """

        query = []

        if end_timestamp:
            query.append("&endTimestamp="+end_timestamp)

        if timezone:
            query.append("&timezone="+timezone)

        operation = f"signals/counts?startTimestamp={start_timestamp}&bucketDuration={bucket_duration}" + '&'.join(query)

        response_json = self.request_http_get(operation)

        return response_json['data']
