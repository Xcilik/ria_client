import asyncio

from aiofiles.os import makedirs
from aiofiles.os import remove as aremove
from aiofiles.ospath import isdir
from bs4 import BeautifulSoup

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

DOWN_PATH = "CilikQrCode/"


__MODULE__ = "QrCode"
__HELP__ = f"""
<b>QrCode:</b>
<i>Fitur ini berfungsi untuk merubah kode <b>QR</b> text menjadi gambar <b>QR</b>, serta dapat membaca kode <b>QR.</b></i>

<b>ᴄᴍᴅ:</b>
├⋟ <code>.qrgen</code> [text QRcode]
└⋟ Untuk merubah QRcode text menjadi gambar.

<b>ᴄᴍᴅ:</b>
├⋟<code>.qrread</code> [reply to media]
└⋟ Untuk merubah QRcode menjadi text.
"""


@CILIK.UBOT("qrgen", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    ID = message.reply_to_message or message
    if message.reply_to_message:
        texts = message.reply_to_message.text
    else:
        if len(message.command) < 2:
            return await message.delete()
        else:
            texts = message.text.split(None, 1)[1]
    Tm = await message.reply("Processing QRcode. . .")
    text = texts.replace(" ", "%20")
    QRcode = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={text}"
    await client.send_photo(message.chat.id, QRcode, reply_to_message_id=ID.id)
    await Tm.delete()


@CILIK.UBOT("qrread", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    replied = message.reply_to_message
    if not (replied and replied.media and (replied.photo or replied.sticker)):
        TM = await message.reply("<b>Reply to photo Qr!</b>")
        return
    if not await isdir(DOWN_PATH):
        await makedirs(DOWN_PATH)
    AM = await message.reply("`Downloading Qr...`")
    down_load = await client.download_media(message=replied, file_name=DOWN_PATH)
    await AM.edit("`Reading QRcode...`")
    cmd = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + down_load + "",
        "https://zxing.org/w/decode",
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    out_response = stdout.decode().strip()
    err_response = stderr.decode().strip()
    await aremove(down_load)
    if not (out_response or err_response):
        await AM.edit("Tidak bisa mendapatkan data Kode QR ini...")
        return
    try:
        soup = BeautifulSoup(out_response, "html.parser")
        qr_contents = soup.find_all("pre")[0].text
    except IndexError:
        await TM.edit("Indeks Daftar Di Luar Jangkauan")
        return
    await AM.edit(f"<b>Data QRCode:</b>\n<code>{qr_contents}</code>")
