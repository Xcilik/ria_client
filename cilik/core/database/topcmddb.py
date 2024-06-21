from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_TOPCMD

# function database
mongo_client = AsyncIOMotorClient(MONGO_TOPCMD)
mongodb = mongo_client.topcmdbot

# variabel
topcmddb = mongodb.topcmd
sarandb = mongodb.saran


# Fungsi untuk mendapatkan semua saran dari database
async def get_saran():
    all_saran = sarandb.find()
    saran_list = [saran["text"] async for saran in all_saran]
    return saran_list


# Fungsi untuk menambahkan saran ke dalam database
async def add_saran(new_saran):
    existing_saran = await get_saran()
    existing_saran.append(new_saran)
    await sarandb.delete_many({})  # Menghapus semua dokumen lama
    for saran in existing_saran:
        await sarandb.insert_one({"text": saran})


# topcmd database
async def add_top_cmd(cmd_name):
    result = await topcmddb.find_one({"cmd_name": cmd_name})
    if result:
        await topcmddb.update_one({"cmd_name": cmd_name}, {"$inc": {"count": 1}})
    else:
        await topcmddb.insert_one({"cmd_name": cmd_name, "count": 1})


# Handler untuk mendapatkan total penggunaan command
async def get_total_commands_used():
    total_commands_used = await topcmddb.aggregate(
        [{"$group": {"_id": None, "total": {"$sum": "$count"}}}]
    ).to_list(1)
    return total_commands_used[0]["total"] if total_commands_used else 0


# Handler untuk mendapatkan top commands
async def get_top_cmd(limit=None):
    pipeline = [{"$sort": {"count": -1}}]
    if limit:
        pipeline.append({"$limit": limit})

    top_cmds = await topcmddb.aggregate(pipeline).to_list(None)
    total_commands_used = await get_total_commands_used()
    statistics = f"<b>Statistics:</b>\n🔨 Commands used: {total_commands_used}\n"

    top_cmds_text = "\n".join(
        "• 📊 <code>{}</code>: {}".format(cmd["cmd_name"], cmd["count"])
        for cmd in top_cmds
    )

    return statistics + top_cmds_text
