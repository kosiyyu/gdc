def generate_config(
        user_id: str,
        push_backup_url: str,
        pull_backup_url: str,
        region: str,
        ecr_repository_uri: str,
        docker_image: str,
        ec2_ami_id: str,
        instance_type: str,
        key_name: str):
    container_name = ""

    script_text = f"""#!/bin/bash
    # Set environment variables
    echo "USER_ID={user_id}" >> /etc/environment
    echo "PUSH_BACKUP_URL={push_backup_url}" >> /etc/environment
    echo "PULL_BACKUP_URL={pull_backup_url}" >> /etc/environment

    # Authenticate with ECR
    aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {ecr_repository_uri}
    
    # Pull and run the Docker container
    docker pull {docker_image}
    docker run -d -e --name {container_name} -p 25565:25565 \
    -e PUSH_BACKUP_URL="{push_backup_url}" \
    -e PULL_BACKUP_URL="{pull_backup_url}" \
    {docker_image}
    """

    config = {
        "BlockDeviceMappings": [
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeType': 'gp3'
                },
            },
        ],
        'ImageId': ec2_ami_id,
        'InstanceType': instance_type,
        'MinCount': 1,
        'MaxCount': 1,
        'KeyName': key_name,
        'UserData': script_text,
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': f'MinecraftServer{user_id}'},
                    {'Key': 'UserId', 'Value': str(user_id)}
                ]
            }
        ]
    }
    
    return config