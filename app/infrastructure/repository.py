import logging
from typing import List
from dataclasses import dataclass

from app.config import Config
from app.errors import (
    ElementNotFoundError,
    InsertionError,
    DBConnectionError
)
from app.entities.models import (
    MessageFormat,
    MessageType,
    ClientDict,
    Client
)
from app.infrastructure.repository_i import RepositoryInterface

from pydantic import BaseSettings
from confluent_kafka import Producer
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConnectionFailure,
    ExecutionTimeout
)


log = logging.getLogger(__name__)


@dataclass
class Repository(RepositoryInterface):

    nosql_conn: AsyncIOMotorDatabase
    messaging_con: Producer
    conf: BaseSettings = Config()

    async def get_client_data(self, client_id: int) -> ClientDict:
        try:
            client = await self.nosql_conn[self.conf.clients_collec].find_one(
                {"_id": client_id}
            )
        except (ConnectionFailure, ExecutionTimeout):
            raise DBConnectionError(
                "Client not found in DB"
            )
        if not client:
            raise ElementNotFoundError(
                "Client not found in DB"
            )
        return client

    async def search_client(self, word: str) -> List[ClientDict]:
        try:
            clients_get = await self.nosql_conn[self.conf.clients_collec].find(
                {
                    "name": {
                        "$regex": word,
                        "$options": "mxsi"
                    }
                }
            ).to_list(self.conf.max_search_elements)
        except (ConnectionFailure, ExecutionTimeout):
            raise DBConnectionError(
                "Could not found service in DB"
            )
        return clients_get

    async def create_client(self, client: Client) -> ClientDict:
        client = jsonable_encoder(client)
        try:
            await self.nosql_conn[self.conf.clients_collec].insert_one(
                client
            )
        except (ConnectionFailure, ExecutionTimeout):
            raise InsertionError("Could not insert service in DB")
        return client

    async def update_client(
        self,
        client_id: str,
        client: Client
    ) -> ClientDict:
        query = {"_id": client_id}
        values = {
            "$set": client.dict(exclude_unset=True)
        }
        try:
            await self.nosql_conn[self.conf.clients_collec].update_one(
                query,
                values
            )
        except (ConnectionFailure, ExecutionTimeout):
            raise InsertionError("Could not update services in DB")

    async def notify(
        self,
        client: Client,
        _type: MessageType
    ):
        message = MessageFormat(
            type=_type.value,
            content=client)
        self.messaging_con.produce(
            self.conf.kafka_topic,
            message.json(encoder=str).encode("utf-8")
        )
        self.messaging_con.flush()
