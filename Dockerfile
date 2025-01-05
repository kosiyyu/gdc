FROM alpine:latest AS build

# RUN apk add udev openjdk21-jre python3 py3-pip gcc python3-dev musl-dev linux-headers
RUN apk add udev openjdk21-jre python3 py3-pip gcc python3-dev musl-dev linux-headers
RUN pip install --break-system-packages python-dotenv
RUN pip install --break-system-packages psutil

# Info:
# .--------------------------------------------------------------------------------.
# | .json files, server.properties and world will be provided when backup is loaded|
# | server.jar, eula.txt provided in container                                     |
# | all others files and folders will be created when server.jar is executed       |
# .--------------------------------------------------------------------------------.
# Copy build minecraft server files
COPY out /out
COPY env_loader /env_loader
COPY scripts /scripts
COPY .env_common .env_common

EXPOSE 25565

# Run the minecraft server
CMD ["python", "/scripts/run.py"]