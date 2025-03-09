import os
from typing import TypedDict
from dotenv import load_dotenv

class EnvVariables(TypedDict):
    JAVA_VERSION: str
    SRC_PATH: str
    BINARY_FILENAME: str
    EULA_FILENAME: str
    BACKUP_FILENAME: str
    BACKUP_DIR: str
    LOG_FILENAME: str

    WORLD_DIR: str
    SERVER_PROPERTIES_FILENAME: str
    USERCACHE_FILENAME: str
    BANNED_PLAYERS_FILENAME: str
    BANNED_IPS_FILENAME: str
    WHITELIST_FILENAME: str
    OPS_FILENAME: str

def load_env() -> EnvVariables:
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env_common')

    load_dotenv(os.path.abspath(env_path), override=True)

    return EnvVariables(
        JAVA_VERSION = os.getenv("JAVA_VERSION", ""),
        SRC_PATH = os.getenv("SRC_PATH", ""),
        BINARY_FILENAME = os.getenv("BINARY_FILENAME", ""),
        EULA_FILENAME = os.getenv("EULA_FILENAME", ""),
        BACKUP_FILENAME = os.getenv("BACKUP_FILENAME", ""),
        BACKUP_DIR = os.getenv("BACKUP_DIR", ""),
        LOG_FILENAME = os.getenv("LOG_FILENAME", ""),

        WORLD_DIR = os.getenv("WORLD_DIR", ""),
        SERVER_PROPERTIES_FILENAME = os.getenv("SERVER_PROPERTIES_FILENAME", ""),
        USERCACHE_FILENAME = os.getenv("USERCACHE_FILENAME", ""),
        BANNED_PLAYERS_FILENAME = os.getenv("BANNED_PLAYERS_FILENAME", ""),
        BANNED_IPS_FILENAME = os.getenv("BANNED_IPS_FILENAME", ""),
        WHITELIST_FILENAME = os.getenv("WHITELIST_FILENAME", ""),
        OPS_FILENAME = os.getenv("OPS_FILENAME", ""),
    )

env = load_env()