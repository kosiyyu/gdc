##

```
docker build -t <tag_name> -f <dockerfile_name> .
```

```
docker run -d --name <container_name> -p 25565:25565 \
-e PUSH_BACKUP_URL="<push_backup_url>" \
-e PULL_BACKUP_URL="<pull_backup_url>" \
<image_name>
```

##

```
docker build -t m39 -f Dockerfile .

docker run -d --name m39_container -p 25565:25565 \
-e PUSH_BACKUP_URL="<push_backup_url>" \
-e PULL_BACKUP_URL="<pull_backup_url>" \
m39
```
