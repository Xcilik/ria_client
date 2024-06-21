import random
from io import BytesIO

from freeGPT import AsyncClient

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK
from cilik.utils.functions import get_text

__MODULE__ = "OpenAI"
__HELP__ = f"""
<b>OpenAI:</b>
<b>OpenAI</b> <i>adalah sistem ChatGPT / kecerdasan buatan fitur ini akan membantu kamu untuk menjawab pertanyaan dengan benar.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.ai</code> or <code>.openai</code> [teks]
├⋟ Generate or manipulated teks.
└⋟ <b>example:</b> <code>.ai</code> contoh code python simple.

<b>ᴄᴍᴅ:</b>
├⋟<code>.aski</code> or <code>.dalle</code> [teks]
├⋟ Generate or manipulated image.
└⋟ <b>example:</b> <code>.aski</code> cat black and white.
"""


async def memek(text):
    prompt = text
    try:
        resp = await AsyncClient.create_completion("gpt3", prompt)
        return resp
    except Exception as e:
        return e
    return resp, e


@CILIK.UBOT("Ai|ai|ask|Ask|openai|Openai", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    args = get_text(message)
    if not args:
        return await message.reply("<b>What???</b>")
    Tm = await message.reply("<code>Generated Text...</code>")
    try:
        response = await memek(args)
        msg = message.reply_to_message or message
        await client.send_message(message.chat.id, response, reply_to_message_id=msg.id)
    except Exception as error:
        await message.reply(str(error))
    await Tm.delete()


@CILIK.UBOT("aski|Aski|Dalle|dalle", SUDO=True)
async def curie(client, message):
    await add_top_cmd(message.command[0])
    msg = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not msg:
        await message.reply("<b>What image to manipulated?</b>")
    else:
        cilik = await message.reply("<code>Manipulated image...</code>")
        iye = ["pollinations", "prodia"]
        meme = random.choice(iye)
        try:
            resp = await AsyncClient.create_generation(meme, msg)
            img_bytes = BytesIO(resp)
            await message.reply_photo(photo=img_bytes)
            await cilik.delete()
        except Exception as e:
            await cilik.edit(f"{e}")
