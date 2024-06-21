from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_UBOT

mongo_client = AsyncIOMotorClient(MONGO_UBOT)

mongodb = mongo_client.ubot

afkdb = mongodb.afk
gbandb = mongodb.gban
blgcastdb = mongodb.blgcast
logsdb = mongodb.logger
loggerdb = mongodb.logchat
permitdb = mongodb.pmpermit
approvdb = mongodb.approv
guarddb = mongodb.guard
pmmsgdb = mongodb.pmmsg
postdb = mongodb.post
prefixeddb = mongodb.prefix
varsdb = mongodb.vars
cekfilterdb = mongodb.cekfilter
welcomedb = mongodb.welcome
welcomecekdb = mongodb.welcomecek
welcometextdb = mongodb.welcometext


# PLUGINS DB


# afk
async def go_afk(user_id: int, time, reason=""):
    user_data = await afkdb.find_one({"user_id": user_id})
    if user_data:
        await afkdb.update_one(
            {"user_id": user_id},
            {"$set": {"afk": True, "time": time, "reason": reason}},
        )
    else:
        await afkdb.insert_one(
            {"user_id": user_id, "afk": True, "time": time, "reason": reason}
        )


async def no_afk(user_id: int):
    await afkdb.delete_one({"user_id": user_id, "afk": True})


async def check_afk(user_id: int):
    user_data = await afkdb.find_one({"user_id": user_id, "afk": True})
    return user_data


# gbandb
async def get_gban_user(user_id):
    user = await gbandb.find_one({"user_id": user_id})
    if not user:
        return []
    return user["gbnid"]


async def add_gban_user(user_id, gban_id):
    gbnid = await get_gban_user(user_id)
    gbnid.append(gban_id)
    await gbandb.update_one(
        {"user_id": user_id}, {"$set": {"gbnid": gbnid}}, upsert=True
    )
    return True


async def remove_gban_user(user_id, gban_id):
    gbnid = await get_gban_user(user_id)
    gbnid.remove(gban_id)
    await gbandb.update_one(
        {"user_id": user_id}, {"$set": {"gbnid": gbnid}}, upsert=True
    )
    return True


# gcastdb
async def get_gbl(user_id):
    user = await blgcastdb.find_one({"user_id": user_id})
    if not user:
        return []
    return user["gbl"]


async def add_gbl(user_id, chat_id):
    gbl = await get_gbl(user_id)
    if chat_id not in gbl:
        gbl.append(chat_id)
        await blgcastdb.update_one(
            {"user_id": user_id}, {"$set": {"gbl": gbl}}, upsert=True
        )


async def remove_gbl(user_id, chat_id):
    gbl = await get_gbl(user_id)
    if chat_id in gbl:
        gbl.remove(chat_id)
        await blgcastdb.update_one(
            {"user_id": user_id}, {"$set": {"gbl": gbl}}, upsert=True
        )


# loggerdb
async def get_user_logs(user_id):
    logs = await logsdb.find_one({"_id": user_id})
    if not logs:
        return "off"
    return logs["log"]


async def add_user_logs(user_id, log):
    await logsdb.update_one({"_id": user_id}, {"$set": {"log": log}}, upsert=True)


# logschatdb
async def get_chat_logs(user_id):
    logs = await loggerdb.find_one({"user_id": user_id})
    if not logs:
        return None
    return logs["log"]


async def add_chat_logs(user_id, log):
    await loggerdb.update_one({"user_id": user_id}, {"$set": {"log": log}}, upsert=True)


# pmpermitdb
async def set_pm_limit(user_id, limit):
    await permitdb.update_one({"_id": user_id}, {"$set": {"limit": limit}}, upsert=True)


async def get_pm_limit(user_id):
    limits = await permitdb.find_one({"_id": user_id})
    if not limits:
        return 5
    return limits["limit"]


async def approve_user(user_id, user):
    await approvdb.insert_one({"user_id": user_id, "user": user})


async def disapprove_user(user_id, user):
    await approvdb.delete_one({"user_id": user_id, "user": user})


async def is_user_approved(user_id, user):
    r = await approvdb.find_one({"user_id": user_id, "user": user})
    if r:
        return r
    else:
        return False


async def add_pmmsg(user_id, pm_id):
    await pmmsgdb.update_one({"_id": user_id}, {"$set": {"pm_id": pm_id}}, upsert=True)


async def get_pmmsg(user_id):
    pmmsg = await pmmsgdb.find_one({"_id": user_id})
    if not pmmsg:
        return None
    return pmmsg["pm_id"]


async def add_guard(user_id, guard):
    await guarddb.update_one({"_id": user_id}, {"$set": {"guard": guard}}, upsert=True)


async def get_guard(user_id):
    guards = await guarddb.find_one({"_id": user_id})
    if not guards:
        return "off"
    return guards["guard"]


# postdb
async def get_post(user_id):
    user = await postdb.find_one({"user_id": user_id})
    if not user:
        return []
    return user["post"]


async def add_post(user_id, chat_id):
    post = await get_post(user_id)
    post.append(chat_id)
    await postdb.update_one({"user_id": user_id}, {"$set": {"post": post}}, upsert=True)
    return True


async def remove_post(user_id, chat_id):
    post = await get_post(user_id)
    post.remove(chat_id)
    await postdb.update_one({"user_id": user_id}, {"$set": {"post": post}}, upsert=True)
    return True


# prefixeddb
async def get_pref(user_id):
    sh = await prefixeddb.users.find_one({"_id": user_id})
    if sh:
        return sh.get("prefixesi")
    else:
        return ["!", ".", "-", "^"]


async def set_pref(user_id, prefix):
    await prefixeddb.users.update_one(
        {"_id": user_id}, {"$set": {"prefixesi": prefix}}, upsert=True
    )


async def rem_pref(user_id):
    await prefixeddb.users.update_one(
        {"_id": user_id}, {"$unset": {"prefixesi": ""}}, upsert=True
    )


# varsdb
async def set_vars(bot_id, vars_name, value, query="vars"):
    update_data = {"$set": {f"{query}.{vars_name}": value}}
    await varsdb.update_one({"_id": bot_id}, update_data, upsert=True)


async def get_vars(bot_id, vars_name, query="vars"):
    result = await varsdb.find_one({"_id": bot_id})
    return result.get(query, {}).get(vars_name, None) if result else None


async def remove_vars(bot_id, vars_name, query="vars"):
    remove_data = {"$unset": {f"{query}.{vars_name}": ""}}
    await varsdb.update_one({"_id": bot_id}, remove_data)


async def all_vars(user_id, query="vars"):
    result = await varsdb.find_one({"_id": user_id})
    return result.get(query) if result else None


async def remove_all_vars(bot_id):
    await varsdb.delete_one({"_id": bot_id})


async def get_list_from_vars(user_id, vars_name, query="vars"):
    vars_data = await get_vars(user_id, vars_name, query)
    return [int(x) for x in str(vars_data).split()] if vars_data else []


async def add_to_vars(user_id, vars_name, value, query="vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    vars_list.append(value)
    await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)


async def remove_from_vars(user_id, vars_name, value, query="vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value in vars_list:
        vars_list.remove(value)
        await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)


# cekfilter
async def cek_filter(user_id):
    cek = await cekfilterdb.find_one({"_id": user_id})
    if not cek:
        return "off"
    return cek["cek_filter"]


async def set_filter(user_id, cek_filter):
    await cekfilterdb.update_one(
        {"_id": user_id}, {"$set": {"cek_filter": cek_filter}}, upsert=True
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
