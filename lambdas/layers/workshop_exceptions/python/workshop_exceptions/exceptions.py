class WorkshopError(Exception):
    """Base class for exceptions in this module.
    
    Attributes:
        message: explanation of the error
    """
    def __init__(self):
        """Default constructor."""
        self.message = 'Undefined error.  See CloudWatch logs for more details.'


class DynamoServiceError(WorkshopError):
    """Exception raised for errors occurring during DynamoService boto3 service wrapper operations."""
    def __init__(self, client_error_code, message):
        """Default constructor.
        
        Args:
            client_error_code: error code raised by failed boto3 operation
            message: message to be logged
        """
        self.message = f"{self.__class__.__name__}: Exception '{client_error_code}' raised: {message}"


class EmptyDynamoResultError(WorkshopError):
    """Exception raised for empty DynamoDB query response."""
    def __init__(self, table_name, partition_key=None, search_value=None):
        """Default constructor.
        
        Args:
            table_name: the name of the table queried
            partition_key: the partition key used for the query, defaults to None
            search_value: the value searched for, defaults to None
        """
        if partition_key is None:
            self.message = f"{self.__class__.__name__}: Empty DynamoDB response received: scan of table '{table_name}' returned empty response."
        else:
            self.message = f"{self.__class__.__name__}: Empty DynamoDB response received: No key '{partition_key}' with value '{search_value}' in table '{table_name}'"


class EmptyEventValue(WorkshopError):
    """Exception raised for empty values passed to event."""
    def __init__(self, key):
        """Default constructor.
        
        Args:
            key: the key referencing an empty value
        """
        self.message = f"{self.__class__.__name__}: Key '{key}' in received event references empty value"


class EventValidationError(WorkshopError):
    """Exception raised for errors in parameters passed to Lambda."""
    def __init__(self, key, value, constraint):
        """Default constructor.
        
        Args:
            key: the invalid event key
            value: the invalid event value
            constraint: the constraint for the given key
        """
        self.message = f"{self.__class__.__name__}: Value '{value}' at key '{key}' failed to satisfy constraint: {constraint}"


class MissingEventKeyError(WorkshopError):
    """Exception raised for missing required key within Lambda event."""
    def __init__(self, key):
        """Default constructor.
        
        Args:
            key: the missing key
        """
        self.message = f"{self.__class__.__name__}: Key '{key}' is missing from received event"
