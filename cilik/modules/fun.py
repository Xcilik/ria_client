import random
from asyncio import sleep

from pyrogram.enums import MessagesFilter

from cilik.core.database import (
    add_animation,
    add_top_cmd,
    delete_animation,
    get_all_animations,
    get_animation,
)
from cilik.core.handler import CILIK

__MODULE__ = "Fun"
__HELP__ = f"""
<b>Fun Fitur:</b>
<i>Fitur ini merupakan fitur fun atau untuk senang-senang.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.asupan</code>
└⋟ Untuk mengirim video asupan random

<b>ᴄᴍᴅ:</b>
├⋟<code>.ayang</code>
└⋟ Untuk mencari ayang (cewek)

<b>ᴄᴍᴅ:</b>
├⋟<code>.ayang2</code>
└⋟ Untuk mencari ayang (cowok)
"""


@CILIK.UBOT("asupan", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    y = await message.reply_text("<b>🔎 Mencari video asupan...</b>")
    try:
        asupannya = []
        async for asupan in client.search_messages(
            "@asupancilihehskbot", filter=MessagesFilter.VIDEO
        ):
            asupannya.append(asupan)
        video = random.choice(asupannya)
        await video.copy(
            message.chat.id,
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit(
            "<i>Asupan yang baik adalah makan 3x sehari dan minum air putih 8 gelas sehari...</i>"
        )


@CILIK.UBOT("ayang", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    y = await message.reply_text("<b>🔎 Mencari Ayang...</b>")
    try:
        ayangnya = []
        async for ayang in client.search_messages(
            "@CeweLogoPack", filter=MessagesFilter.PHOTO
        ):
            ayangnya.append(ayang)
        photo = random.choice(ayangnya)
        await photo.copy(
            message.chat.id,
            caption=f"<b>Ayang nya <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("Ayang tidak ditemukan, karena kamu jomblo!")


@CILIK.UBOT("ayang2", SUDO=True)
async def _(client, message):
    y = await message.reply_text("<b>🔎 Mencari Ayang...</b>")
    try:
        ayang2nya = []
        async for ayang2 in client.search_messages(
            "@fotocoworandom", filter=MessagesFilter.PHOTO
        ):
            ayang2nya.append(ayang2)
        photo = random.choice(ayang2nya)
        await photo.copy(
            message.chat.id,
            caption=f"<b>Ayang nya <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("<b>Ayang tidak ditemukan, karena kamu jomblo</b>")


async def play_animation(message, steps):
    for step in steps:
        if step.startswith("sleep("):
            delay = int(step[6:-1])
            await sleep(delay)
        else:
            await message.edit(step)


@CILIK.UBOT("addcmd")
async def handler_addcmd(client, message):
    if len(message.command) < 2:
        await message.reply(".addcmd {name_animation} {text/reply}")
        return

    animation_name = message.command[1]
    user_id = client.me.id

    if message.reply_to_message:
        # Jika user membalas pesan, gunakan isi pesan sebagai langkah-langkah animasi
        if message.reply_to_message.text:
            animation_steps = message.reply_to_message.text.strip().split("\n")
    else:
        # Jika user memberikan teks, gunakan teks tersebut sebagai langkah-langkah animasi
        parts = message.text.split("\n", 1)
        animation_steps = parts[1].strip().split("\n") if len(parts) > 1 else []

    await add_animation(user_id, animation_name, animation_steps)
    await message.reply(f"Saved animation '{animation_name}'.")


@CILIK.UBOT("delcmd")
async def handler_delcmd(client, message):
    if len(message.command) < 2:
        await message.reply(".delcmd {name_animation")
        return
    animation_name = message.command[1]
    message.from_user.id
    success = await delete_animation(client.me.id, animation_name)
    await message.reply(
        f"Animation for '{animation_name}' {'is deleted' if success else 'not found.'}"
    )


@CILIK.UBOT("cmd")
async def handler_cmd(client, message):
    if len(message.command) < 2:
        await message.reply(".cmd {name_animation")
        return
    animation_name = message.command[1]
    message.from_user.id
    steps = await get_animation(client.me.id, animation_name)
    if steps:
        await play_animation(message, steps)
    else:
        await message.reply(f"Animation '{animation_name}' not found.")


@CILIK.UBOT("listcmd")
async def handler_listcmd(client, message):
    message.from_user.id
    cmd_list = await get_all_animations(client.me.id)

    if cmd_list:
        cmd_list_text = "\n• ".join(cmd_list)
        await message.reply(f"List custom command animation:\n• {cmd_list_text}")
    else:
        await message.reply("乁⁠(⁠ ⁠•⁠_⁠•⁠ ⁠)⁠ㄏ")
