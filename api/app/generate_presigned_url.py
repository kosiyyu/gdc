import os
import boto3
import datetime as dt

def generate_presigned_url(user_id: str) -> dict:
    client = boto3.client('s3')

    bucket_name = os.getenv("BUCKET_NAME")
    ttl_seconds = os.getenv("TTL_SECONDS")

    time_string = str(dt.datetime.now().timestamp()).replace(".", "")
    in_bucket_filename = f"user/{user_id}/url_created_at_{time_string}.tar.gz"

    response = client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': bucket_name,
            'Key': in_bucket_filename
        },
        ExpiresIn=ttl_seconds,
        HttpMethod='PUT'
    )

    return response