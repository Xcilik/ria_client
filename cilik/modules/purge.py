from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

__MODULE__ = "Purge"
__HELP__ = f"""
<b>Purge:</b>
<i>Fitur  ini berfungsi untuk menghapus pesan / menghapus semua pesan</i>.

<b>ᴄᴍᴅ:</b>
├⋟<code>.purge</code> [reply to message]
└⋟ Bersihkan (hapus semua pesan) obrolan dari pesan yang dibalas hingga yang terakhir.

<b>ᴄᴍᴅ:</b>
├⋟<code>.del</code> [reply to message]
└⋟ Hapus pesan yang dibalas.

<b>ᴄᴍᴅ:</b>
├⋟<code>.purgeme</code> [number of messages]
├⋟ Hapus pesan anda sendiri dengan menentukan total pesan.
└⋟ <b>Example:</b> <code>.purgeme 100</code> 

"""


@CILIK.UBOT("del", SUDO=True)
async def del_user(_, message):
    await add_top_cmd(message.command[0])
    rep = message.reply_to_message
    await message.delete()
    await rep.delete()


@CILIK.UBOT("purgeme", SUDO=True)
async def purge_me_func(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) != 2:
        return await message.delete()
    n = (
        message.reply_to_message
        if message.reply_to_message
        else message.text.split(None, 1)[1].strip()
    )
    if not n.isnumeric():
        return await message.reply("<b>Argumen Tidak Valid!</b>")
    n = int(n)
    if n < 1:
        return await message.reply("Usage: `!purgeme` {number}")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(message.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return await eor(message, text="Tidak ada pesan yang ditemukan.")
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )


@CILIK.UBOT("purge", SUDO=True)
async def purgefunc(client, message):
    await add_top_cmd(message.command[0])
    await message.delete()
    if not message.reply_to_message:
        return await message.reply_text("<b>Reply to message!</b>")
    chat_id = message.chat.id
    message_ids = []
    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )
