from typing import Any, List
from dataclasses import dataclass

from app.entities.models import (
    MessageType,
    ClientDict,
    Client
)
from app.config import Config
from app.adapters.gateway_i import GatewayInterface
from app.infrastructure.repository_i import RepositoryInterface

from pydantic import BaseSettings
from fastapi.encoders import jsonable_encoder


@dataclass
class Gateway(GatewayInterface):

    repository: RepositoryInterface
    conf: BaseSettings = Config()

    async def get_client_data(self, client_id: int) -> ClientDict:
        return await self.repository.get_client_data(client_id)

    async def search_client(self, word: str) -> List[ClientDict]:
        return await self.repository.search_client(word)

    async def create_client(self, client: Client) -> ClientDict:
        if self.conf.stream_consume:
            service_type = MessageType.client
            await self.repository.notify(client, service_type)
            response = jsonable_encoder(client)
        else:
            response = await self.repository.create_service(client)
        return response

    async def update_client(self, client_id: str, client: Any) -> Any:
        if self.conf.stream_consume:
            client_got = await self.repository.get_client_data(client_id)
            client_model = Client(**client_got)
            new_client_data = client.dict(exclude_unset=True)
            updated_client = client_model.copy(update=new_client_data)
            client_type = MessageType.client
            await self.repository.notify(
                updated_client,
                client_type
            )
            updated_client = jsonable_encoder(updated_client)
        else:
            await self.repository.update_client(
                client_id,
                client
            )
            updated_client = await self.repository.get_client_data(
                client_id
            )
        return updated_client
