import time
from datetime import datetime
from random import randint

from pyrogram.raw.functions import Ping

from cilik.core.database import add_saran, add_top_cmd, get_vars, set_vars
from cilik.core.handler import CILIK
from config import OWNER_ID

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("w", 60 * 60 * 24 * 7),
    ("d", 60 * 60 * 24),
    ("h", 60 * 60),
    ("m", 60),
    ("s", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount}{unit}{"" if amount == 1 else ""}')
    return ":".join(parts)


@CILIK.UBOT("dev", SUDO=False)
async def _(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("<b>Give suggestion!</b>", quote=True)
    anu = message.text.split(None, 1)[1]
    await add_saran(anu)
    await message.reply("✅ <i>Message sent!</i>", quote=True)


emojis = ["🏓", "♥️", "🔥", "💫", "💀", "⭐", "✨", "💥", "💤", "🎉", "❤️‍🔥", "🌛", "🗿"]


@CILIK.UBOT("ping", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    start = time.time()
    datetime.utcnow()
    await client.invoke(Ping(ping_id=randint(0, 2147483647)))
    delta_ping = round((time.time() - start) * 1000, 3)
    uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    emot_pong = (
        await get_vars(client.me.id, "EMOJI_PONG", "EMOTES")
        or "<emoji id=5269563867305879894>🏓</emoji>"
    )
    emot_uptime = (
        await get_vars(client.me.id, "EMOJI_UPTIME", "EMOTES")
        or "<emoji id=5316615057939897832>⏰</emoji>"
    )
    emot_mention = (
        await get_vars(client.me.id, "EMOJI_MENTION", "EMOTES")
        or "<emoji id=6226371543065167427>👑</emoji>"
    )

    if client.me.id == OWNER_ID:
        _ping = f"""
<b>🏓 Pong!</b>
<code>{delta_ping}ms</code>
"""
        return await message.reply(_ping, quote=True)

    elif client.me.is_premium:
        _ping = f"""
<b>{emot_pong} Pong:</b> <code>{delta_ping}ms</code>
<b>{emot_uptime} Uptime:</b> <code>{uptime}</code>
<b>{emot_mention} Owner:</b> <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a>
"""
    else:
        _ping = f"""
<b>🏓 Pong!</b>
<code>{delta_ping}ms</code>
"""
    await message.reply(_ping, quote=True)


@CILIK.UBOT("setemoji", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    try:
        msg = await message.reply("Set emojies...", quote=True)

        if len(message.command) < 3:
            return await msg.edit("Usage: `!setemoji` {query} {value}")

        query_mapping = {
            "pong": "EMOJI_PONG",
            "uptime": "EMOJI_UPTIME",
            "mention": "EMOJI_MENTION",
        }
        command, mapping, value = message.command[:3]

        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            emoji_id = value
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = f"<emoji id={entity.custom_emoji_id}>{value}</emoji>"
                        break

            await set_vars(client.me.id, query_var, emoji_id, "EMOTES")
            await msg.edit(
                f"<b>✅ <code>{query_var}</code> Berhasil di setting ke:</b> {emoji_id}"
            )
        else:
            await msg.edit("<b>Mapping tidak ditemukan</b>")

    except Exception as error:
        await msg.edit(str(error))
