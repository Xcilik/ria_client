from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_BOT

# function database
mongo_client = AsyncIOMotorClient(MONGO_BOT)
mongodb = mongo_client.bot

# variable
# bot
sudoersdb = mongodb.akses
usersdb = mongodb.broadcast
resell = mongodb.seller
selerbuyerdb = mongodb.getsellerbuyer


# client
prefixbotdb = mongodb.prefixdbbot
notesbuttondb = mongodb.notesbutton
collection = mongodb.notes
filtertextdb = mongodb.filtertext
filterbuttondb = mongodb.filterbutton
secretbuttondb = mongodb.secretbutton
welcomedb = mongodb.welcome
welcomecekdb = mongodb.welcomecek
welcometextdb = mongodb.welcometext



# notesbutton
async def save_note_button(user_id, note_name, note_button):
    doc = {"user_id": user_id, "notesbutton": {note_name: note_button}}
    result = await notesbuttondb.find_one({"user_id": user_id})
    if result:
        await notesbuttondb.update_one(
            {"user_id": user_id},
            {"$set": {f"notesbutton.{note_name}": note_button}},
            upsert=True,
        )
    else:
        await notesbuttondb.insert_one(doc)


async def get_note_button(user_id, note_name):
    result = await notesbuttondb.find_one({"user_id": user_id})
    if result is not None:
        try:
            note_button = result["notesbutton"][note_name]
            return note_button
        except KeyError:
            return None
    else:
        return None


async def rm_note_button(user_id, note_name):
    await notesbuttondb.update_one(
        {"user_id": user_id}, {"$unset": {f"notesbutton.{note_name}": ""}}
    )


async def rm_all_note_button(user_id):
    await notesbuttondb.update_one(
        {"user_id": user_id}, {"$unset": {"notesbutton": ""}}
    )


# notestext
async def save_note(user_id, note_name, note_id):
    doc = {"user_id": user_id, "notes": {note_name: note_id}}
    result = await collection.find_one({"user_id": user_id})
    if result:
        await collection.update_one(
            {"user_id": user_id},
            {"$set": {f"notes.{note_name}": note_id}},
            upsert=True,
        )
    else:
        await collection.insert_one(doc)


async def get_note(user_id, note_name):
    result = await collection.find_one({"user_id": user_id})
    if result is not None:
        try:
            note_id = result["notes"][note_name]
            return note_id
        except KeyError:
            return None
    else:
        return None


async def rm_note(user_id, note_name):
    await collection.update_one(
        {"user_id": user_id}, {"$unset": {f"notes.{note_name}": ""}}
    )


async def all_notes(user_id):
    results = await collection.find_one({"user_id": user_id})
    try:
        notes_dic = results["notes"]
        key_list = notes_dic.keys()
        return key_list
    except:
        return None


async def rm_all(user_id):
    await collection.update_one({"user_id": user_id}, {"$unset": {"notes": ""}})


# filter text
async def save_filter(user_id, filter_name, filter_id):
    doc = {"user_id": user_id, "filter": {filter_name: filter_id}}
    result = await filtertextdb.find_one({"user_id": user_id})
    if result:
        await filtertextdb.update_one(
            {"user_id": user_id},
            {"$set": {f"filter.{filter_name}": filter_id}},
            upsert=True,
        )
    else:
        await filtertextdb.insert_one(doc)


async def get_filter(user_id, filter_name):
    result = await filtertextdb.find_one({"user_id": user_id})
    if result is not None:
        try:
            filter_id = result["filter"][filter_name]
            return filter_id
        except KeyError:
            return None
    else:
        return None


async def rm_filter(user_id, filter_name):
    await filtertextdb.update_one(
        {"user_id": user_id}, {"$unset": {f"filter.{filter_name}": ""}}
    )


async def all_filter(user_id):
    results = await filtertextdb.find_one({"user_id": user_id})
    try:
        filter_dic = results["filter"]
        key_list = filter_dic.keys()
        return key_list
    except:
        return None


async def rm_all_filter(user_id):
    await filtertextdb.update_one({"user_id": user_id}, {"$unset": {"filter": ""}})


# filter button
async def save_filter_button(user_id, filter_name, filter_button):
    doc = {"user_id": user_id, "filterbutton": {filter_name: filter_button}}
    result = await filterbuttondb.find_one({"user_id": user_id})
    if result:
        await filterbuttondb.update_one(
            {"user_id": user_id},
            {"$set": {f"filterbutton.{filter_name}": filter_button}},
            upsert=True,
        )
    else:
        await filterbuttondb.insert_one(doc)


async def get_filter_button(user_id, filter_name):
    result = await filterbuttondb.find_one({"user_id": user_id})
    if result is not None:
        try:
            filter_button = result["filterbutton"][filter_name]
            return filter_button
        except KeyError:
            return None
    else:
        return None


async def rm_filter_button(user_id, filter_name):
    await filterbuttondb.update_one(
        {"user_id": user_id}, {"$unset": {f"filterbutton.{filter_name}": ""}}
    )


