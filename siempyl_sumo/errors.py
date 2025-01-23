class APIError(Exception):
    MESSAGE_PREFIX = ""

    def __init__(self, message):
        self.message = f"{self.MESSAGE_PREFIX} {message}"
        return super().__init__(self.message)

class ApiPermissionError(Exception):
    """
    Exception raised for errors in API permissions.

    Attributes:
        message -- explanation of the error, provided by API endpoint
    """
    MESSAGE_PREFIX = "SIEM API error."

class ApiSyntaxError(Exception):
    """
    Exception raised for errors in API syntax.

    Attributes:
        message -- explanation of the error
    """
    MESSAGE_PREFIX = "SIEM API error."

class ApiPaginationError(Exception):
    """
    Exception raised for errors in API pagination.

    Attributes:
        message -- explanation of the error
    """
    MESSAGE_PREFIX = "SIEM API error."

class EntityNotFound(Exception):
    """
    Exception raised for when a queried entity doesn't exist.

    Attributes:
        message -- explanation of the error
    """
    MESSAGE_PREFIX = "Entity not found."

class MatchListNotFound(Exception):
    """
    Exception raised for when a queried match list doesn't exist.

    Attributes:
        message -- explanation of the error
    """
    MESSAGE_PREFIX = "Match list not found."

class MatchListItemNotFound(Exception):
    """
    Exception raised for when a queried match list item doesn't exist.

    Attributes:
        message -- explanation of the error
    """
    MESSAGE_PREFIX = "Match list not found."

class SignalEntityMismatch(Exception):
    """
    Exception raised for when an insight is created with mismatched signal entities.

    Attributes:
        message -- explanation of the error
    """
    MESSAGE_PREFIX = "Signals do not belong to the same entity."

class InsightInputError(Exception):
    """
    Exception raised for when an invalid insight ID is provided.

    Attributes:
        message -- explanation of the error
    """
    MESSAGE_PREFIX = "Invalid Insight Input"
