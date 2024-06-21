from pyrogram import filters

from cilik import ubot
from cilik.core.database import *
from cilik.core.handler import CILIK, checkplan
from cilik.utils.functions import get_arg

DEFAULT_TEXT = """
**Welcome {mention}**

How are you today?
"""

# Initialize cache
wlcm_cache = {}

@CILIK.UBOT("pmwlcm", SUDO=True)
@checkplan
async def pmguard(client, message):
    arg = get_arg(message)
    user_id = client.me.id
    if not arg:
        await message.reply("Usage: `!pmwlcm` on/off")
        return
    await set_wlcm(user_id, arg)
    wlcm_cache[user_id] = {"status": arg}
    await message.reply(f"Success! PM Welcome <b>{arg.upper()}</b>", quote=True)


@CILIK.UBOT("setpmwlcm", SUDO=True)
@checkplan
async def setpmwlcm(client, message):
    if len(message.command) < 1:
        return await message.reply("Usage: `!setpmwlcm` {text/reply}")
    text = message.text.markdown if message.text else message.caption.markdown
    if message.reply_to_message:
        if message.reply_to_message.text:
            await add_wlcm_text(client.me.id, message.reply_to_message.text.markdown)
            wlcm_cache[client.me.id]["text"] = message.reply_to_message.text.markdown
            await message.reply("WELCOME_MESSAGE has been successfully set!", quote=True)
        else:
            copy = await client.copy_message("me", message.chat.id, message.reply_to_message.id)
            await add_wlcm_text(client.me.id, copy.id)
            wlcm_cache[client.me.id]["text"] = copy.id
            await message.reply("WELCOME_MESSAGE has been successfully set!", quote=True)
    else:
        data = text.split(None, 1)[1].strip()
        await add_wlcm_text(client.me.id, data)
        wlcm_cache[client.me.id]["text"] = data
        await message.reply("WELCOME_MESSAGE has been successfully set!", quote=True)


@ubot.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=3
)
async def wlcm(client, message):
    user_id = client.me.id
    if user_id not in wlcm_cache:
        wlcm_cache[user_id] = {"status": await cek_wlcm(user_id)}
        if wlcm_cache[user_id]["status"] == "on":
            wlcm_cache[user_id]["chats"] = await get_wlcm(user_id)
            wlcm_cache[user_id]["text"] = await get_wlcm_text(user_id)
    
    if wlcm_cache[user_id]["status"] == "on":
        if not message.from_user:
            return
        if message.chat.id == 777000:
            return
        if message.chat.id in wlcm_cache[user_id]["chats"]:
            return
        
        text = wlcm_cache[user_id].get("text", DEFAULT_TEXT)
        await message.reply(
            text=text.format(
                name=message.from_user.first_name,
                username=f"@{message.from_user.username}" if message.from_user.username else None,
                mention=message.from_user.mention,
                id=message.from_user.id,
            )
        )
        await add_wlcm(user_id, int(message.chat.id))
        wlcm_cache[user_id]["chats"].append(message.chat.id)
