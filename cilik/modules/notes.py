import re
from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ParseMode
from pytz import timezone

from cilik import ubot, username_bot
from cilik.core.database import *
from cilik.core.handler import CILIK, checkplan


@CILIK.UBOT("addnote", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("Usage: !addnote {note_name} {text/reply}")
    text = message.text.markdown if message.text else message.caption.markdown
    if message.reply_to_message:
        if message.reply_to_message.text:

            note_name = message.text.split()[1]
            pesan = re.sub(
                r"\[.*?\]\(buttonurl:.*?\)", "", message.reply_to_message.text.markdown
            )
            buttons = re.findall(
                r"\[.*?\]\(buttonurl:.*?\)", message.reply_to_message.text.markdown
            )

            if buttons:
                await save_note_button(client.me.id, note_name, buttons)
                await save_note(client.me.id, note_name, pesan)
            else:
                await save_note(client.me.id, note_name, pesan)
                ceking = await get_note_button(client.me.id, note_name)
                if ceking:
                    await remove_note_button(client.me.id, note_name)
            await message.reply(
                f"<b>Note saved!</b>\nnotename ( <code>{note_name}</code>)", quote=True
            )
        else:
            note_name = message.text.split()[1]
            copy = await client.copy_message(
                "me", message.chat.id, message.reply_to_message.id
            )
            await save_note(client.me.id, note_name, copy.id)
            await message.reply(
                f"<b>Note saved!</b>\nnotename ( <code>{note_name}</code> )", quote=True
            )
    else:
        name = text.split(None, 1)[1].strip()
        text = name.split(" ", 1)
        if len(text) > 1:
            note_name = text[0]
            data = text[1].strip()

        pesan = re.sub(r"\[.*?\]\(buttonurl:.*?\)", "", data)
        buttons = re.findall(r"\[.*?\]\(buttonurl:.*?\)", data)

        if buttons:
            await save_note_button(client.me.id, note_name, buttons)
            await save_note(client.me.id, note_name, pesan)
        else:
            await save_note(client.me.id, note_name, pesan)
            ceking = await get_note_button(client.me.id, note_name)
            if ceking:
                await rm_note_button(client.me.id, note_name)
        await message.reply(
            f"<b>Note saved!</b>\nnotename ( <code>{note_name}</code>)", quote=True
        )


def is_int(text):
    try:
        int(text)
    except:
        return False
    return True


@CILIK.UBOT("sget", SUDO=True)
@checkplan
async def _(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("Usage: !sget {note_name}")
    note_name = message.text.split()[1]
    note = await get_note(client.me.id, note_name)
    buttons = await get_note_button(client.me.id, note_name)
    if not note:
        return await message.reply(f"<b>Note</b> <code>{note_name}</code> tidak ada.")
    elif buttons:
        try:
            x = await client.get_inline_bot_results(
                username_bot,
                f"note_button {note_name} {message.chat.first_name} {message.chat.username} {message.chat.id}",
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
        await message.reply(
            text=note.format(
                me=client.me.mention,
                name=message.chat.first_name,
                username=(
                    f"@{message.chat.username}" if message.chat.username else None
                ),
                mention=f"[{message.chat.first_name}](tg://user?id={message.chat.id})",
                id=message.chat.id,
                date=(datetime.now(timezone("Asia/Jakarta"))).strftime("%A, %d-%B-%Y"),
                time=(datetime.now(timezone("Asia/Jakarta"))).strftime("%H:%M:%S %Z"),
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=message.id,
        )
    await message.delete()


@CILIK.UBOT("get", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("Usage: !get {note_name}")
    note_name = message.text.split()[1]
    note = await get_note(client.me.id, note_name)
    buttons = await get_note_button(client.me.id, note_name)
    if not note:
        return await message.reply(f"<b>Note</b> <code>{note_name}</code> tidak ada.")
    elif buttons:
        try:
            x = await client.get_inline_bot_results(
                username_bot,
                f"note_button {note_name} {message.chat.first_name} {message.chat.username} {message.chat.id}",
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
        await message.reply(
            text=note.format(
                me=client.me.mention,
                name=message.chat.first_name,
                username=(
                    f"@{message.chat.username}" if message.chat.username else None
                ),
                mention=f"[{message.chat.first_name}](tg://user?id={message.chat.id})",
                id=message.chat.id,
                date=(datetime.now(timezone("Asia/Jakarta"))).strftime("%A, %d-%B-%Y"),
                time=(datetime.now(timezone("Asia/Jakarta"))).strftime("%H:%M:%S %Z"),
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=message.id,
        )


@CILIK.UBOT("delnote", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply("Usage: !delnote {note_name}")
    note_name = message.text.split()[1]
    note = await get_note(client.me.id, note_name)
    button = await get_note_button(client.me.id, note_name)
    if not note:
        return await message.reply(f"<code>{note_name}</code> tidak ada di database")
    elif button:
        await rm_note(client.me.id, note_name)
        await rm_note_button(client.me.id, note_name)
    else:
        await rm_note(client.me.id, note_name)

    await message.reply(f"<b>Sukses menghapus note</b> <code>{note_name}</code>")


@CILIK.UBOT("delallnote", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    try:
        await rm_all(client.me.id)
        await rm_all_note_button(client.me.id)
        await message.reply("<b>Menghapus semua note.</b>")
    except Exception as e:
        return await message.reply(str(e))


@ubot.on_message(filters.regex(r"^#.+") & filters.text & filters.me)
async def get_one_note(client, message):
    print(message)
    note_name = message.text.replace("#", "", 1)
    if not note_name:
        return
    note = await get_note(client.me.id, note_name)
    buttons = await get_note_button(client.me.id, note_name)
    if not note:
        return await message.reply(f"<b>Note</b> <code>{note_name}</code> tidak ada.")
    elif buttons:
        try:
            x = await client.get_inline_bot_results(
                username_bot,
                f"note_button {note_name} {message.chat.first_name} {message.chat.username} {message.chat.id}",
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
        await message.reply(
            text=note.format(
                me=client.me.mention,
                name=message.chat.first_name,
                username=(
                    f"@{message.chat.username}" if message.chat.username else None
                ),
                mention=f"[{message.chat.first_name}](tg://user?id={message.chat.id})",
                id=message.chat.id,
                date=(datetime.now(timezone("Asia/Jakarta"))).strftime("%A, %d-%B-%Y"),
                time=(datetime.now(timezone("Asia/Jakarta"))).strftime("%H:%M:%S %Z"),
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=message.id,
        )


@CILIK.UBOT("markdownhelp", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    try:
        x = await client.get_inline_bot_results(
            username_bot, f"markdown_help {message.id} {message.chat.id}"
        )
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
            )
    except Exception as error:
        await message.reply(str(error))


@CILIK.UBOT("notes", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    try:
        all = await all_notes(client.me.id)
        msg = "<b>Saved Notes</b>\n\n"
        for anu in all:
            msg += f"• <code>{anu}</code>\n"
        await message.reply(msg)
    except Exception:
        await message.reply("<b>Tidak ada catatan yang tersimpan.</b>")
