import boto3.exceptions
from fastapi import FastAPI, Response
from app.models import ContainerBlueprint, UserInput
from app.generate_config import generate_config
from app.generate_presigned_url import generate_presigned_url
from app.hash import hash_password
import boto3
import hashlib

app = FastAPI()

@app.get("/")
async def read_root():
    return "Server is running..."

@app.post("/gen")
async def gen(blueprint: ContainerBlueprint, response: Response):

    try:
        # Dummy user_id and api_key (non_aws)
        user_id = "dbe47166-0a87-41c7-b445-d9d7bb25d178"
        api_key = "b73d5940-09d8-412a-a2b5-e9a2b8690b8a"

        if blueprint.user_id != user_id or blueprint.key != api_key:
            response.status_code = 401
            return None
        
        ec2 = boto3.client('ec2')

        push_backup_url="will be generated"
        pull_backup_url="will be generated"

        region="eu-north-1"
        ecr_repository_uri = "dummy ecr_repository_uri"
        docker_image = "dummy image"
        ec2_ami_id = 'ami-12345678'
        instance_type = 't2.micro'
        key_name = 'my-key-pair'

        config = generate_config(
            user_id=user_id, # user_id (user who wants to rent instance)
            push_backup_url=push_backup_url,
            pull_backup_url=pull_backup_url,
            region=region,
            ecr_repository_uri=ecr_repository_uri,
            docker_image=docker_image,
            ec2_ami_id=ec2_ami_id,
            instance_type=instance_type,
            key_name=key_name
        )

        response = ec2.run_instances(**config)

        response.status_code = 200
        return None
    except boto3.exceptions.Boto3Error:
        response.status_code = 500
        return None
    except:
        response.status_code = 500
        return None

@app.post("/generate_push_backup_url")
async def generate_push_backup_url(user: UserInput, response: Response):
    try:
        # "### passw0rd"
        if user.email == "test@gmail.com" and user.password == "### passw0rd":
            # Make db call for user_id
            # Then
            response.status_code = 200
            return generate_presigned_url("12345678")

        response.status_code = 500
        return None
    except Exception as e:
        response.status_code = 500
        print(f"{e}")
        return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
