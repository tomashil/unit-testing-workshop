import boto3
from boto3.dynamodb.conditions import Key

from workshop_exceptions.exceptions import DynamoServiceError
from workshop_exceptions.exceptions import EmptyDynamoResultError

class DynamoService:
    """Functionality package for boto3 DynamoDB service operations.
    
    Attributes:
        resource: boto3 DynamoDB resource
        table: boto3 DynamoDB Table
        table_name: name of table
        partition_key: partition key of table
        sort_key: sort_key of table, defaults to None
    """
    def __init__(
            self,
            table_name,
            partition_key,
            sort_key=None
        ):
        """Default constructor.

        Args:
            table_name: name of table
            partition_key: partition key of table
            sort_key: sort_key of table, defaults to None
        """
        self.table_name = table_name
        self.resource = boto3.resource('dynamodb')
        self.table = self.resource.Table(self.table_name)
        self.partition_key = partition_key
        self.sort_key = sort_key

    def query(self, search_key):
        """Performs boto3 query given a value to search for within table.
        
        Args:
            search_key: the key to query for
        
        Returns:
            The result of the query operation.

        Raises:
            DynamoServiceError if ClientError occurs during query operation
            EmptyDynamoResultError if query result is empty
        """
        try:
            result = self.table.query(
                KeyConditionExpression=Key(self.partition_key).eq(search_key)
            )['Items']
        except self.resource.client.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']

            raise DynamoServiceError(error_code, error_message)
            
        if len(result) == 0:
            raise EmptyDynamoResultError(self.table_name, self.partition_key, search_key)
            
        return result[0]

    def scan(self):
        """Performs boto3 table scan.
        
        Returns:
            Result of the table scan.

        Raises:
            EmptyDynamoResultError if scan result is empty
        """
        try:
            result = self.table.scan()['Items']
        except self.resource.client.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']

            raise DynamoServiceError(error_code, error_message)
        
        if len(result) == 0:
            raise EmptyDynamoResultError(self.table_name)
            
        return result
