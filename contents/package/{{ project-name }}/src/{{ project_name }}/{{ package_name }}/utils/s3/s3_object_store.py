import os
import boto3
import logging


class S3:
    """Wrapper around boto s3 features"""

    def __init__(self):

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.s3client = None
        self.session = None

    def authenticate_with_keys(self, access_key, secret_key, region):
        """Authenticate s3 credentials"""

        if not access_key:
            self.logger.error("AWS_ACCESS_KEY was not found.")
            return False

        if not secret_key:
            self.logger.error("AWS_SECRET_KEY was not found.")
            return False

        if not region:
            self.logger.error("AWS_REGION was not found.")
            return False

        try:
            self.session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )

            self.s3client = self.session.client("s3")
            self.logger.info("S3 authentication was successful.")
            return True

        except Exception as e:
            self.logger.error(e)
            raise

    def authenticate(self):
        """Authenticate s3 credentials"""

        # this method is used when service account is used

        try:
            self.session = boto3.Session()
            self.s3client = self.session.client("s3")
            self.logger.info("S3 authentication was successful.")
            return True

        except Exception as e:
            self.logger.error(e)
            raise

    def list_buckets(self):
        """List all s3 bucket"""

        # Note : you must have rights to enumerate buckets

        try:
            response = self.s3client.list_buckets()

            bucket_list = []

            # Output the bucket names
            for bucket in response["Buckets"]:
                bucket_list.append(bucket["Name"])

            return bucket_list

        except Exception as e:
            logging.error(e)
            raise

    def list_objects(self, bucket_name):
        """List contents of a s3 bucket"""

        # Note : you must have rights to enumerate objects

        try:
            response = self.s3client.list_objects(Bucket=bucket_name)

        except Exception as e:
            logging.error(e)
            raise

        if "Contents" not in response:
            return []

        file_list = []
        for obj in response["Contents"]:
            file_list.append(obj["Key"])

        return file_list

    def download_file(self, bucket_name, object_name, local_file_name):
        """Download object from a S3 bucket to a local file"""

        # Note : you must have rights to download objects

        try:
            self.logger.info(f"S3 : downloading bucket {bucket_name}  key {object_name} to {local_file_name}")
            self.s3client.download_file(bucket_name, object_name, local_file_name)
            return True

        except Exception as e:
            logging.error(e)
            return False

    def upload_file(self, local_file_name, bucket_name, object_name):
        """Upload a local file to a bucket"""

        # Note : you must have rights to upload objects

        try:
            self.logger.info(f"S3 : uploading local file {local_file_name} to bucket {bucket_name} key {object_name}")
            self.s3client.upload_file(local_file_name, bucket_name, object_name)
            return True

        except Exception as e:
            self.logger.error(e)
            return False

    def move_file(self, source_bucket_name, object_name, target_bucket_name):
        """Move an object between two buckets"""

        # Note : you must have rights to move objects

        try:
            copy_source = {"Bucket": source_bucket_name, "Key": object_name}
            self.s3client.copy_object(
                CopySource=copy_source, Bucket=target_bucket_name, Key=object_name
            )
            self.s3client.delete_object(Bucket=source_bucket_name, Key=object_name)

            return True

        except Exception as e:
            self.logger.error(e)
            return False
