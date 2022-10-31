def get_fake_payload(head_objects, bucket, key):

    # Fake SQS payload
    event_time = str(head_objects['LastModified'])
    size = head_objects['ContentLength']
    etag = head_objects['ETag'].strip("\"")  # There are additional " on e-tag in some instances
    version_id = head_objects['VersionId']

    fake_payload = {"Records": [{"eventTime": event_time, "eventName": "ObjectCreated:Put",
                                 "s3": {"bucket": {"name": bucket}, "object": {"key": key,
                                                                               "size": size,
                                                                               "eTag": etag,
                                                                               "versionId": version_id}
                                        }
                                 }]
                    }

    return fake_payload
