from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_CLIENT

mongo_client = AsyncIOMotorClient(MONGO_CLIENT)
mongodb = mongo_client.client

ubotdb = mongodb.ubotdb
clientdb = mongodb.clientdb


# isi data client
async def add_ubot(user_id, api_id, api_hash, session_string):
    return await ubotdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "api_id": api_id,
                "api_hash": api_hash,
                "session_string": session_string,
            }
        },
        upsert=True,
    )


async def get_userbots():
    data = []
    async for ubot in ubotdb.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(ubot["user_id"]),
                api_id=ubot["api_id"],
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
    return data


async def get_ubot(user_id):
    user_data = await ubotdb.find_one({"user_id": user_id})
    return user_data


async def remove_ubot(user_id):
    return await ubotdb.delete_one({"user_id": user_id})


# isi client
async def get_client():
    user_client = await clientdb.find_one({"client": "client"})
    if not user_client:
        return []
    return user_client["user_client"]


async def add_client(user_id):
    user_client = await get_client()
    if user_id not in user_client:
        user_client.append(user_id)
        await clientdb.update_one(
            {"client": "client"},
            {"$set": {"user_client": user_client}},
            upsert=True,
        )


async def remove_client(user_id):
    user_client = await get_client()
    if user_id in user_client:
        user_client.remove(user_id)
        await clientdb.update_one(
            {"client": "client"},
            {"$set": {"user_client": user_client}},
            upsert=True,
        )
