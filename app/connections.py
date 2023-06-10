from app.config import Config
from app.errors import DBConnectionError

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from confluent_kafka import Producer
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
)

conf = Config()


def create_connection() -> AsyncIOMotorDatabase:
    url_connection = conf.mongodb_url
    database_name = conf.mongo_db
    try:
        client = AsyncIOMotorClient(url_connection)
    except (ConfigurationError, ConnectionFailure) as e:
        raise DBConnectionError(
            f"Could not connect to database due to: {e}"
        )
    return client[database_name]


def create_producer() -> Producer:

    kafka_conf = {
        "bootstrap.servers": conf.kafka_server,
        "security.protocol": conf.kafka_protocol,
        "sasl.mechanisms": conf.sasl_mechanism,
        "sasl.username": conf.sasl_username,
        "sasl.password": conf.sasl_pass,
    }
    return Producer(kafka_conf)
