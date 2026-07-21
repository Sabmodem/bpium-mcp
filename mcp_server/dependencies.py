from api.client import BpiumClient
from contextlib import asynccontextmanager
import os
from load_dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def get_bpium_client():
    client = BpiumClient(os.getenv("URL"))
    await client.login_post(os.getenv("LOGIN"), os.getenv("PASSWORD"))
    try:
        yield client
    finally:
        await client.close()
