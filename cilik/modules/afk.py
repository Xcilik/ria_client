from asyncio import sleep
from datetime import datetime

from pyrogram import filters

from cilik import ubot
from cilik.core.database import add_top_cmd, check_afk, go_afk, no_afk
from cilik.core.handler import CILIK, checkplan
from cilik.utils.functions import get_text

afk_sanity_check: dict = {}
afk_cache: dict = {}  # Cache for AFK status

afkstr = """
• AFK Aktif\n\n• Alasan {}
"""
onlinestr = """
• AFK Tidak Aktif\n\n• Alasan {}
"""


async def is_afk_(f, client, message):
    user_id = client.me.id
    if user_id in afk_cache:
        return afk_cache[user_id]["is_afk"]
    else:
        af_k_c = await check_afk(user_id)
        afk_cache[user_id] = {
            "is_afk": bool(af_k_c),
            "time": af_k_c["time"] if af_k_c else None,
            "reason": af_k_c["reason"] if af_k_c else None,
        }
        return afk_cache[user_id]["is_afk"]


is_afk = filters.create(func=is_afk_, name="is_afk_")


@CILIK.UBOT("afk")
@checkplan
async def set_afk(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) == 1:
        return await message.reply(
            f"<b>Berikan alasan!</b>",
            quote=True,
        )
    user_id = client.me.id
    msge = get_text(message)
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if msge:
        msg = f"<b>• Sedang AFK</b>.\n<b>• Alasan</b> : <code>{msge}</code>"
        await go_afk(user_id, afk_start, msge)
    else:
        msg = "<b>• Sedang AFK</b>."
        await go_afk(user_id, afk_start)

    afk_cache[user_id] = {"is_afk": True, "time": afk_start, "reason": msge}
    await message.reply(msg)


@ubot.on_message(
    is_afk
    & (filters.mentioned | filters.private)
    & ~filters.me
    & ~filters.bot
    & filters.incoming
)
async def afk_er(client, message):
    user_id = client.me.id
    if not message.from_user:
        return
    if message.from_user.id == user_id:
        return
    if user_id not in afk_cache:
        return  # Safety check, should not happen

    use_r = int(user_id)
    if use_r not in afk_sanity_check.keys():
        afk_sanity_check[use_r] = 1
    else:
        afk_sanity_check[use_r] += 1
    if afk_sanity_check[use_r] == 5:
        await message.reply_text("<b>• Sedang AFK</b>.")
        afk_sanity_check[use_r] += 1
        return
    if afk_sanity_check[use_r] > 5:
        return

    lol = afk_cache[user_id]
    reason = lol["reason"]
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    message_to_reply = (
        f"<b>• Sedang AFK</b>\n<b>• Waktu</b> : <code>{total_afk_time}</code>\n<b>• Alasan</b> : <code>{reason}</code>"
        if reason
        else f"<b>• Sedang AFK</b>\n<b>• Waktu</b> : <code>{total_afk_time}</code>"
    )
    await message.reply(message_to_reply)


@CILIK.UBOT("unafk")
@checkplan
async def no_afke(client, message):
    user_id = client.me.id
    if user_id not in afk_cache:
        return  # Safety check, should not happen

    lol = afk_cache[user_id]
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    kk = await message.reply(
        f"<b>• Saya Kembali.</b>\n<b>• AFK Selama</b> : <code>{total_afk_time}</code>"
    )
    await sleep(3)
    await kk.delete()
    await no_afk(user_id)
    afk_cache[user_id] = {"is_afk": False, "time": None, "reason": None}
