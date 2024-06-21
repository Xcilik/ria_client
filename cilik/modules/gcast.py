from asyncio import sleep

from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest

from cilik.core.database import add_gbl, add_top_cmd, get_gbl, remove_gbl
from cilik.core.handler import CILIK, checkplan
from config import BLACKLIST_CHAT

__MODULE__ = "Broadcast"
__HELP__ = f"""
<b>Global Broadcasting:</b>
<i>Fitur ini berfungsi untuk mengirim pesan text / media secara global atau keseluruh grup / user dengan satu perintah.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.gcast</code> [text/reply to text/media]
└⋟ Mengirim pesan kesemua grup.

<b>ᴄᴍᴅ:</b>
├⋟<code>.gucast</code> [text/reply to text/media]
└⋟ Mengirim pesan ke semua user.

<b>Blacklist</b>
<b>ᴄᴍᴅ:</b>
├⋟<code>.addbl</code> [id / username grup]
├⋟ Untuk menambahkan Gcast Blacklist.
└⋟ <b>Note:</b> Agar gcast tidak masuk ke grup tersebut.

<b>ᴄᴍᴅ:</b>
├⋟<code>.delbl</code> [id /username grup]
└⋟ Untuk menghapus Gcast Blacklist.

<b>ᴄᴍᴅ:</b>
├⋟<code>.getbl</code> 
└⋟ Untuk melihat Gcast Blacklist yang tersimpan di <b>Database.</b>

<b>Logger/ Tag mention</b>
<b>ᴄᴍᴅ:</b>
├⋟<code>.logs on/off</code> 
└⋟ Untuk mengaktifkan Tag mention, jika anda di tag/di reply di suatu grup maka akan muncul notif di Grup logs.

<b>ᴄᴍᴅ:</b>
├⋟<code>.setlogs</code> 
└⋟ Untuk set Grup Logs, buatlah sebuah grup dan ketik .setlogs di grup itu, maka Tag mention akan terkirim di grup tersebut, jika tidak maka akan terkirim di pesan Tersimpan.
"""


