from random import randint
from typing import Optional

from pyrogram import Client
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.functions.phone import EditGroupCallTitle as vctitle
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import ChatPermissions, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, FILTERS

__MODULE__ = "Vctools"
__HELP__ = f"""
<b>VoiceChat Tools:<b>
<i>Fitur ini berfungsi untuk mengcontrol Obrolan Suara (OS) group, serta kamu dapat melakukan fake OS.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.joinvc</code> or <code>.naik</code> [username group/channel]
└⋟ Untuk bergabung ke obrolan suara [fake os]

<b>ᴄᴍᴅ:</b>
├⋟<code>.leavevc</code> or <code>.turun</code> [username group/channel]
└⋟ Untuk turun dari obrolan suara [fake os]

<b>ᴄᴍᴅ:</b>
├⋟<code>.startvc</code> 
└⋟ Untuk membuka obrolan suara [os]

<b>ᴄᴍᴅ:</b>
├⋟<code>.stopvc</code> 
└⋟ Untuk menutup obrolan suara [os]

"""

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"<b>No group call Found</b> {err_msg}")
    return False


@CILIK.UBOT("startvc", FILTERS.ME_GROUP, SUDO=True)
async def _(client, m: Message):
    await add_top_cmd(m.command[0])
    chat_id = m.chat.id
    try:
        await client.invoke(
            CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
            )
        )
        await m.reply("<b>Voicechat started!</b>")
    except Exception as e:
        await m.reply(str(e))


@CILIK.UBOT("stopvc", FILTERS.ME_GROUP, SUDO=True)
async def _(client, m: Message):
    await add_top_cmd(m.command[0])
    if not (
        group_call := (
            await get_group_call(client, m, err_msg=", group call already ended")
        )
    ):
        return await m.reply("group call already ended!")
    try:
        await client.send(DiscardGroupCall(call=group_call))
        await m.reply("<b>Ended group call...</b>")
    except Exception as e:
        await m.reply(str(e))


@CILIK.UBOT("joinvc|naik", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    file = "./cilik/resources/cilikvc.mp3"
    if chat_id:
        try:
            await client.call_py.join_group_call(
                chat_id, InputStream(InputAudioStream(file), None)
            )
            msg = "<b>Joined to voicechat</b>\n"
            if not len(message.command) > 1:
                await message.reply(msg)
            elif len(message.command) > 1:
                msg += f"<b>Chat Id:</b> {chat_id}"
                await message.reply(msg)
        except Exception as e:
            await message.reply(str(e))


@CILIK.UBOT("gbut", FILTERS.ME_GROUP)
async def _(client, m: Message):
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    file = "./cilik/resources/cilikvc.mp3"
    if chat_id:
        try:
            await client.call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
            )
            msg = "<b>Joined to voicechat</b>\n"
            if not len(m.command) > 1:
                await m.edit("gabut")
            elif len(m.command) > 1:
                msg += f"<b>Chat Id:</b> {chat_id}"
                await m.reply("gabut")
        except Exception:
            await m.reply("gabut")


@CILIK.UBOT("leavevc|turun|end", FILTERS.ME_GROUP, SUDO=True)
async def _(client, m: Message):
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    if chat_id:
        try:
            await client.call_py.leave_group_call(chat_id)
            msg = "<b>Leaved to voicechat</b>\n"
            if not len(m.command) > 1:
                await m.reply(msg)
            elif len(m.command) > 1:
                msg += f"<b>Chat Id:</b> {chat_id}"
                await m.reply(msg)
        except Exception as e:
            await m.reply(str(e))


@CILIK.UBOT("vctitle|judulos", FILTERS.ME_GROUP, SUDO=True)
async def _(client: Client, message: Message):
    title = len(message.command) > 1
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("You don't have enough permission")
    group_call = await get_group_call(
        client, message, err_msg=", group call already ended"
    )
    if not title:
        return await message.reply("<b>Usage:</b> <code>.vctitle halo semua</code>")
        return
    try:
        await client(vctitle(call=group_call, title=title))
        await message.reply(f"<b>Mengubah voice title\ntitle:</b> <code>{title}</code>")
    except Exception as ex:
        await message.reply(f"<b>Error:</b> <code>{ex}</code>")


@CILIK.UBOT("runyek", FILTERS.ME_GROUP)
async def _(client, m: Message):
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    file = "./cilik/resources/yanto.mp3"
    if chat_id:
        try:
            await client.call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            msg = "<b>Joined to voicechat</b>\n"
            if not len(m.command) > 1:
                await m.reply(msg)
            elif len(m.command) > 1:
                msg += f"<b>Chat Id:</b> {chat_id}"
                await m.reply(msg)
        except Exception as e:
            await m.reply(f"<b>Error:</b> {e}")
