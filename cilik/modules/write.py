from aiofiles.os import remove as aremove
from PIL import Image, ImageDraw, ImageFont

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

__MODULE__ = "Write"
__HELP__ = f"""
<b>Writing in Book:</b>
<i>Fitur ini berguna untuk kamu yang malas menulis, fitur ini dapat merubah text menjadi gambar buku dengan tulisan tangan.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.write</code> [text]
└⋟ Untuk menulis teks dikertas.
"""


def text_set(text):
    lines = []
    if len(text) <= 55:
        lines.append(text)
    else:
        all_lines = text.split("\n")
        for line in all_lines:
            if len(line) <= 55:
                lines.append(line)
            else:
                k = len(line) // 55
                for z in range(1, k + 2):
                    lines.append(line[((z - 1) * 55) : (z * 55)])
    return lines[:25]


@CILIK.UBOT("write|nulis|tulis", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.reply("<b>Berikan Text atau Reply</b>")
    k = await message.reply("<code>✍️ Writing...</code>")
    img = Image.open("cilik/resources/kertas.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("cilik/resources/assfont.ttf", 30)
    x, y = 150, 140
    lines = text_set(text)
    line_height = font.getsize("hg")[1]
    for line in lines:
        draw.text((x, y), line, fill=(1, 22, 55), font=font)
        y = y + line_height - 5
    file = "cilik.jpg"
    img.save(file)
    await message.reply_photo(photo=file)
    await aremove(file)
    await k.delete()


@CILIK.UBOT("bon|nota")
async def _(client, message):
    text = f"""
    
    
    

   NAME : UDIN
   ID : 1234344555 
   BULAN : 3 
   EXPIRED : 06-Juli-2003
"""
    k = await message.reply("<code>✍️ Writing...</code>")
    img = Image.open("cilik/resources/nota.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("cilik/resources/atwriter.ttf", 70)
    x, y = 150, 140
    lines = text_set(text)
    line_height = font.getsize("hg")[1]
    for line in lines:
        draw.text((x, y), line, fill=(1, 22, 55), font=font)
        y = y + line_height - 5
    file = "grey.png"
    img.save(file)
    await message.reply_photo(photo=file)
    await aremove(file)
    await k.delete()
