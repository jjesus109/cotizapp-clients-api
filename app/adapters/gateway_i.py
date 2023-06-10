from typing import Any, List
from abc import ABC, abstractmethod


class GatewayInterface(ABC):

    @abstractmethod
    async def get_client_data(self, client_id: int) -> Any:
        """Get client data from DB

        Args:
            client_id (int): id to get data about the client

        Returns:
            Any: Client data got
        """

    @abstractmethod
    async def search_client(self, word: str) -> List[Any]:
        """Word to search into client catalog

        Args:
            word (str): word to search

        Returns:
            List[Any]: list of match product
        """

    @abstractmethod
    async def create_client(self, client: Any) -> Any:
        """Create client in DB

        Args:
            serclientvice (Any): client to create

        Returns:
            Any: Client created
        """

    @abstractmethod
    async def update_client(self, client_id: str, client: Any) -> Any:
        """Update client in DB

        Args:
            client_id (str): client id to update data
            client (Any): client to update

        Returns:
            Any: Client updated
        """
