from asyncio import gather
from io import BytesIO

from cilik import aiohttpsession
from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

# from cilik.utils.functions import make_carbon


async def make_carbon(code, bg_color="rgba(171, 184, 195, 1)"):
    url = "https://carbonara.solopov.dev/api/cook"
    data = {"code": code, "backgroundColor": bg_color}
    async with aiohttpsession.post(url, json=data) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@CILIK.UBOT("carbon", SUDO=True)
async def carbon_func(client, message):
    await add_top_cmd(message.command[0])
    color_map = {
        "blue": "rgba(0, 47, 255, 0.8)",
        "black": "rgba(0, 0, 0, 1)",
        "green": "rgba(0, 255, 0, 1)",
        "white": "rgba(0, 255, 0, 0)",
        "pink": "rgba(255, 57, 255, 0.8)",
        "red": "rgba(255, 0, 0, 1)",
        "grey": "rgba(0, 46, 105, 0.57)",
        "yellow": "rgba(255, 255, 0, 0.57)",
        "orange": "rgba(255, 155, 0, 1)",
        "purple": "rgba(189, 0, 255, 1)",
    }

    text = None
    bg_color = "rgba(171, 184, 195, 1)"  # Default background color

    if len(message.command) > 1:
        color_command = message.text.split()[1]
        if color_command in color_map:
            bg_color = color_map[color_command]
            if len(message.command) > 2:
                text = message.text.split(None, 2)[2]
        elif len(message.command) > 1:
            text = message.text.split(None, 1)[1]

    if message.reply_to_message and not text:
        replied_text = message.reply_to_message.text or message.reply_to_message.caption
        if replied_text:
            text = replied_text

    if not text:
        return await message.reply(
            "colour = {blue, black, green, white, pink, red, grey, yellow, orange, purple}\n\n!carbon text/reply or !carbon {colour} text/reply",
            quote=True,
        )

    ex = await message.reply("Carboning...", quote=True)
    carbon = await make_carbon(text, bg_color)
    await gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"<b>Carbonised By : </b>{client.me.mention}",
        ),
    )
    carbon.close()