@CILIK.UBOT("addbl", SUDO=True)
async def add_gbla(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        chat_id = message.chat.id
        user_id = client.me.id
        chat_id = await client.get_chat(chat_id)
        schats = await get_gbl(user_id)
        if chat_id in schats:
            return await message.reply_text(
                "Grup ini sudah masuk di <b>Daftar Blacklist</b>",
            )
        await add_gbl(user_id, chat_id.id)
        await message.reply_text(
            f"Berhasil Grup {chat_id.title} telah ditambahkan di <b>Daftar Blacklist</b>"
        )
    else:
        chat_id = message.text.split()[1]
        if "@" in chat_id:
            chat_id = chat_id.replace("@", "")
            chat_id = await client.get_chat(chat_id)
            schats = await get_gbl(user_id)
            if chat_id.id in schats:
                return await message.reply_text(
                    "Grup ini sudah masuk di <b>Daftar Blacklist</b>",
                )
            await add_gbl(client.me.id, chat_id.id)
            await message.reply_text(
                f"Berhasil Grup {chat_id.title} telah ditambahkan di <b>Daftar Blacklist</b>"
            )

        else:
            schats = await get_gbl(client.me.id)
            if int(chat_id) in schats:
                return await message.reply_text(
                    "Grup ini sudah masuk di <b>Daftar Blacklist</b>",
                )
            await add_gbl(client.me.id, int(chat_id))
            await message.reply_text(
                f"Berhasil Grup <code>{int(chat_id)}</code> ditambahkan di <b>Daftar Blacklist</b>"
            )


@CILIK.UBOT("getbl|listbl", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    user_id = int(client.me.id)
    text = "<b>LIST CHAT BLACKLIST:</b>\n\n"
    j = 0
    for count, gbl in enumerate(await get_gbl(user_id), 1):
        try:
            title = (await client.get_chat(gbl)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"<b>{count}. {title}</b> | <code>{gbl}</code>\n"
    if j == 0:
        await message.reply_text("Tidak ada <b>Daftar Blacklist</b> yang tersimpan!")
    else:
        await message.reply_text(text)


@CILIK.UBOT("delbl", SUDO=True)
async def del_gbl(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        chat_id = await client.get_chat(message.chat.id)
        schats = await get_gbl(client.me.id)
        if chat_id.id not in schats:
            return await message.reply_text(
                "Grup ini sudah di hapus dari <b>Daftar Blacklist</b>",
            )
        await remove_gbl(client.me.id, chat_id.id)
        await message.reply_text(
            f"Berhasil Grup {chat_id.title} telah dihapus dari <b>Daftar Blacklist</b>"
        )

    else:
        chat_id = message.text.split()[1]
        if "@" in chat_id:
            chat = chat_id.replace("@", "")
            chats = await client.get_chat(chat)
            schats = await get_gbl(client.me.id)
            if chats.id not in schats:
                return await message.reply_text(
                    "Grup ini sudah di hapus dari <b>Daftar Blacklist</b>",
                )
            await remove_gbl(client.me.id, chats.id)
            await message.reply_text(
                f"Berhasil Grup {chats.title} telah dihapus dari <b>Daftar Blacklist</b>"
            )

        else:
            schats = await get_gbl(client.me.id)
            if int(chat_id) not in schats:
                return await message.reply_text(
                    "Grup ini sudah di hapus dari <b>Daftar Blacklist</b>",
                )
            await remove_gbl(client.me.id, int(chat_id))
            await message.reply_text(
                f"Berhasil Grup <code>{int(chat_id)}</code> telah di hapus dari <b>Daftar Blacklist</b>"
            )


@CILIK.UBOT("gcast", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    sent = 0
    failed = 0
    msg = await message.reply("<code>Globally Broadcasting Msg...</code>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit("<b>Berikan text/reply!</b>")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            user_id = int(client.me.id)
            BLGCAST = await get_gbl(user_id)
            if chat_id not in BLACKLIST_CHAT and chat_id not in BLGCAST:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await sleep(0.5)
                except Exception:
                    failed += 1
                    await sleep(0.5)

    await msg.edit(
        f"Berhasil mengirim pesan ke {sent} group(s), gagal terkirim di {failed} group(s)"
    )


@CILIK.UBOT("gucast", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    sent = 0
    failed = 0
    msg = await message.reply("<code>Globally UBroadcasting Msg...</code>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit("<b>Berikan text/reply!</b>")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in BLACKLIST_CHAT:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await sleep(0.5)
                except Exception:
                    failed += 1
                    await sleep(0.5)

    await msg.edit(
        f"Berhasil mengirim pesan ke {sent} user(s), gagal terkirim di {failed} user(s)"
    )


@CILIK.UBOT("gcastall", SUDO=True)
@checkplan
async def _(client, message):
    await add_top_cmd(message.command[0])
    sent = 0
    failed = 0
    msg = await message.reply("<code>Globally AllBroadcasting Msg...</code>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type == [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE]:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit("<b>Berikan text/reply!</b>")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in BLACKLIST_CHAT:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await sleep(0.5)
                except Exception:
                    failed += 1
                    await sleep(0.5)

    await msg.edit(
        f"Berhasil mengirim pesan ke semua grup dan user\n\nTotal pesan terikirim {sent}"
    )


@CILIK.UBOT("sended", SUDO=True)
async def _(client, message):
    if message.reply_to_message:
        if len(message.command) < 2:
            chat_id = message.chat.id
        else:
            chat_id = message.text.split()[1]
        try:
            await message.reply_to_message.copy(chat_id)
            tm = await message.reply(f"Berhasil Dikirim Ke {chat_id}")
            await sleep(2.5)
            await message.delete()
            await tm.delete()
        except BadRequest as t:
            await message.reply(f"{t}")
            return
    try:
        chat_id = message.text.split(None, 2)[1]
        chat_send = message.text.split(None, 2)[2]
    except TypeError as e:
        await message.reply(f"{e}")
    if len(chat_send) >= 2:
        try:
            await client.send_message(chat_id, chat_send)
            tm = await message.reply(f"Berhasil Dikirim Ke {chat_id}")
            await sleep(2.5)
            await message.delete()
            await tm.delete()
        except BadRequest as t:
            await message.reply(f"{t}")
