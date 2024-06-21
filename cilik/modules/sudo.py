from cilik.core.database import *
from cilik.core.handler import CILIK, checkplan
from cilik.utils.functions import extract_user

__MODULE__ = "Sudo"
__HELP__ = f"""
<b>Sudo:</b>
<i>Fitur ini berfungsi untuk memberi akses bot kamu kepada orang lain / user lainnya.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.addsudo</code> [user_id/username] atau balas ke user
└⋟ Untuk menambahkan user ke sudo

<b>ᴄᴍᴅ:</b>
├⋟<code>.delsudo</code> [user_id/username] atau balas ke user
└⋟ Untuk menghapus user dari sudo

<b>ᴄᴍᴅ:</b>
├⋟<code>.getsudo</code> 
└⋟ Untuk melihat list sudo
"""


@CILIK.UBOT("addsudo")
@checkplan
async def _(client, message):
    await add_top_cmd(message.command[0])
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("**Berikan user_id/username/reply!**")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await message.reply(error)

    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USERS")

    if user.id in sudo_users:
        return await message.reply(
            f"<b><a href=tg://openmessage?user_id={user.id}>{user.first_name} {user.last_name or ''}</a></b> sudah ada dalam daftar sudo"
        )

    try:
        await add_to_vars(client.me.id, "SUDO_USERS", user.id)
        return await message.reply(
            f"✅ <b><a href=tg://openmessage?user_id={user.id}>{user.first_name} {user.last_name or ''}</a></b> berhasil di tambahkan ke daftar sudo"
        )
    except Exception as error:
        return await message.reply(error)


@CILIK.UBOT("delsudo")
@checkplan
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("**Berikan user_id/username/reply!**")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await message.reply(error)

    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USERS")

    if user.id not in sudo_users:
        return await message.reply(
            f"<b><a href=tg://openmessage?user_id={user.id}>{user.first_name} {user.last_name or ''}</a></b> tidak ada dalam daftar sudo"
        )

    try:
        await remove_from_vars(client.me.id, "SUDO_USERS", user.id)
        return await message.reply(
            f"❌ <b><a href=tg://openmessage?user_id={user.id}>{user.first_name} {user.last_name or ''}</a></b> berhasil di hapus dari daftar sudo"
        )
    except Exception as error:
        return await message.reply(error)


@CILIK.UBOT("listsudo")
@checkplan
async def _(client, message):
    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USERS")

    if not sudo_users:
        return await message.reply("Daftar sudo kosong!")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            sudo_list.append(
                f" ├ <b><a href=tg://openmessage?user_id={user.id}>{user.first_name} {user.last_name or ''}</a></b> | <code>{user.id}</code>"
            )
        except:
            continue

    if sudo_list:
        response = (
            "❏ <b>Daftar Sudo:</b>\n"
            + "\n".join(sudo_list)
            + f"\n ╰ Total: {len(sudo_list)}"
        )
        return await message.reply(response)
    else:
        return await message.reply("tidak dapat mengambil daftar sudo")
