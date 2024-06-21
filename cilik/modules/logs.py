from asyncio import sleep

from pyrogram import filters
from pyrogram.enums import ParseMode

from cilik import ubot
from cilik.core.database import (
    add_chat_logs,
    add_top_cmd,
    add_user_logs,
    get_chat_logs,
    get_user_logs,
)
from cilik.core.handler import CILIK, checkplan
from cilik.utils.functions import get_arg

__MODULE__ = "Global"
__HELP__ = f"""
<b>Global Banned:</b>
<i>Fitur ini berfungsi untuk memblokir atau membanned user secara global atau diseluruh grup yang dimana kamu mendapat izin admin di setiap grupnya.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.gban</code> [user_id/username/reply to user]
└⋟ Untuk banned user dari semua group chats.

<b>ᴄᴍᴅ:</b>
├⋟<code>.ungban</code> [user_id/username/reply to user]
└⋟ Untuk unbanned user dari semua group chats.

<b>ᴄᴍᴅ:</b>
├⋟<code>.gbanlist</code>
└⋟ Untuk melihat list user yang Terbanned.
"""

# Caching variables
user_logs_cache = {}
chat_logs_cache = {}


async def get_user_logs_cache(user_id):
    if user_id in user_logs_cache:
        return user_logs_cache[user_id]
    else:
        logs_status = await get_user_logs(user_id)
        user_logs_cache[user_id] = logs_status
        return logs_status


async def get_chat_logs_cache(user_id):
    if user_id in chat_logs_cache:
        return chat_logs_cache[user_id]
    else:
        chat_logs = await get_chat_logs(user_id)
        chat_logs_cache[user_id] = chat_logs
        return chat_logs


@CILIK.UBOT("logs", SUDO=True)
@checkplan
async def logs_user(client, message):
    await add_top_cmd(message.command[0])
    arg = get_arg(message)
    user_id = client.me.id
    if not arg:
        await message.reply("Usage: `!logs` on/off")
        return
    await add_user_logs(user_id, arg)
    user_logs_cache[user_id] = arg  # Update the cache
    await message.reply(f"Sukses Logs mention <b>{arg.upper()}</b>")


@CILIK.UBOT("setlogs", SUDO=True)
@checkplan
async def add_logger(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        chat_id = message.chat.id
        await add_chat_logs(client.me.id, chat_id)
        chat_logs_cache[client.me.id] = chat_id  # Update the cache
        await message.reply(
            "✅ <i>Grup logs berhasil di set, semua mention akan masuk di Grup ini</i>"
        )
    else:
        chat_id = message.text.split()[1]
        await add_chat_logs(client.me.id, chat_id)
        chat_logs_cache[client.me.id] = chat_id  # Update the cache
        await message.reply(
            f"✅ <i> Grup logs berhasil di set, Chat Id</i> : {chat_id}"
        )


@ubot.on_message(filters.group & filters.mentioned & filters.incoming)
async def log_tagged_messages(client, message):
    user_id = client.me.id
    if await get_user_logs_cache(user_id) == "on":
        gruplogs = await get_chat_logs_cache(user_id)
        if gruplogs:
            grup = gruplogs
        else:
            grup = "me"
        result = (
            f"<b>📨 #TAGS #MESSAGE</b>\n<b> • Dari : </b>{message.from_user.mention}"
        )
        result += f"\n<b> • Grup : </b>{message.chat.title}"
        result += f"\n<b> • 👀 </b><a href = '{message.link}'>Lihat Pesan</a>"
        result += f"\n<b> • Message : </b><code>{message.text}</code>"
        await sleep(0.5)
        await client.send_message(
            grup,
            result,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
