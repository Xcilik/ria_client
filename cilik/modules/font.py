from cilik import username_bot
from cilik.core.database import add_top_cmd, set_font
from cilik.core.handler import CILIK, checkplan
from cilik.utils.functions import get_text

__MODULE__ = "Fonts"
__HELP__ = f"""
<b>Fonts Generator:</b>
<i>Fitur ini berfungsi untuk merubah font biasa menjadi font ascii / font model.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.font</code> [text] or reply to message
└⋟ Merubah fonts.
"""


@CILIK.UBOT("font", SUDO=True)
@checkplan
async def font_message(client, message):
    await add_top_cmd(message.command[0])
    args = get_text(message)
    if not args:
        return await message.reply("**Berikan text/reply!**")
    await set_font(client.me.id, args)
    try:
        x = await client.get_inline_bot_results(username_bot, "get_font")
        for m in x.results:
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
            )
    except Exception as error:
        return await message.reply(str(error))
