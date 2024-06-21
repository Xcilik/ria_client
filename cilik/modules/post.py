from asyncio import sleep

from cilik.core.database import add_post, add_top_cmd, get_post, remove_post
from cilik.core.handler import CILIK, checkplan

__MODULE__ = "PostContent"
__HELP__ = f"""
<b>Post Content:</b>
<i>Fitur ini berfungsi untuk kamu yang punya banyak channel dan ingin mengirim / mengupload konten secara bersamaan.</i> 

<b>ᴄᴍᴅ:</b>
├⋟<code>.post</code> [text/reply to text/media]
└⋟ Mengirim konten kesemua Channel yang tersimpan di <b>Database</b>.

<b>ᴄᴍᴅ:</b>
├⋟<code>.addpost</code> [id / username channel]
└⋟ Untuk menambahkan Channel ke <b>LIST POST</b>.


<b>ᴄᴍᴅ:</b>
├⋟<code>.delpost</code> [id /username grup]
└⋟ Untuk menghapus Channel dari <b>LIST POST</b>.

<b>ᴄᴍᴅ:</b>
├⋟<code>.getpost</code> 
└⋟ Untuk melihat list Channel yang tersimpan di <b>Database.</b>
"""


@CILIK.UBOT("addpost", SUDO=True)
@checkplan
async def post(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        chat_id = message.chat.id
        user_id = int(client.me.id)
        chat_id = await client.get_chat(chat_id)
        schats = await get_post(user_id)
        if chat_id.id in schats:
            return await message.reply_text(
                "Channel/Grup ini sudah ada di <b>DATABASE</b>",
            )
        added = await add_post(user_id, chat_id.id)
        if added:
            await message.reply_text(
                f"Berhasil Channel/Grup {chat_id.title} telah ditambahkan di <b>DATABASE</b>"
            )
        else:
            await message.reply("Gagal menambahkan Channel")
    else:
        chat_id = message.text.split()[1]
        if "@" in chat_id:
            chat_id = chat_id.replace("@", "")
            chat_id = await client.get_chat(chat_id)
            schats = await get_post(int(client.me.id))
            if chat_id.id in schats:
                return await message.reply_text(
                    "Channel/Grup ini sudah ada di <b>DATABASE</b>",
                )
            added = await add_post(int(client.me.id), chat_id.id)
            if added:
                await message.reply_text(
                    f"Berhasil Channel/Grup {chat_id.title} ditambahkan di <b>DATABASE</b>"
                )
            else:
                await message.reply("Gagal menambahkan Channel")
        else:
            schats = await get_post(int(client.me.id))
            if int(chat_id) in schats:
                return await message.reply_text(
                    "Channel/Grup ini sudah ada di <b>DATABASE</b>",
                )
            added = await add_post(int(client.me.id), int(chat_id))
            if added:
                await message.reply_text(
                    f"Berhasil Channel/Grup <code>{int(chat_id)}</code> ditambahkan di <b>DATABASE</b>"
                )
            else:
                await message.reply("Gagal menambahkan Channel")


@CILIK.UBOT("listpost", SUDO=True)
@checkplan
async def _(client, message):
    await add_top_cmd(message.command[0])
    user_id = int(client.me.id)
    text = "<b>LIST GRUP/CHANNEL :</b>\n\n"
    j = 0
    for count, post in enumerate(await get_post(user_id), 1):
        try:
            title = (await client.get_chat(post)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"<b>{count}. {title}</b> | <code>{post}</code>\n"
    if j == 0:
        await message.reply_text("Tidak ada <b>LIST GRUP/CHANNEL</b> yang tersimpan!")
    else:
        await message.reply_text(text)


@CILIK.UBOT("delpost", SUDO=True)
@checkplan
async def del_post(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        chat_id = message.chat.id
        user_id = client.me.id
        chat_id = await client.get_chat(chat_id)
        schats = await get_post(user_id)
        if chat_id.id not in schats:
            return await message.reply_text(
                "Grup/Channel ini sudah di hapus dari <b>DATABASE</b>",
            )
        added = await remove_post(user_id, chat_id.id)
        if added:
            await message.reply_text(
                f"Berhasil Grup/Channel {chat_id.title} dihapus dari <b>DATABASE</b>"
            )
        else:
            await message.reply("Gagal menghapus Grup/Channel dari <b>DATABASE</b>")
    else:
        chat_id = message.text.split()[1]
        if "@" in chat_id:
            chat_id = chat_id.replace("@", "")
            user_id = client.me.id
            chat_id = await client.get_chat(chat_id)
            schats = await get_post(user_id)
            if chat_id.id not in schats:
                return await message.reply_text(
                    "Grup/Channel ini sudah di hapus dari <b>DATABASE</b>",
                )
            added = await remove_post(user_id, chat_id.id)
            if added:
                await message.reply_text(
                    f"Berhasil Grup/Channel {chat_id.title} dihapus dari <b>DATABASE</b>"
                )
            else:
                await message.reply("Gagal menghapus Grup/Channel dari <b>DATABASE</b>")
        else:
            schats = await get_post(int(client.me.id))
            if int(chat_id) not in schats:
                return await message.reply_text(
                    "Grup/Channel ini sudah di hapus dari <b>DATABASE</b>",
                )
            added = await remove_post(int(client.me.id), int(chat_id))
            if added:
                await message.reply_text(
                    f"Berhasil Grup/Channel  <code>{int(chat_id)}</code> dihapus dari <b>DATABASE</b>"
                )
            else:
                await message.reply("Gagal menghapus Grup/Channel dari <b>DATABASE</b>")


@CILIK.UBOT("post", SUDO=True)
@checkplan
async def _(client, message):
    await add_top_cmd(message.command[0])
    sent = 0
    failed = 0
    if message.reply_to_message:
        send = message.reply_to_message
    else:
        if len(message.command) < 2:
            return await message.reply("<b>Berikan text atau reply!</b>")
        else:
            send = message.text.split(None, 1)[1]
    post = await get_post(client.me.id)
    if not post:
        return await message.reply(
            "Tidak ada Grup/Channel yang tersimpan di <b>DATABASE</b>"
        )
    for chat_id in post:
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

    await message.reply(
        f"Berhasil mengirim pesan ke {sent} <b>Grup/Channel</b>, gagal terkirim di {failed} <b>Grup/Channel</b>"
    )
