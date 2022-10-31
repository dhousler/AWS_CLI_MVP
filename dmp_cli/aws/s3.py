from dmp_cli.aws.sessions import Session
import botocore


class S3I(Session):  # is a relationship
    def __init__(self, aws_region, aws_service, aws_profile):
        super().__init__(aws_region, aws_service, aws_profile)

        self.resource = super().set_resource()
        self.client = super().set_client()

    def list_buckets(self):
        buckets = [bucket.name for bucket in self.resource.buckets.all()]

        return buckets

    def list_bucket_keys(self, bucket):

        keys = []

        s3_bucket = self.resource.Bucket(bucket)

        # need to add a check here!

        for s3_bucket_object in s3_bucket.objects.all():
            # print(s3_bucket_object.key)
            if s3_bucket_object.key.endswith("/"):  # skip all keys that end with / so only get files
                pass
            else:
                keys += [s3_bucket_object.key]

        return keys

    def check_bucket_key(self, bucket, key):

        try:
            self.resource.Object(bucket, key).load()

        except botocore.exceptions.ClientError as e:

            if e.response['Error']['Code'] == "404":
                result = f'Does not exist'

            else:
                print("Error occurred during key lookup from S3.")

        else:
            result = "Exists"

        return result

    def get_head_object(self, bucket, key):
        s = self.client.head_object(Bucket=bucket, Key=key)

        rc = s['ResponseMetadata']['HTTPStatusCode']
        if rc < 200 or rc >= 300:
            raise RuntimeError("Call to get_head_object failed: ", rc)

        return s

    def check_bucket_encryption(self, bucket, sse_s3=False):
        """Check that the named bucket is encrypted with SSE-S3 only. Throw an exception otherwise"""

        s = self.client.get_bucket_encryption(Bucket=bucket)

        rc = s['ResponseMetadata']['HTTPStatusCode']
        if rc < 200 or rc >= 300:
            raise RuntimeError("Call to get_bucket_encryption failed: ", rc)

        try:
            key = s['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault'][
                'SSEAlgorithm']
        except BaseException as e:
            # logger.error(s)
            print("Bucket probably not encrypted with SSE-S3")
            raise e

        if sse_s3 and key != 'AES256':
            # logger.error(s)
            raise RuntimeError("Bucket not encrypted with SSE-S3. Expecting 'AES256', got: ", key)

        return key

    def get_encrypted_buckets(self, encryption_type):

        # logger.info("Retrieving bucket list using s3 resource ")

        buckets = [bucket.name for bucket in self.resource.buckets.all()
                   if self.check_bucket_encryption(bucket=bucket.name, sse_s3=False) == encryption_type]

        return buckets

    def check_bucket_notification(self, bucket):
        """Check if the named bucket is notifying any downstream source of events"""

        s = self.client.get_bucket_notification_configuration(Bucket=bucket)

        rc = s['ResponseMetadata']['HTTPStatusCode']
        if rc < 200 or rc >= 300:
            raise RuntimeError("Call to check_bucket_notification failed: ", rc)

        return s

    def upload_file_to_bucket(self, bucket, file_path, key):
        # https: // www.stackvidhya.com / write - a - file - to - s3 - using - boto3 /
        self.resource.Bucket(bucket).upload_file(file_path, key)
        print(f'Uploaded: {bucket}/{key}')

        return None

    def download_file_from_bucket(self, bucket, key, file_path):
        #  https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/s3-example-download-file.html
        try:
            self.resource.Bucket(bucket).download_file(key, file_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

        return None


class S3C:  # part of relationship
    description = "Uses resource session to set aws s3 calls."

    def __init__(self, aws_region, aws_service, aws_profile):
        self.aws_region = aws_region
        self.aws_service = aws_service
        self.aws_profile = aws_profile
        self.obj_session_resource = Session(aws_region, aws_service, aws_profile).set_resource()
        self.obj_session_client = Session(aws_region, aws_service, aws_profile).set_client()

    def list_buckets(self):
        buckets = [bucket.name for bucket in self.obj_session_resource.buckets.all()]

        return buckets
