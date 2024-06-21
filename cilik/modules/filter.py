import re
from datetime import datetime

from pyrogram import filters
from pytz import timezone

from cilik import ubot, username_bot
from cilik.core.database import *
from cilik.core.handler import CILIK, checkplan
from cilik.utils.functions import get_arg

filter_status_cache = {}


async def get_filter_status_cache(user_id):
    if user_id in filter_status_cache:
        return filter_status_cache[user_id]
    else:
        filter_status = await cek_filter(user_id)
        filter_status_cache[user_id] = filter_status
        return filter_status


@ubot.on_message(
    filters.text
    & filters.private
    & ~filters.me
    & ~filters.via_bot
    & ~filters.forwarded,
    group=1,
)
async def filters_re(client, message):
    filter_status = await get_filter_status_cache(client.me.id)
    if filter_status == "on":
        text = message.text.lower().strip()
        if not text:
            return
        list_of_filters = await all_filter(client.me.id)
        if list_of_filters:
            for word in list_of_filters:
                pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
                if re.search(pattern, text, flags=re.IGNORECASE):
                    _filter = await get_filter(client.me.id, word)
                    _filterbutton = await get_filter_button(client.me.id, word)
                    if _filterbutton:
                        try:
                            x = await client.get_inline_bot_results(
                                username_bot,
                                f"filter_button {word} {message.from_user.first_name} {message.from_user.username} {message.from_user.id} {message.from_user.mention}",
                            )
                            for m in x.results:
                                await client.send_inline_bot_result(
                                    message.chat.id,
                                    x.query_id,
                                    m.id,
                                )
                        except Exception as error:
                            return await client.send_message(
                                message.chat.id, str(error)
                            )
                    elif is_int(_filter):
                        await client.copy_message(message.chat.id, "me", int(_filter))
                    else:
                        await message.reply(
                            text=_filter.format(
                                me=client.me.mention,
                                name=message.from_user.first_name,
                                username=(
                                    f"@{message.from_user.username}"
                                    if message.from_user.username
                                    else None
                                ),
                                mention=message.from_user.mention,
                                id=message.from_user.id,
                                date=(datetime.now(timezone("Asia/Jakarta"))).strftime(
                                    "%A, %d-%B-%Y"
                                ),
                                time=(datetime.now(timezone("Asia/Jakarta"))).strftime(
                                    "%H:%M:%S %Z"
                                ),
                            ),
                        )


@CILIK.UBOT("filter", SUDO=True)
@checkplan
async def filter_user(client, message):
    arg = get_arg(message)
    user_id = client.me.id
    if not arg:
        await message.reply("Usage: `!filter` on/off")
        return
    await set_filter(user_id, arg)
    filter_status_cache[user_id] = arg  # Update the cache
    await message.reply(f"Success! Filter <b>{arg}</b>")


@CILIK.UBOT("addfilter", SUDO=True)
@checkplan
async def _(client, message):
    await set_filter(client.me.id, "on")
    if len(message.command) < 2:
        return await message.reply("Usage: `!addfilter` {filter_name} {text/reply}")
    text = message.text.markdown if message.text else message.caption.markdown
    if message.reply_to_message:
        if message.reply_to_message.text:

            filter_name = message.text.split()[1]
            pesan = re.sub(
                r"\[.*?\]\(buttonurl:.*?\)", "", message.reply_to_message.text.markdown
            )
            buttons = re.findall(
                r"\[.*?\]\(buttonurl:.*?\)", message.reply_to_message.text.markdown
            )

            if buttons:
                await save_filter_button(client.me.id, filter_name, buttons)
                await save_filter(client.me.id, filter_name, pesan)
            else:
                await save_filter(client.me.id, filter_name, pesan)
            await message.reply(
                f"<b>Filter saved!</b>\nfiltername ( <code>{filter_name}</code>)",
                quote=True,
            )
        else:
            filter_name = message.text.split()[1]
            copy = await client.copy_message(
                "me", message.chat.id, message.reply_to_message.id
            )
            await save_filter(client.me.id, filter_name, copy.id)
            await message.reply(
                f"<b>Filter saved!</b>\nfiltername ( <code>{filter_name}</code> )",
                quote=True,
            )
    else:
        name = text.split(None, 1)[1].strip()
        text = name.split(" ", 1)
        if len(text) > 1:
            filter_name = text[0]
            data = text[1].strip()

        pesan = re.sub(r"\[.*?\]\(buttonurl:.*?\)", "", data)
        buttons = re.findall(r"\[.*?\]\(buttonurl:.*?\)", data)

        if buttons:
            await save_filter_button(client.me.id, filter_name, buttons)
            await save_filter(client.me.id, filter_name, pesan)
        else:
            if await get_filter_button(client.me.id, filter_name):
                await rm_filter_button(client.me.id, filter_name)

            await save_filter(client.me.id, filter_name, pesan)
        await message.reply(
            f"<b>Filter saved!</b>\nfiltername ( <code>{filter_name}</code>)",
            quote=True,
        )


def is_int(text):
    try:
        int(text)
    except:
        return False
    return True


@CILIK.UBOT("getfilter", SUDO=True)
@checkplan
async def _(client, message):
    # await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("Usage: `!getfilter` {filter_name}")
    filter_name = message.text.split()[1]
    note = await get_filter(client.me.id, filter_name)
    buttons = await get_filter_button(client.me.id, filter_name)
    if not note:
        return await message.reply(
            f"<b>Filter</b> <code>{filter_name}</code> tidak ada."
        )
    elif buttons:
        try:
            x = await client.get_inline_bot_results(
                username_bot, f"filter_button {filter_name}"
            )
            for m in x.results:
                await client.send_inline_bot_result(
                    message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
                )
        except Exception as error:
            return await message.reply(str(error))
    elif is_int(note):
        await client.copy_message(message.chat.id, "me", int(note))
    else:
        await message.reply(note)
    await message.delete()


@CILIK.UBOT("delfilter", SUDO=True)
@checkplan
async def _(client, message):
    # await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("Usage: `!delfilter` {filter_name}")
    filter_name = message.text.split()[1]
    note = await get_filter(client.me.id, filter_name)
    button = await get_filter_button(client.me.id, filter_name)
    if not note:
        return await message.reply(f"<code>{filter_name}</code> tidak ada di database")
    elif button:
        await rm_filter(client.me.id, filter_name)
        await rm_filter_button(client.me.id, filter_name)
    else:
        await rm_filter(client.me.id, filter_name)

    await message.reply(f"<b>Sukses menghapus filter</b> <code>{filter_name}</code>")


@CILIK.UBOT("delallfilter", SUDO=True)
@checkplan
async def _(client, message):
    # await add_top_cmd(message.command[0])
    try:
        await rm_all_filter(client.me.id)
        await rm_all_filter_button(client.me.id)
        await message.reply("<b>Menghapus semua filters.</b>")
    except Exception as e:
        return await message.reply(str(e))


@CILIK.UBOT("listfilter", SUDO=True)
@checkplan
async def _(client, message):
    # await add_top_cmd(message.command[0])
    try:
        all = await all_filter(client.me.id)
        msg = "<b>Saved Filters</b>\n\n"
        for anu in all:
            msg += f"• <code>{anu}</code>\n"
        await message.reply(msg)
    except Exception:
        await message.reply("<b>Tidak ada filters yang tersimpan.</b>")
