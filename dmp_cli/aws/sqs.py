import json
from dmp_cli.aws.sessions import Session


class SQS(Session):  # is a relationship
    def __init__(self, aws_region, aws_service, aws_profile):
        super().__init__(aws_region, aws_service, aws_profile)

        self.resource = super().set_resource()
        self.client = super().set_client()

    def get_queue_url(self, q_name):
        queue = self.resource.get_queue_by_name(QueueName=q_name)

        return queue.url  # .url extracts just url otherwise: sqs.Queue(url='https://url/path/...')

    def send_sqs(self, q_name, payload):

        queue = self.resource.get_queue_by_name(QueueName=q_name)
        response = queue.send_message(MessageBody=json.dumps(payload))

        rc = response['ResponseMetadata']['HTTPStatusCode']
        if rc < 200 or rc >= 300:
            raise RuntimeError("Call to send sqs failed: ", rc)

        return response
