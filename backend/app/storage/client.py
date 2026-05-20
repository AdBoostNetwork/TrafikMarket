import os

import aioboto3


def make_storage() -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
        aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
    )
