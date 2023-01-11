import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Form
from fastapi.routing import APIRoute
from starlette.requests import Request
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", default="mongodb://localhost:27017/database")


async def ping_pong():
    """Reference to Redis"""
    return {"ping": "pong"}


async def main_page():
    """Main page of the application"""
    return {"Hello": "You're on the Main page"}


async def create_record(request: Request, username: str = Form(...)) -> dict:
    """Create a record"""

    # establish the connection with mongo
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["database"]
    # put into collection `records` {"username": username}
    await mongo_client.records.insert_one({"username": username})

    return {"success": True}


async def get_records(request: Request) -> list:
    """Get all records in mongoDb"""

    # establish connection with mongo database
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["database"]

    # cursor is the collection and .find finds all records
    cursor = mongo_client.records.find({})
    res = []

    # get 100 records and run in for
    for document in await cursor.to_list(length=100):
        # fastapi can't convert ObjectId in mongo db to string or other type
        # then we need to convert _id to string
        document["_id"] = str(document["_id"])
        # add document - record
        res.append(document)

    return res


routes = [
    # main page
    APIRoute(path="/", endpoint=main_page, methods=["GET"]),
    # ping/pong
    APIRoute(path="/ping", endpoint=ping_pong, methods=["GET"]),
    # urls for mongo
    APIRoute(path="/create_record", endpoint=create_record, methods=["POST"]),
    APIRoute(path="/get_records", endpoint=get_records, methods=["GET"]),
]

# client for connect with mongo
client = AsyncIOMotorClient(MONGODB_URL)

# fastapi application
app = FastAPI()
# set state mongo client
app.state.mongo_client = client
# include our routers
app.include_router(APIRouter(routes=routes))

if __name__ == "__main__":
    # start application
    uvicorn.run(app, host="0.0.0.0", port=8000)
