from pyrogram.enums import ChatType

from cilik.core.database import add_top_cmd, set_font
from cilik.core.handler import CILIK
from cilik.utils.functions import extract_user

__MODULE__ = "Info"
__HELP__ = f"""
<b>Information:</b>
<i>Fitur ini berfungsi untuk mencari info tentang User / Grup / Channel <b>Telegram.</b></i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.cek</code> [user_id]
└⋟ Untuk mendapatkan informasi user di <b>FBI DATABASE.</b>

<b>ᴄᴍᴅ:</b>
├⋟<code>.info</code> [user_id / username / reply to users]
└⋟ Untuk mendapatkan info pengguna / user telegram.
         
<b>ᴄᴍᴅ:</b>
├⋟<code>.cinfo</code> [chat_id / username / reply to chat]
└⋟ Untuk mendapatkan info group / channel.
 
"""


@CILIK.UBOT("whois|info", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    user_id = await extract_user(message)
    Tm = await message.reply("<code>Search for <b>user</b> information...</code>")
    if not user_id:
        return await Tm.edit("<b>Berikan userid/username/reply!</b>")
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bioh = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b>User Information:</b>

<b>user_id:</b> <code>{user.id}</code>
<b>first_name:</b> {first_name}
<b>last_name:</b> {last_name}
<b>username:</b> {username}
<b>dc_id:</b> <code>{dc_id}</code>
<b>is_bot:</b> <code>{user.is_bot}</code>
<b>is_premium:</b> <code>{user.is_premium}</code>
<b>user_bio:</b> {bioh}

<b>same_groups_seen:</b> {len(common)}
<b>last_seen:</b> <code>{status}</code>
"""

        await set_font(client.me.id, out_str)
        x = await client.get_inline_bot_results("smallubot", f"info_user {user.id}")
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
            )
        await Tm.delete()
    except Exception as e:
        return await Tm.edit(f"INFO: {e}")


@CILIK.UBOT("cwhois|cinfo", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    Tm = await message.reply("<code>Search for <b>chat</b> information...</code>")
    try:
        if len(message.text.split()) > 1:
            chat_u = message.text.split()[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await Tm.edit(
                    "Gunakan perintah ini di dalam grup atau ketik `!cinfo {group username atau id}`"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b>Chat Information:</b>

<b>chat_id:</b> <code>{chat.id}</code>
<b>title:</b> {chat.title}
<b>username:</b> {username}
<b>type:</b> <code>{type}</code>
<b>dc_id:</b> <code>{dc_id}</code>
<b>is_scam:</b> <code>{chat.is_scam}</code>
<b>is_fake:</b> <code>{chat.is_fake}</code>
<b>verified:</b> <code>{chat.is_verified}</code>
<b>restricted:</b> <code>{chat.is_restricted}</code>
<b>protected:</b> <code>{chat.has_protected_content}</code>

<b>total_members:</b> <code>{chat.members_count}</code>
<b>description:</b>
<code>{description}</code>
"""
        await set_font(client.me.id, out_str)
        x = await client.get_inline_bot_results(
            "smallubot", f"info_user {chat.username}"
        )
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
            )
        await Tm.delete()
    except Exception as e:
        return await Tm.edit(f"INFO: `{e}`")
