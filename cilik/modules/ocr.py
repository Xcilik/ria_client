import asyncio

import requests
from aiofiles import open as aopen
from aiofiles.os import remove as aremove

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, checkplan

OCR_SPACE_API_KEY = "30dd97e2b588957"


async def ocr_space_file(
    filename, overlay=False, api_key=OCR_SPACE_API_KEY, language="eng"
):
    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    async with aopen(filename, "rb") as f:
        r = await asyncio.to_thread(
            requests.post,
            "https://api.ocr.space/parse/image",
            files={filename: await f.read()},
            data=payload,
        )
    return r.json()


@CILIK.UBOT("ocr", SUDO=True)
@checkplan
async def ocr(client, message):
    await add_top_cmd(message.command[0])
    cmd = message.command
    lang_code = ""
    if len(cmd) > 1:
        lang_code = " ".join(cmd[1:])
    elif len(cmd) == 1:
        lang_code = "eng"
    replied = message.reply_to_message
    if not replied:
        await message.reply("<b>Reply to image!</b>")
        return
    if replied.video:
        await message.delete()
        return
    if replied.document:
        await message.delete()
        return
    if replied.voice:
        await message.delete()
        return
    if replied.audio:
        await message.delete()
        return
    if replied.photo:
        reply_p = replied.photo
    elif replied.sticker:
        reply_p = replied.sticker
    downloaded_file_name = await client.download_media(
        reply_p,
        "cilik/resources/file.png",
    )
    test_file = await ocr_space_file(
        filename=downloaded_file_name,
        language=lang_code,
    )
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException as e:
        await message.reply(e)
    else:
        if ParsedText == "ParsedResults":
            await message.delete()
            return
        else:
            await message.reply(f"{ParsedText}")
    await aremove(downloaded_file_name)
