import logging
import datetime as dt
import boto3
from botocore.exceptions import ClientError

'''
description: Function goal is to generate a presigned URL and send the generated URL
to the sender based on the user_id

variables:
user_id -> user identifier 

constants:
BUCKET_NAME -> <your s3 bucket name>
TTL_SECONDS -> time to live in seconds (300s = 5min)
'''

BUCKET_NAME = "minecraftworldskosiyyuproto"
TTL_SECONDS = 300

def create_presigned_url(event, context):

    user_id: str = event.get("user_id", "")
    # FIXME: Create propper user_id check
    if len(user_id) <= 6:
        return {
            "statusCode": 400,
        }
    
    client = boto3.client('s3')
    
    # For example: "1735330036761159"
    time_string = str(dt.datetime.now().timestamp()).replace(".","")

    # Format: "user/<user_id>/url_created_at_<time_string>.tar.gz"
    in_bucket_filename = f"user/{user_id}/url_created_at_{time_string}.tar.gz"

    try:
        response = client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': in_bucket_filename
            },
            ExpiresIn=TTL_SECONDS,
            HttpMethod='PUT'
            )
        
    except ClientError as e:
        logging.error(e)
        return {
            "statusCode": 500,
        }


    return {
        "statusCode": 200,
        "body": response
    }
