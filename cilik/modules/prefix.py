from cilik.core.database import *
from cilik.core.handler import CILIK

__MODULE__ = "Settings"
__HELP__ = f"""
<b>Prefix:</b>
<i>Fitur ini berfungsi untuk mengatur awalan perintah userbot kamu.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.setprefix [prefix]
└⋟ Untuk mengubah prefix userbot.

Contoh: .setprefix ! (akan menjadi !ping , !help)
.setprefix none (maka tidak ada prefix)


<b>Set Emoji Ping:</b>
<i>Fitur ini berfungsi untuk mengatur tampilan ping.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.setemoji [query] [emoji_prem]
└⋟ Untuk merubah tampilan pong, uptime, mention pada ping.

query:
    •> PONG
    •> UPTIME
    •> MENTION
"""


@CILIK.UBOT("setprefix")
async def setprefix(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("Usage: `!setprefix` {prefix}")
    else:
        if message.command[1].lower() == "none":
            prefix = [""]
        else:
            prefix = message.command[1:]
        try:
            client.set_prefix(client.me.id, prefix)
            await set_pref(client.me.id, prefix)
            await set_prefix_bot(client.me.id, prefix)
            return await message.reply(
                f"✅ The prefix has been changed to : {' '.join(message.command[1:])}"
            )
        except Exception as error:
            await message.reply(error)
