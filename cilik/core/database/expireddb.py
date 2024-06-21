from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_EXPIRED

# function database
mongo_client = AsyncIOMotorClient(MONGO_EXPIRED)
mongodb = mongo_client.expired

waktuhabisdb = mongodb.waktuhabis
habisdb = mongodb.habis


# expired database
async def get_date_end(user_id):
    user = await waktuhabisdb.users.find_one({"_id": user_id})
    if user:
        return user.get("date_id")
    else:
        return None


async def add_date_end(user_id, date_id):
    await waktuhabisdb.users.update_one(
        {"_id": user_id}, {"$set": {"date_id": date_id}}, upsert=True
    )


async def remove_date_end(user_id):
    await waktuhabisdb.users.update_one(
        {"_id": user_id}, {"$unset": {"date_id": ""}}, upsert=True
    )


# one day expired database
async def get_habis():
    dah_habis = await habisdb.find_one({"habis": "habis"})
    if not dah_habis:
        return []
    return dah_habis["dah_habis"]


async def add_habis(user_id):
    dah_habis = await get_habis()
    if user_id not in dah_habis:
        dah_habis.append(user_id)
        await habisdb.update_one(
            {"habis": "habis"}, {"$set": {"dah_habis": dah_habis}}, upsert=True
        )


async def remove_habis(user_id):
    dah_habis = await get_habis()
    if user_id in dah_habis:
        dah_habis.remove(user_id)
        await habisdb.update_one(
            {"habis": "habis"}, {"$set": {"dah_habis": dah_habis}}, upsert=True
        )
