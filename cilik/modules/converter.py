from asyncio import gather

from aiofiles.os import remove as aremove
from pyrogram.enums import MessageMediaType

from cilik.core.handler import CILIK
from cilik.utils.functions import bash

__MODULE__ = "Converter"
__HELP__ = f"""
<b>Media Converter:</b>
<i>Fitur ini berfungsi untuk mengconvert dari satu jenis media ke jenis media lainnya misalkan dari video ke file suara.mp3 dan lainnya.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.toaudio or .tomp3</code> [reply to video / voice]
└⋟ Untuk menconvert file video / voice ke audio (.mp3)

<b>ᴄᴍᴅ:</b>
├⋟<code>.toogg or .tovoice</code> [reply to audio / video]
└⋟ Untuk menconvert file video / audio ke voice (.ogg)

<b>ᴄᴍᴅ:</b>
├⋟<code>.toanime</code> [reply to photo]
└⋟ Untuk merubah foto menjadi foto anime

<b>ᴄᴍᴅ:</b>
├⋟<code>.togif</code> [reply to photo]
└⋟ Untuk merubah video menjadi gif.

<b>ᴄᴍᴅ:</b>
├⋟<code>.tosticker</code> [reply to photo]
└⋟ Untuk merubah foto menjadi sticker.

<b>ᴄᴍᴅ:</b>
├⋟<code>.toimg</code> [reply to photo]
└⋟ Untuk merubah sticker menjadi foto.

<b>ᴄᴍᴅ:</b>
├⋟<code>.totext</code> [reply to video or voice or document voice]
└⋟ Untuk merubah suara menjadi text.

<b>ᴄᴍᴅ:</b>
├⋟<code>.ocr</code> [reply to photo]
└⋟ Untuk mengimplementasikan teks yang ada di gambar.

"""


@CILIK.UBOT("togif", SUDO=True)
async def _(client, message):
    replied = message.reply_to_message
    Tm = await message.reply("<code>Converting to Gif...</code>")
    if not replied:
        await Tm.edit("<b>Reply to video!</b>")
        return
    if replied.media == MessageMediaType.VIDEO:
        file = await client.download_media(
            message=replied,
            file_name="download/",
        )
        out_file = file + ".gif"
        try:
            await bash(f"ffmpeg -i {file} -vf scale=320:-1 -t 10 -r 10 {out_file}")
            await client.send_animation(
                message.chat.id,
                animation=out_file,
                reply_to_message_id=message.id,
            )
            await Tm.delete()
            await aremove(file)
        except BaseException as e:
            await Tm.edit(f"<b>INFO:</b> {e}")
    else:
        await Tm.edit("<b>Reply to video!</b>")
        return


@CILIK.UBOT("tosticker", SUDO=True)
async def _(client, message):
    link = message.reply_to_message
    if not link:
        await message.reply("<b>Reply to photo!</b>")
    else:
        try:
            ya = await link.download(f"{link.photo.file_unique_id}.webp")
            await gather(*[message.reply_sticker(sticker=ya)])
            await aremove(ya)
        except Exception as e:
            await message.reply(str(e))


@CILIK.UBOT("toimg|toimage", SUDO=True)
async def _(client, message):
    r = message.reply_to_message

    if not r:
        return await message.reply("<b>Reply to sticker!</b>")

    if not r.sticker:
        return await message.reply("<b>Reply to sticker!</b>")

    m = await message.reply("<code>Converting to Image...</code>")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    await aremove(f)


@CILIK.UBOT("tomp3|toaudio", SUDO=True)
async def _(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("<b>Reply to media!</b>")
        return
    if replied.media == MessageMediaType.VOICE:
        anu = await replied.download(f"{replied.voice.file_unique_id}.mp3")
    elif replied.media == MessageMediaType.VIDEO:
        anu = await replied.download(f"{replied.video.file_unique_id}.mp3")
    try:
        iya = await message.reply("<code>Converting to audio...</code>")
        await gather(*[message.reply_document(anu, file_name="audio.mp3")])
        await iya.delete()
        await aremove(anu)
    except Exception as e:
        return await message.reply(e)


@CILIK.UBOT("toogg|tovoice", SUDO=True)
async def _(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("<b>Reply to media!</b>")
        return
    if replied.media == MessageMediaType.AUDIO:
        anu = await replied.download(f"{replied.audio.file_unique_id}.ogg")
        durasi = int(replied.audio.duration)
    elif replied.media == MessageMediaType.VIDEO:
        anu = await replied.download(f"{replied.video.file_unique_id}.ogg")
        durasi = int(replied.video.duration)
    try:
        iya = await message.reply("<code>Converting to voice...</code>")
        await gather(*[message.reply_voice(anu, duration=durasi)])
        await iya.delete()
        await aremove(anu)
    except Exception as e:
        return await message.reply(e)
