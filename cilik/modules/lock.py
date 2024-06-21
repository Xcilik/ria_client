from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import ChatNotModified
from pyrogram.types import ChatPermissions, Message

from cilik import ubot
from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, FILTERS
from config import OWNER_ID

__MODULE__ = "Lock"
__HELP__ = f"""
<b>Locked Groups:</b>
<i>Fitur ini berfungsi untuk mengatur izin grup, seperti mengunci media, sticker dan lainnya.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.lock</code> [parameter]
└⋟ Untuk mengunci izin grup.

<b>ᴄᴍᴅ:</b>
├⋟<code>.unlock</code> [parameter]
└⋟ Untuk membuka izin grup.

<b>ᴄᴍᴅ:</b>
├⋟<code>.locks</code> 
└⋟ Untuk melihat izin grup.

<b>example:</b> <code>.lock all</code> 
<b>parameter:</b> [ <code>msg</code> - <code>media</code> - <code>stickers</code> - <code>polls</code> - <code>info</code>  - <code>invite</code> - <code>webprev</code> - <code>pin</code> - <code>all</code> ]
"""

incorrect_parameters = "Incorrect Parameters, Ketik .help."

data = {
    "msg": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(client: Client, chat_id):
    perms = []
    perm = (await client.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms


async def tg_lock(
    client: Client, message: Message, permissions: list, perm: str, lock: bool
):
    if lock:
        if perm not in permissions:
            return await message.reply("Already locked.")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.reply("Already Unlocked.")
        permissions.append(perm)

    permissions = {perm: True for perm in list(set(permissions))}

    try:
        await client.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.reply(
            "To unlock this, you have to unlock 'messages' first."
        )

    await message.reply(("Locked." if lock else "Unlocked."))


@ubot.on_message(
    filters.command(["lock", "unlock"], ",") & filters.group & filters.user(OWNER_ID)
)
@CILIK.UBOT("lock|unlock", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message: Message):
    await add_top_cmd(message.command[0])
    if len(message.command) != 2:
        return await message.reply(incorrect_parameters)

    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()

    if parameter not in data and parameter != "all":
        return await message.reply(incorrect_parameters)

    permissions = await current_chat_permissions(client, chat_id)

    if parameter in data:
        await tg_lock(
            client,
            message,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        await client.set_chat_permissions(chat_id, ChatPermissions())
        await message.reply(f"<b>🔐 Locked Everything in {message.chat.title}</b>")

    elif parameter == "all" and state == "unlock":
        await client.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False,
            ),
        )
        await message.reply(f"<b>🔓 Unlocked Everything in {message.chat.title}</b>")


@ubot.on_message(
    filters.command(["locks"], ",") & filters.group & filters.user(OWNER_ID)
)
@CILIK.UBOT("locks", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message: Message):
    await add_top_cmd(message.command[0])
    permissions = await current_chat_permissions(client, message.chat.id)

    if not permissions:
        return await message.reply("No Permissions.")

    perms = ""
    for i in permissions:
        perms += f"  ► <code>{i}</code>\n"

    await message.reply(perms)
