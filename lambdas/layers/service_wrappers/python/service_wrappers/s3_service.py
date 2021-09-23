import boto3

from workshop_exceptions.exceptions import S3DeleteObjectError

class S3Service:
    """Functionality package for boto3 S3 operations.

    Attributes:
        bucket_name: name of bucket
        resource: boto3 S3 resource
        bucket: boto3 S3 Bucket
    """
    def __init__(self, bucket_name):
        """Default constructor.

        Args:
            bucket_name: name of bucket
        """
        self.bucket_name = bucket_name
        self.resource = boto3.resource('s3')
        self.bucket = self.resource.Bucket(self.bucket_name)

    def delete_all(self):
        """Deletes all object in a bucket.
        
        Raises:
            S3DeleteObjectError: if client error in boto3 delete operation
        """
        try:
            for obj in self.bucket.objects.all():
                self.resource.Object(self.bucket.name, obj.key).delete()
        except self.resource.client.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']

            raise S3DeleteObjectError(error_code, error_message)
            