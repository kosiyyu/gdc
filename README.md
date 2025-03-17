# GDC - Game Distribution Controller

> Author: Karol Koś

## Overview

The Game Distribution Controller (GDC) is a side project of mine—an API for managing game servers with the help of a mobile application for easier access. The system leverages AWS infrastructure to provide game server provisioning and management.

> [!IMPORTANT]
> Currently, the implementation consists only of a **Minecraft Vanilla server**.

## System Components

GDC consists of two main components:

- **REST API**: Built on AWS, serving as the backend for server management operations.
- **Mobile Application**: A user interface for remotely controlling game server.

## Technologies

### Backend

- API Gateway
- Lambda
- ECS - Fargate
- ECR
- Docker
- Golang
- Python

### Mobile Application

- React Native
- TypeScript

> **Note:** Deployment automation will be added in the near future.

## Current Features

- Start and stop the game server on request.
- Check server existence and status.
- Retrieve the server's IP address for active instance.
- Automatically create a game world if run for the first time.
- Persistent worlds

## Planned Features

- **Backup and Restore:** Ability to back up Minecraft worlds and import/export them.
- **Additional Game Servers:** Support for **Don't Starve Together** and **Counter-Strike (Vanilla)**.

> [!NOTE]
> New game support will be added **only if I don't get bored with this project**.
