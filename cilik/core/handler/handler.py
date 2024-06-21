from pyrogram import filters
from pyrogram.types import Message

from cilik import *
from cilik.core.database import get_list_from_vars, get_plan
from config import OWNER_ID


class FILTERS:
    ME = filters.me
    GROUP = filters.group
    PRIVATE = filters.private
    OWNER = filters.user(OWNER_ID)
    ME_PRIVATE = filters.me & filters.private
    ME_GROUP = filters.me & filters.group
    ME_OWNER = filters.me & filters.user(OWNER_ID)


class CILIK:
    def UBOT(command, filter=FILTERS.ME, SUDO=False):
        def wrapper(func):
            memek = anjay(command)

            @ubot.on_message(memek & filter if not SUDO else memek)
            async def wrapped_func(client, message):
                user = message.from_user or message.sender_chat
                is_self = user.is_self if message.from_user else message.outgoing
                sudo_id = await get_list_from_vars(client.me.id, "SUDO_USERS")

                if SUDO and is_self or user.id in sudo_id:
                    return await func(client, message)

                elif not SUDO:
                    return await func(client, message)

            return wrapped_func

        return wrapper


def checkplan(func):
    async def wrapper(client, message: Message):
        user_id = client.me.id
        check = await get_plan(user_id)
        if check == "Riaa":
            return await message.reply(
                "Buka potensi penuh userbot Anda dengan **RiaaPro!**  Tingkatkan sekarang untuk mengakses fitur luar biasa ini.",
                quote=True,
            )
        return await func(client, message)

    return wrapper