async def rm_all_filter_button(user_id):
    await filterbuttondb.update_one(
        {"user_id": user_id}, {"$unset": {"filterbutton": ""}}
    )


# broadcastbot
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})


# akses database
async def get_prem():
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]


async def add_prem(user_id):
    sudoers = await get_prem()
    if user_id not in sudoers:
        sudoers.append(user_id)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )


async def remove_prem(user_id):
    sudoers = await get_prem()
    if user_id in sudoers:
        sudoers.remove(user_id)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )


# selerdb database
async def get_seles():
    seles = await resell.find_one({"seles": "seles"})
    if not seles:
        return []
    return seles["reseller"]


async def add_seles(user_id):
    reseller = await get_seles()
    reseller.append(user_id)
    await resell.update_one(
        {"seles": "seles"}, {"$set": {"reseller": reseller}}, upsert=True
    )
    return True


async def remove_seles(user_id):
    reseller = await get_seles()
    reseller.remove(user_id)
    await resell.update_one(
        {"seles": "seles"}, {"$set": {"reseller": reseller}}, upsert=True
    )
    return True


# sellerbuyer database
async def add_seller_buyer(user_id, seler_id):
    await selerbuyerdb.update_one(
        {"_id": user_id}, {"$set": {"seler_id": seler_id}}, upsert=True
    )


async def get_seller_buyer(user_id):
    selerbuyer = await selerbuyerdb.find_one({"_id": user_id})
    if not selerbuyer:
        return None
    return selerbuyer["seler_id"]


async def remove_seller_buyer(user_id):
    await selerbuyerdb.delete_one({"_id": user_id})


# prefixbotdb database
async def get_prefix_bot(user_id):
    sh = await prefixbotdb.users.find_one({"_id": user_id})
    if sh:
        return sh.get("prefixesi")
    else:
        return ["!", ".", "-", "^"]


async def set_prefix_bot(user_id, prefix):
    await prefixbotdb.users.update_one(
        {"_id": user_id}, {"$set": {"prefixesi": prefix}}, upsert=True
    )


# secret message database
async def save_secret_button(user_id, secret_name, secret_button):
    doc = {"user_id": user_id, "secretbutton": {secret_name: secret_button}}
    result = await secretbuttondb.find_one({"user_id": user_id})
    if result:
        await secretbuttondb.update_one(
            {"user_id": user_id},
            {"$set": {f"secretbutton.{secret_name}": secret_button}},
            upsert=True,
        )
    else:
        await secretbuttondb.insert_one(doc)


async def get_secret_button(user_id, secret_name):
    result = await secretbuttondb.find_one({"user_id": user_id})
    if result is not None:
        try:
            secret_button = result["secretbutton"][secret_name]
            return secret_button
        except KeyError:
            return None
    else:
        return None


async def rm_secret_button(user_id, secret_name):
    await secretbuttondb.update_one(
        {"user_id": user_id}, {"$unset": {f"secretbutton.{secret_name}": ""}}
    )


async def rm_all_secret_button(user_id):
    await secretbuttondb.update_one(
        {"user_id": user_id}, {"$unset": {"secretbutton": ""}}
    )



# welcome
async def get_wlcm(user_id):
    user = await welcomedb.find_one({"user_id": user_id})
    if not user:
        return []
    return user["wlcm"]


async def clear_wlcm(user_id):
    user = await welcomedb.find_one({"user_id": user_id})
    if user:
        await welcomedb.update_one(
            {"user_id": user_id}, {"$set": {"wlcm": []}}, upsert=True
        )
    return True


async def add_wlcm(user_id, chat_id):
    wlcm = await get_wlcm(user_id)
    wlcm.append(chat_id)
    await welcomedb.update_one(
        {"user_id": user_id}, {"$set": {"wlcm": wlcm}}, upsert=True
    )
    return True


async def remove_wlcm(user_id, chat_id):
    wlcm = await get_wlcm(user_id)
    wlcm.remove(chat_id)
    await welcomedb.update_one(
        {"user_id": user_id}, {"$set": {"wlcm": wlcm}}, upsert=True
    )
    return True


async def cek_wlcm(user_id):
    cek = await welcomecekdb.find_one({"user_id": user_id})
    if not cek:
        return "off"
    return cek["cek_wlcm"]


async def set_wlcm(user_id, cek_wlcm):
    await welcomecekdb.update_one(
        {"user_id": user_id}, {"$set": {"cek_wlcm": cek_wlcm}}, upsert=True
    )


async def add_wlcm_text(user_id, wlcm_text):
    await welcometextdb.update_one(
        {"user_id": user_id}, {"$set": {"wlcm_text": wlcm_text}}, upsert=True
    )


async def get_wlcm_text(user_id):
    pmmsg = await welcometextdb.find_one({"user_id": user_id})
    if not pmmsg:
        return None
    return pmmsg["wlcm_text"]
