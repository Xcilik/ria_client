from cilik import username_bot
from cilik.core.handler import CILIK, checkplan


@CILIK.UBOT("hitung|calculator|kalkulator", SUDO=True)
@checkplan
async def calc_message(client, message):
    try:
        x = await client.get_inline_bot_results(username_bot, "callculator")
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
            )
    except Exception as error:
        return await message.reply(str(error))
