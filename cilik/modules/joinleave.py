from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, checkplan

__MODULE__ = "JoinLeave"
__HELP__ = f"""
<b>Join / Leave:</b>
<i>Fitur ini berfungsi untuk bergabung atau keluar dari grup/channel atau semua grup/channel</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.join</code> [chat_id / username chat]
└⋟ Untuk bergabung ke dalam grup/channel

<b>ᴄᴍᴅ:</b>
├⋟<code>.kickme</code> or <code>.leave</code> [chat_id / username chat]
└⋟ Untuk keluar dari grup / channel
 
<b>ᴄᴍᴅ:</b>
├⋟<code>.leaveallgc</code>
└⋟ Untuk keluar dari semua grup.

<b>ᴄᴍᴅ:</b>
├⋟<code>.leaveallch</code>
└⋟ Untuk keluar dari semua channel.
"""


JANGAN = [
    -1001917973794,
    -1001874736197,
    -1001473548283,
    -1001687155877,
    -1001830597771,
]


@CILIK.UBOT("join", SUDO=True)
async def join(client, message):
    await add_top_cmd(message.command[0])
    Man = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not Man:
        return await message.reply("**Berikan chat_id/username!**")
    xxnx = await message.reply("`Joining...`")
    try:
        await xxnx.edit(f"<b>Berhasil Bergabung ke Chat ID</b> <code>{Man}</code>")
        await client.join_chat(Man)
    except Exception as ex:
        await xxnx.edit(f"<b>Error:</b> \n\n{str(ex)}")


@CILIK.UBOT("leave|kickme", SUDO=True)
async def leave(client, message):
    await add_top_cmd(message.command[0])
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply("leave this group...")
    if message.chat.id in JANGAN:
        return await xxnx.edit("Perintah ini Dilarang digunakan di Group ini!")
    try:
        await xxnx.edit_text(f"{client.me.first_name} has left this group, bye!!")
        await client.leave_chat(Man)
    except Exception as ex:
        await xxnx.edit_text(f"<b>Error:</b> \n\n{str(ex)}")


@CILIK.UBOT("leaveallgc", SUDO=True)
@checkplan
async def kickmeall(client, message):
    await add_top_cmd(message.command[0])
    Man = await message.reply("`Global Leave from group chats...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type.value in ("group", "supergroup"):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"<b>Berhasil Keluar dari {done} Group, Gagal Keluar dari {er} Group</b>"
    )


@CILIK.UBOT("leaveallch", SUDO=True)
@checkplan
async def kickmeallch(client, message):
    await add_top_cmd(message.command[0])
    Man = await message.reply("`Global Leave from channel...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type.value == "channel":
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"<b>Berhasil Keluar dari {done} Channel, Gagal Keluar dari {er} Channel</b>"
    )
