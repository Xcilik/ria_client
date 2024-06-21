from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_UTILS

# function database
mongo_client = AsyncIOMotorClient(MONGO_UTILS)
mongodb = mongo_client.utils

# variable
revokedb = mongodb.revoke
fontdb = mongodb.font
plandb = mongodb.plan

# pmpermit variable
pmpermitbuttondb = mongodb.pmpermitbutton
pmpermittextdb = mongodb.pmpermittextdb

# animation variable
animations_collection = mongodb.animasi_collection


# revoke database
async def get_revoke():
    revokers = await revokedb.find_one({"revoke": "revoke"})
    if not revokers:
        return []
    return revokers["revokers"]


async def add_revoke(user_id):
    revokers = await get_revoke()
    if user_id not in revokers:
        revokers.append(user_id)
        await revokedb.update_one(
            {"revoke": "revoke"}, {"$set": {"revokers": revokers}}, upsert=True
        )


async def remove_revoke(user_id):
    revokers = await get_revoke()
    if user_id in revokers:
        revokers.remove(user_id)
        await revokedb.update_one(
            {"revoke": "revoke"}, {"$set": {"revokers": revokers}}, upsert=True
        )


# plan database
async def add_plan(user_id, plan):
    await plandb.update_one({"user_id": user_id}, {"$set": {"plan": plan}}, upsert=True)


async def get_plan(user_id):
    plan = await plandb.find_one({"user_id": user_id})
    if not plan:
        return "small"
    return plan["plan"]


# font database
async def set_font(user_id, fonttext):
    await fontdb.update_one(
        {"user_id": user_id}, {"$set": {"fonttext": fonttext}}, upsert=True
    )


async def get_font(user_id):
    fonts = await fontdb.find_one({"user_id": user_id})
    if not fonts:
        return None
    return fonts["fonttext"]


# pmpermit button database
async def save_pmpermit_button(user_id, pmpermit_name, pmpermit_button):
    doc = {"user_id": user_id, "pmpermitbutton": {pmpermit_name: pmpermit_button}}
    result = await pmpermitbuttondb.find_one({"user_id": user_id})
    if result:
        await pmpermitbuttondb.update_one(
            {"user_id": user_id},
            {"$set": {f"pmpermitbutton.{pmpermit_name}": pmpermit_button}},
            upsert=True,
        )
    else:
        await pmpermitbuttondb.insert_one(doc)


async def get_pmpermit_button(user_id, pmpermit_name):
    result = await pmpermitbuttondb.find_one({"user_id": user_id})
    if result is not None:
        try:
            pmpermit_button = result["pmpermitbutton"][pmpermit_name]
            return pmpermit_button
        except KeyError:
            return None
    else:
        return None


async def rm_pmpermit_button(user_id, pmpermit_name):
    await pmpermitbuttondb.update_one(
        {"user_id": user_id}, {"$unset": {f"pmpermitbutton.{pmpermit_name}": ""}}
    )


# pmpermit text database
async def save_pmpermit(user_id, pmpermit_name, pmpermit_id):
    doc = {"user_id": user_id, "pmpermit": {pmpermit_name: pmpermit_id}}
    result = await pmpermittextdb.find_one({"user_id": user_id})
    if result:
        await pmpermittextdb.update_one(
            {"user_id": user_id},
            {"$set": {f"pmpermit.{pmpermit_name}": pmpermit_id}},
            upsert=True,
        )
    else:
        await pmpermittextdb.insert_one(doc)


async def get_pmpermit(user_id, pmpermit_name):
    result = await pmpermittextdb.find_one({"user_id": user_id})
    if result is not None:
        try:
            pmpermit_id = result["pmpermit"][pmpermit_name]
            return pmpermit_id
        except KeyError:
            return None
    else:
        return None


async def rm_pmpermit(user_id, pmpermit_name):
    await pmpermittextdb.update_one(
        {"user_id": user_id}, {"$unset": {f"pmpermit.{pmpermit_name}": ""}}
    )


# animation database
async def add_animation(user_id, name, steps):
    await animations_collection.update_one(
        {"user_id": user_id, "name": name}, {"$set": {"steps": steps}}, upsert=True
    )


async def delete_animation(user_id, name):
    result = await animations_collection.delete_one({"user_id": user_id, "name": name})
    return result.deleted_count > 0


async def get_animation(user_id, name):
    result = await animations_collection.find_one({"user_id": user_id, "name": name})
    return result["steps"] if result else None


async def get_all_animations(user_id):
    cursor = animations_collection.find({"user_id": user_id})
    animations = []
    async for anim in cursor:
        animations.append(anim["name"])
    return animations
