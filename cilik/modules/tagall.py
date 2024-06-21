import asyncio
import random
from random import shuffle

from pyrogram.types import Message

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, FILTERS, checkplan

__MODULE__ = "Mentions"
__HELP__ = f"""
<b>Mentions / Tag:</b>
<i>Fitur ini berfungsi untuk men TAG semua anggota grup, bisa dilengkapi dengan text informasi.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.tagall</code> [type message/reply message]
└⋟ Untuk men TAG semua anggota grup.

<b>ᴄᴍᴅ:</b>
├⋟<code>.emojitag [text]</code>
└⋟ Untuk men TAG semua anggota grup dengan Emoji.

<b>ᴄᴍᴅ:</b>
├⋟<code>.stop</code>
└⋟ Untuk membatalkan mentions / tagall.

"""

tagallgcid = []

emoji = "😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 ☺️ 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🎲 🧩 ♟ 🎯 🎳 🎭💕 💞 💓 💗 💖 ❤️‍🔥 💔 🤎 🤍 🖤 ❤️ 🧡 💛 💚 💙 💜 💘 💝 🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧 🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍨".split(
    " "
)


@CILIK.UBOT("tagall|stop", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message: Message):
    await add_top_cmd(message.command[0])
    if message.command[0] == "tagall":
        if message.chat.id in tagallgcid:
            return
        tagallgcid.append(message.chat.id)
        text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else ""
        users = [
            member.user.mention
            async for member in message.chat.get_members()
            if not (member.user.is_bot or member.user.is_deleted)
        ]
        shuffle(users)
        m = message.reply_to_message or message
        for output in [users[i : i + 5] for i in range(0, len(users), 5)]:
            if message.chat.id not in tagallgcid:
                break
            await asyncio.sleep(1.5)
            await m.reply_text(
                ", ".join(output) + "\n\n" + text, quote=bool(message.reply_to_message)
            )
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
    elif message.command[0] == "stop":
        if message.chat.id not in tagallgcid:
            return await message.reply_text("Tidak ada mentions")
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
        await message.reply_text("<b>Stoped.</b>")


@CILIK.UBOT("emojitag", FILTERS.ME_GROUP, SUDO=True)
@checkplan
async def tagmentions(client, message: Message):
    await add_top_cmd(message.command[0])
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not text:
        await message.reply("<b>Berikan Text!</b>")
    else:
        tagallgcid.append(message.chat.id)
        usrnum = 0
        usrtxt = ""
        async for usr in client.get_chat_members(message.chat.id):
            if not message.chat.id in tagallgcid:
                break
            usrnum += 1
            usrtxt += f"<a href=tg://user?id={usr.user.id}>{random.choice(emoji)}</a>"
            if usrnum == 5:
                if text:
                    txt = f"{usrtxt}\n\n{text}"
                    await client.send_message(message.chat.id, txt)
                await asyncio.sleep(1.5)
                usrnum = 0
                usrtxt = ""
        try:
            tagallgcid.remove(message.chat.id)
        except:
            pass
