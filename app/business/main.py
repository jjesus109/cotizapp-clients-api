import logging

from app.config import Config
from app.connections import create_connection, create_producer
from app.infrastructure.repository import Repository
from app.adapters.gateway import Gateway
from app.entities.models import (
    Client,
    ClientUpdate
)

from app.errors import ElementNotFoundError, DBConnectionError

import uvicorn
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, status

conf = Config()
app = FastAPI()
log = logging.getLogger(__name__)
nosql_connection = create_connection()
messaging_conn = create_producer()
gateway = Gateway(
    Repository(
        nosql_connection,
        messaging_conn
    )
)


@app.get("/api/v1/clients")
async def get_clients(word_to_search: str):
    try:
        clients = await gateway.search_client(word_to_search)
    except (ElementNotFoundError, DBConnectionError) as e:
        log.error(f"Could not find the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not finde the client"
        )
    except Exception as e:
        log.error(f"Could not find the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not search the serviclientce"
        )
    return clients


@app.get("/api/v1/clients/{client_id}")
async def get_client(client_id: str):
    try:
        client = await gateway.get_client_data(client_id)
    except (ElementNotFoundError, DBConnectionError) as e:
        log.error(f"Could not find the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the client"
        )
    except Exception as e:
        log.error(f"Could not find the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the client"
        )
    return client


@app.post(
        "/api/v1/clients",
        response_description="Add new client",
        response_model=Client)
async def create_client(client: Client):
    try:
        client = await gateway.create_client(client)
    except (ElementNotFoundError, DBConnectionError) as e:
        log.error(f"Could not create the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could create the client"
        )
    except Exception as e:
        log.error(f"Could not create the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create the client"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=client
    )


@app.patch("/api/v1/clients/{client_id}")
async def modify_client(client_id: str, client: ClientUpdate):
    try:
        client = await gateway.update_client(client_id, client)
    except (ElementNotFoundError, DBConnectionError) as e:
        log.error(f"Could not update the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could update the client"
        )
    except Exception as e:
        log.error(f"Could not update the client: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update the client"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=client
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
