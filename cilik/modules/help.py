from cilik import username_bot
from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, checkplan


@CILIK.UBOT("alive|menu|help", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    if message.command[0] == "alive":
        text = f"user_alive_command {message.id} {client.me.id} {client.me.dc_id} {message.chat.id}"
    elif message.command[0] == "help":
        text = "help"
    elif message.command[0] == "menu":
        text = "help"
    try:
        x = await client.get_inline_bot_results(username_bot, text)
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
            )
    except Exception as error:
        await message.reply(error)


@CILIK.UBOT("pdftoimg|imgtopdf", SUDO=True)
@checkplan
async def _(client, message):
    await add_top_cmd(message.command[0])
    if message.command[0] == "pdftoimg":
        text = "pdftoimg"
    elif message.command[0] == "imgtopdf":
        text = "imgtopdf"
    try:
        x = await client.get_inline_bot_results(username_bot, text)
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
            )
    except Exception as error:
        await message.reply(error)
