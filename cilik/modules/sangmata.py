from asyncio import sleep

from pyrogram.errors import YouBlockedUser
from pyrogram.raw.functions.messages import DeleteHistory

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK
from cilik.utils.functions import extract_user

__MODULE__ = "SangMata"
__HELP__ = f"""
<b>SangMata:</b>
<i>Fitur ini berfungsi untuk melihat history name dan username akun <b>Telegram.</b></i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.sg</code> [id/username] or [reply to user]
└⋟ Untuk mengetahui History name dan History username seseorang .
"""


@CILIK.UBOT("sg", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    args = await extract_user(message)
    lol = await message.reply("<code>Searching...</code>")
    if args:
        try:
            user = (await client.get_users(args)).id
        except:
            user = message.text.split()[1]
    bot = "@SangMata_beta_bot"
    try:
        txt = await client.send_message(bot, f"{user}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        txt = await client.send_message(bot, f"{user}")
    await txt.delete()
    await sleep(2)
    await lol.delete()
    async for stalk in client.search_messages(bot, query="Names"):
        if not stalk:
            await message.reply("Tidak ada catatan tentang user ini")
            user_info = await client.resolve_peer(bot)
            return await client.send(
                DeleteHistory(peer=user_info, max_id=0, revoke=True)
            )
        elif stalk:
            await stalk.copy(message.chat.id, reply_to_message_id=message.id)
    user_info = await client.resolve_peer(bot)
    return await client.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
