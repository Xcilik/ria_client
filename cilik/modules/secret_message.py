from cilik import username_bot
from cilik.core.database import save_secret_button
from cilik.core.handler import CILIK


@CILIK.UBOT("msg", SUDO=True)
async def _(client, message):
    await message.delete()
    if len(message.command) < 2:
        return await client.send_message(
            message.chat.id, ".msg {reply/user_id/username} {text}"
        )
    elif message.reply_to_message:
        target = message.reply_to_message.from_user.id
        text = message.text.split(None, maxsplit=1)[1]

    elif len(message.command) > 2:
        target = message.text.split()[1]
        text = message.text.split(None, maxsplit=2)[2]
    else:
        return await client.send_message(
            message.chat.id, ".msg {reply/user_id/username} {text}"
        )

    try:
        user = await client.get_users(target)
        target = user.id
    except:
        target = target

    reply_me_or_user = message.reply_to_message or message

    await save_secret_button(client.me.id, f"{target}", text)

    parts = message.link.rsplit("/", 1)
    new_link = f"{parts[0]}/{int(parts[1]) + 1}"
    try:
        x = await client.get_inline_bot_results(
            username_bot,
            f"secret {target} {new_link}",
        )
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id,
                x.query_id,
                m.id,
                reply_to_message_id=reply_me_or_user.id,
            )
    except Exception as error:
        return await client.send_message(message.chat.id, str(error))
