FROM alpine:latest AS build

RUN apk add udev openjdk21-jre python3 py3-pip py3-boto3

WORKDIR /server

# Copy build minecraft server files
COPY src /server

EXPOSE 25565

# Run the minecraft server
CMD ["java", "-Xmx1024M", "-Xms1024M", "-jar", "/server/server.jar", "nogui"]
