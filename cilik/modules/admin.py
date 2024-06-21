from asyncio import sleep

from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges

from cilik.core.database import (
    add_gban_user,
    get_gban_user,
    get_seles,
    remove_gban_user,
)
from cilik.core.handler import CILIK, FILTERS
from cilik.utils.functions import extract_user
from config import OWNER_ID

__MODULE__ = "Admin"
__HELP__ = """
<b>Administrator:</b>
<i>Fitur ini akan berfungsi jika kamu menjadi admin di sebuah grup, dengan fitur ini kamu bisa mute, ban, kick user dan fungsi admin lainnya.</i>
"""


@CILIK.UBOT("kick|ban|mute|unmute|unban", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message):
    if message.command[0] == "kick":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "**Berikan userid/username atau reply!**"
                )
            else:
                _id = message.text.split()[1]
        try:
            user_id = (await client.get_users(_id)).id
        except Exception as error:
            return await message.reply(error)
        if user_id == client.me.id:
            return await message.reply_text("Idiot Master _-.")
        if user_id in [OWNER_ID]:
            return await message.reply_text("Tidak bisa mengeluarkan pengguna ini")
        user = await message.chat.get_member(user_id)
        if user.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(
                "Tidak bisa mengeluarkan Pengguna ini, karena dia admin"
            )
        mention = (await client.get_users(user_id)).mention
        msg = f"<b>Kicked:</b> {mention}\n<b>Admin:</b> {message.from_user.mention}"
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg)
            await sleep(1)
            await message.chat.unban_member(user_id)
        except ChatAdminRequired:
            return await message.reply("Anda bukan admin di group ini!")

    elif message.command[0] == "ban":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "**Berikan userid/username atau reply!**"
                )
            else:
                _id = message.text.split()[1]
        try:
            user_id = (await client.get_users(_id)).id
        except Exception as error:
            return await message.reply(error)
        if user_id == client.me.id:
            return await message.reply_text("Tidak bisa Ban diri sendiri.")
        if user_id in [OWNER_ID]:
            return await message.reply_text(
                "Tidak bisa di ban, dia adalah pembuat saya"
            )
        user = await message.chat.get_member(user_id)
        if user.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(
                "Tidak bisa ban pengguna tersebut, karena dia admin."
            )
        mention = (await client.get_users(user_id)).mention
        msg = f"<b>Banned:</b> {mention}\n<b>Admin:</b> {message.from_user.mention}"
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg)
        except ChatAdminRequired:
            return await message.reply("Anda bukan admin di group ini!")
    elif message.command[0] == "mute":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "**Berikan userid/username atau reply!**"
                )
            else:
                _id = message.text.split()[1]
        try:
            user_id = (await client.get_users(_id)).id
        except Exception as error:
            return await message.reply(error)
        if user_id == client.me.id:
            return await message.reply_text("LoL.")
        if user_id in [OWNER_ID]:
            return await message.reply_text(
                "Tidak bisa di bisuin, karena dia pembuat saya"
            )
        user = await message.chat.get_member(user_id)
        if user.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(
                "Tidak bisa membisukan pengguna tersebut, karena dia admin."
            )
        mention = (await client.get_users(user_id)).mention
        msg = f"<b>Muted:</b> {mention}\n<b>Admin:</b> {message.from_user.mention}"
        try:
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply(msg)
        except ChatAdminRequired:
            return await message.reply("Anda bukan admin di group ini!")

    elif message.command[0] == "unmute":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "**Berikan userid/username atau reply!**"
                )
            else:
                _id = message.text.split()[1]
        try:
            user = await client.get_users(_id)
        except Exception as error:
            return await message.reply(error)
        try:
            await message.chat.unban_member(user.id)
            await message.reply(f"**Unmuted {user.mention} Succesfully!**")
        except ChatAdminRequired:
            return await message.reply("Anda bukan admin di group ini!")

    elif message.command[0] == "unban":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "**Berikan userid/username atau reply!**"
                )
            else:
                _id = message.text.split()[1]
        try:
            user = await client.get_users(_id)
        except Exception as error:
            return await message.reply(error)
        try:
            await message.chat.unban_member(user.id)
            await message.reply(f"**Unbanned {user.mention} Succesfully!**")
        except ChatAdminRequired:
            return await message.reply("Anda bukan admin di group ini !")


# Admin Groups variable


