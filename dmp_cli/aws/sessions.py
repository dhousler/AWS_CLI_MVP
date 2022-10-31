import boto3 as boto3
from botocore.config import Config


class Session:

    description = "Sets the boto3 session, using region, service and profile"

    def __init__(self, aws_region, aws_service, aws_profile):  # init (initialize) constructs a new oject from the class
        # instance attributes (properties|nouns)
        self.aws_region = aws_region
        self.aws_service = aws_service
        self.aws_profile = aws_profile

        self.config = Config(region_name=self.aws_region)
        self.b3session = boto3.Session(profile_name=self.aws_profile)

    # instance method is a function that belongs to a class

    def set_resource(self):
        r = self.b3session.resource(self.aws_service, config=self.config)
        return r

    def set_client(self):
        c = self.b3session.client(self.aws_service, config=self.config)
        return c





