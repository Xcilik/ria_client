from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK


@CILIK.UBOT("id", SUDO=True)
async def getid(client, message):
    await add_top_cmd(message.command[0])
    chat = message.chat
    your_id = client.me.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"<b><a href={message.link}>Message ID:</a></b> <code>{message_id}</code>\n"
    text += (
        f"<b><a href=tg://user?id={your_id}>Your ID:</a></b> <code>{your_id}</code>\n"
    )

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"<b>User ID:</b> <code>{user_id}</code>\n"
        except Exception:
            return await message.reply(text="This user doesn't exist.")

    text += f"<b><a href=https://t.me/{chat.username}>Chat ID:</a></b> <code>{chat.id}</code>\n\n"
    if not getattr(reply, "empty", True):
        id_ = reply.from_user.id if reply.from_user else reply.sender_chat.id
        text += f"<b><a href={reply.link}>Replied Message ID:</a></b> <code>{reply.id}</code>\n"
        text += (
            f"<b><a href=tg://user?id={id_}>Replied User ID:</a></b> <code>{id_}</code>"
        )

    await message.reply(
        text=text,
        disable_web_page_preview=True,
    )