@CILIK.UBOT("setgpic|setgtitle", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message):
    if message.command[0] == "setgpic":
        zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
        can_change_admin = zuzu.can_change_info
        can_change_member = message.chat.permissions.can_change_info
        if not (can_change_admin or can_change_member):
            await message.reply_text("Tidak ada izin untuk mengganti foto grup")
        if message.reply_to_message:
            if message.reply_to_message.photo:
                await client.set_chat_photo(
                    message.chat.id, photo=message.reply_to_message.photo.file_id
                )
                await message.reply("<b>Setgroup picture success!</b>")
                return
        else:
            await message.reply_text("<b>Reply to photo!</b>")

    elif message.command[0] == "setgtitle":
        text = (
            message.text.split(None, 1)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
        can_change_admin = zuzu.can_change_info
        can_change_member = message.chat.permissions.can_change_info

        if not text:
            await message.reply("<b>Berikan judul Grup!</b>")

        if not (can_change_admin or can_change_member):
            await message.reply_text("Tidak ada izin untuk mengganti title/nama grup")
        else:
            await client.set_chat_title(message.chat.id, title=text)
            await message.reply(
                f"<b>Setchat title success\ntitle:</b> <code>{text}</code>"
            )


@CILIK.UBOT("pin|unpin", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message):
    if not message.reply_to_message:
        return await message.reply("<b>Reply to message!</b>")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await message.reply("Anda tidak ada izin untuk pin pesan")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.reply(
            f"<b>Unpinned <a href='{r.link}'>this</a> message.</b>",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await message.reply(
        f"<b>📌 Pinned <a href='{r.link}'>this</a> message.</b>",
        disable_web_page_preview=True,
    )


# Users Variable


@CILIK.UBOT("promote|fullpromote", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("**Berikan userid/username atau reply!**")
    (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    umention = (await client.get_users(user_id)).mention
    if message.command[0][0] == "f":
        try:
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            return await message.reply(f"<b>🎖 Fully Promoted! {umention}</b>")
        except ChatAdminRequired:
            return await message.reply("Anda bukan admin di group ini!")
    try:
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await message.reply(f"<b>🏅 Promoted! {umention}</b>")
    except ChatAdminRequired:
        return await message.reply("Anda bukan admin di grup ini!")


@CILIK.UBOT("demote|unadmin", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("**Berikan userid/username atau reply!**")
    if user_id == client.me.id:
        return await message.reply("Tidak bisa menurunkan hak admin diri sendiri.")
    try:
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
            ),
        )
        umention = (await client.get_users(user_id)).mention
        await message.reply(f"<b>✅ Demoted! {umention}</b>")
    except ChatAdminRequired:
        return await message.reply("Anda bukan admin di group ini!")


@CILIK.UBOT("gban", SUDO=True)
async def ban_globally(client, message):
    if message.reply_to_message:
        _id = message.reply_to_message.from_user.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("**Berikan userid/username atau reply!**")
        else:
            _id = message.text.split()[1]
    try:
        user_id = (await client.get_users(_id)).id
    except Exception as error:
        return await message.reply(error)
    from_user = message.from_user
    seler = await get_seles()

    if user_id == client.me.id:
        return await message.reply_text("Idiot Master _-.")
    if user_id in seler:
        return await message.reply_text("Tidak bisa gban pengguna ini")

    user = await client.get_users(_id)
    m = await message.reply_text(f"<b>Banning {user.mention} Globally!</b>")
    await add_gban_user(from_user.id, user_id)
    prik = user_id
    iso = 0
    gagal = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            try:
                await client.ban_chat_member(chat, prik)
                iso = iso + 1
                await sleep(0.1)
            except:
                gagal = gagal + 1
                await sleep(0.1)
    ban_text = f"""
<i><b>New Global Ban</b></i>
<b>Origin:</b> {message.chat.title} [<code>{message.chat.id}</code>]
<b>Admin:</b> {from_user.mention}
<b>Banned User:</b> {user.mention}
<b>Banned User ID:</b> <code>{user_id}</code>
<b>Chats:</b> <code>{iso}</code>"""
    await m.edit(ban_text)


@CILIK.UBOT("ungban", SUDO=True)
async def unban_globally(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("**Berikan userid/username atau reply!**")
    user = await client.get_users(user_id)

    is_gbanned = await get_gban_user(client.me.id)
    if user.id not in is_gbanned:
        return await message.reply_text("Pengguna ini tidak ada di list gban!")
    mhuy = await message.reply_text(f"<b>UnBanning {user.mention} Globally!</b>")
    await remove_gban_user(client.me.id, user.id)
    prik = user.id
    iso = 0
    gagal = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            try:
                await client.unban_chat_member(chat, prik)
                iso = iso + 1
                await sleep(0.1)
            except:
                gagal = gagal + 1
                await sleep(0.1)
        return await mhuy.edit(f"Lifted {user.mention} Global Ban.")


@CILIK.UBOT("listgban", SUDO=True)
async def get_gban_userly(client, message):
    user_id = int(client.me.id)
    text = "<b>Gbanned List :</b>\n\n"
    j = 0
    for count, gbl in enumerate(await get_gban_user(user_id), 1):
        try:
            title = (await client.get_users(gbl)).first_name
        except Exception:
            title = "uknown"
        j = 1
        text += f"<b>{count}. Name:</b> {title}\n<b>Id:</b> <code>{gbl}</code>\n\n"
    if j == 0:
        await message.reply_text("Tidak ada <b>List Gban</b> yang tersimpan!")
    else:
        await message.reply_text(text)


@CILIK.UBOT("invitelink", SUDO=True)
async def invitelink(client, message):
    try:
        ya = await client.export_chat_invite_link(message.chat.id)
        await message.reply(f"**Chat name:** {message.chat.title}\n**Link:** `{ya}`")
    except Exception:
        await message.reply("Maaf anda bukan admin di grup/channel ini")
