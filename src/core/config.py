"""
Config Module.

Save your configuration in a JSON file matching the structure defined by the classes.
Then, read and validate the configuration as shown below:

    path = Path('path/to/your/config.json')
    server_connection, topics, db = read_config_from_json(path)

Note: Replace 'path/to/your/config.json' with the actual path to your JSON file.
"""

import json
import logging
from pathlib import Path

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class ServerConnection(BaseSettings):
    """
    Represents the server connection details required to establish a connection with a server.

    Attributes:
        host (str): The server's hostname or IP address.
        port (int): The port on which the server is running.
        username (str): Username for server authentication.
        password (str): Password for server authentication.
        keep_alive (int): Interval in seconds to keep the connection alive.

    Example:
        {
            "host": "example.com",
            "port": 22,
            "username": "user",
            "password": "pass",
            "keep_alive": 60
        }
    """

    host: str = Field(..., description="The server's hostname or IP address.")
    port: int = Field(..., description="The port on which the server is running.")
    username: str | None = Field(None, description="Username for server authentication.")
    password: str | None = Field(None, description="Password for server authentication.")
    keep_alive: int = Field(..., description="Interval in seconds to keep the connection alive.")


class Topic(BaseSettings):
    """
    Represents a topic for subscription or publication with specific Quality of Service (QoS) level.

    Attributes:
        name (str): The name of the topic.
        qos (int): Quality of Service level for the topic.

    Example:
        {
            "name": "sensor_data",
            "qos": 1
        }
    """

    name: str = Field(..., description="The name of the topic.")
    qos: int = Field(..., description="Quality of Service level for the topic.")


class Database(BaseSettings):
    """
    Represents the database connection details.

    Attributes:
        host (str): Database host.
        port (str): Database port.
        db_name (str): Name of the database.
        username (str): Username for database authentication.
        password (str): Password for database authentication.

    Example:
        {
            "host": "db.example.com",
            "port": "5432",
            "db_name": "mydatabase",
            "username": "dbuser",
            "password": "dbpass"
        }
    """

    host: str = Field(..., description="Database host.")
    port: str = Field(..., description="Database port.")
    db_name: str = Field(..., description="Name of the database.")
    username: str = Field(..., description="Username for database authentication.")
    password: str = Field(..., description="Password for database authentication.")


class Config(BaseSettings):
    """
    Main configuration class encapsulating server connection, topic subscriptions/publications,
    and database details.

    Attributes:
        server_connection (ServerConnection): Server connection details.
        topics (List[Topic]): List of topics to subscribe or publish.
        db (Database): Database connection details.
    """

    server_connection: ServerConnection = Field(..., description="Server connection details.")
    topics: list[Topic] = Field(..., description="List of topics to subscribe or publish.")
    db: Database | None = Field(None, description="Database connection details.")


def read_config_from_json(path: Path, logger: logging.Logger) -> Config | None:
    """
    Reads configuration from a JSON file and validates it against the defined Pydantic models.

    Parameters:
        path (Path): The Pathlib Path to the JSON configuration file.

    Returns:
        tuple: Tuple containing instances of ServerConnection, list of Topics, and Database,
        respectively.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValidationError: If the JSON does not match the schema defined by the Pydantic models.
        JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        config = Config.model_validate(data)
    except FileNotFoundError:
        logger.exception("Error: The file %s was not found.", path)
    except ValidationError:
        logger.exception("Validation Error.")
    except json.JSONDecodeError:
        logger.exception("Error: The file contains invalid JSON.")
    else:
        return config
