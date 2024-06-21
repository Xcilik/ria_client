from asyncio import sleep

from pyrogram.enums import UserStatus

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, FILTERS, checkplan

__MODULE__ = "Invite"
__HELP__ = f"""
<b>Invite Members:</b>
<i>Fitur ini berfungsi untuk mengundang member ke grup, untuk cmd .inviteall tidak diperbolehkan untuk akun <b>Telegram</b> dengan id baru atau berawalan 5/6 karena dapat mengakibatkan akun terhapus karena terkena spam dari <b>Telegram.</b></i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.invite</code> [username]
└⋟ Untuk Mengundang Anggota ke grup Anda

<b>ᴄᴍᴅ:</b>
├⋟<code>.inviteall</code> [username_group - number of members]
├⋟ Untuk Mengundang Anggota dari obrolan grup lain ke obrolan grup Anda
└⋟ <b>Notes:</b> <i>Jangan gunakan fitur ini jika akun kamu merupakan akun ID baru yang ber awalan ID 5 / 6.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.cancel</code>
└⋟ Untuk membatalkan perintah inviteall
"""


invte_id = []


@CILIK.UBOT("invite", SUDO=True)
async def inviteee(client, message):
    await add_top_cmd(message.command[0])
    mg = await message.reply("<b>Menambahkan Pengguna!</b>")
    if len(message.command) < 2:
        return await mg.delete()
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit("<b>Berikan user_id/username!</b>")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"Tidak Dapat Menambahkan Pengguna!\nTraceBack: {e}")
        return
    await mg.edit(f"<b>Berhasil ditambahkan {len(user_list)} Ke Grup Ini</b>")


@CILIK.UBOT("inviteall", FILTERS.ME_GROUP, SUDO=True)
@checkplan
async def inv(client, message):
    await add_top_cmd(message.command[0])
    Tm = await message.reply("<b>Inviting members...</b>")
    if len(message.command) < 3:
        await message.delete()
        return await Tm.delete()
    queryy = message.text.split()[1]
    limit_ = message.text.split()[2]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    if tgchat.id in invte_id:
        return await Tm.edit_text(
            "sedang menginvite member silahkan coba lagi nanti atau gunakan perintah: <code>!cancel</code>"
        )
    else:
        invte_id.append(tgchat.id)
        await Tm.edit_text(f"Mengundang anggota dari {chat.title}")
        done = 0
        async for member in client.get_chat_members(chat.id, limit=int(limit_)):
            user = member.user
            zxb = [
                UserStatus.ONLINE,
                UserStatus.OFFLINE,
                UserStatus.RECENTLY,
                UserStatus.LAST_WEEK,
            ]
            if user.status in zxb:
                try:
                    await client.add_chat_members(tgchat.id, user.id)
                    await sleep(0.5)
                    done += 1
                except:
                    pass
        invte_id.remove(tgchat.id)
        await Tm.delete()
        return await message.reply(
            f"<b>✅ <code>{done}</code> Anggota Telah Berhasil Diundang</b>"
        )


@CILIK.UBOT("cancel", FILTERS.ME_GROUP, SUDO=True)
@checkplan
async def cancel(client, message):
    await add_top_cmd(message.command[0])
    if message.chat.id not in invte_id:
        return await message.reply_text(
            "sedang tidak ada perintah: <code>!inviteall</code> yang digunakan"
        )
    try:
        invte_id.remove(message.chat.id)
        await message.reply_text("ok inviteall berhasil dibatalkan")
    except Exception as e:
        await message.reply_text(e)


@CILIK.UBOT("culik", FILTERS.ME_GROUP, SUDO=True)
async def culik(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not text:
        return await message.reply("<b>Usage:</b> <code>.culik @usernamegrup</code>")
    Cilik = await message.reply("Processing . . .")
    chat = await client.get_chat(text)
    tgchat = message.chat
    await Cilik.edit_text(f"inviting users from {chat.username}")
    async for member in client.get_chat_members(chat.id, limit=100):
        user = member.user
        zxb = [
            UserStatus.ONLINE,
            UserStatus.OFFLINE,
            UserStatus.RECENTLY,
            UserStatus.LAST_WEEK,
        ]
        if user.status in zxb:
            try:
                await client.add_chat_members(tgchat.id, user.id)
            except Exception as e:
                mg = await message.reply(f"<b>Error</b> <code>{e}</code>")
                await sleep(5)
                await mg.delete()
