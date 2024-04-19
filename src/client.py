"""
This module provides a flexible MQTT client application that can be configured via a JSON file.
The application reads the configuration, connects to an MQTT broker, subscribes to specified topics,
logs messages with timestamps, and optionally inserts data into a database
based on user configuration.

Attributes:
    CONFIG_PATH (Path): Path to the configuration JSON file.
"""

import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt
from pydantic import ValidationError

# Importing configuration models and logging setup
from src.core.config import Config, Database, read_config_from_json
from src.core.logger import setup_logging

CONFIG_PATH = Path(
    "path/to/your/config.json"
)  # Update this with the actual configuration file path


def on_connect(client: mqtt.Client, userdata: dict, flags, rc: int) -> None:
    """
    Callback for when the client receives a CONNACK response from the server.

    Args:
        client (mqtt.Client): The client instance for this callback.
        userdata (dict): The private user data as set in Client() or userdata_set().
        flags: Response flags sent by the broker.
        rc (int): The connection result.

    """
    logger: logging.Logger = userdata["logger"]
    logger.info("Connected with result code %s", rc)

    # Subscribe to topics from the configuration
    topics = [(topic.name, topic.qos) for topic in userdata["config"].topics]
    if topics:
        client.subscribe(topics)


def on_message(client: mqtt.Client, userdata: dict, msg: mqtt.MQTTMessage) -> None:
    """
    Callback for when a PUBLISH message is received from the server.

    Args:
        client (mqtt.Client): The client instance for this callback.
        userdata (dict): The private user data.
        msg (mqtt.MQTTMessage): An instance of MQTTMessage, which contains message details.

    """
    logger: logging.Logger = userdata["logger"]
    db_config: Database = userdata["config"].db
    msg_payload = msg.payload.decode("utf-8")
    # Timezone is UTC
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    logger.info("[%s] Message received on %s: %s", timestamp, msg.topic, msg_payload)

    # Optional: Insert into database if enabled
    if db_config and userdata.get("db_connection"):
        # This is a placeholder for actual database insertion logic, including a timestamp
        logger.info("[%s] Inserting data into database: %s", timestamp, msg_payload)


def run_client(config: Config, logger: logging.Logger) -> None:
    """
    Sets up and runs the MQTT client with the provided configuration and log_handler.

    Args:
        config (Config): The application configuration loaded from a JSON file.
        logger (logging.Logger): Configured logger for logging messages.

    """
    # MQTT client setup
    client = mqtt.Client(userdata={"logger": logger, "config": config})

    client.on_connect = on_connect
    client.on_message = on_message

    # Set MQTT credentials if provided
    if config.server_connection.username and config.server_connection.password:
        client.username_pw_set(
            config.server_connection.username,
            config.server_connection.password,
        )

    # Connect to MQTT broker
    client.connect(
        config.server_connection.host,
        config.server_connection.port,
        config.server_connection.keep_alive,
    )

    # Optional: Database connection
    if config.db:
        # Placeholder for database connection logic, including logging the timestamp of connection
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        logger.info("[%s] Connected to the database (placeholder)", timestamp)
        # Pass the database connection to the client userdata
        client.user_data_set({"db_connection": True})

    # Start the loop
    client.loop_forever()


def main(config_path: Path) -> None:
    """
    Main function to load the configuration, set up logging, and run the MQTT client.

    Args:
        config_path (Path): The path to the configuration JSON file.

    """
    # Setup logger
    logger = setup_logging()

    try:
        # Load and validate configuration
        config = read_config_from_json(config_path, logger)
        if config:
            run_client(config, logger)
        else:
            logger.error("Configuration could not be loaded or validated.")
    except FileNotFoundError:
        logger.exception("Configuration file not found: %s", config_path)
    except ValidationError:
        logger.exception("Configuration validation error.")
    except Exception as e:
        logger.critical("Unexpected error: %s", e, exc_info=True)


if __name__ == "__main__":
    main(CONFIG_PATH)
    sys.exit(0)
