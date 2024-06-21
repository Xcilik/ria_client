from aiofiles.os import remove as aremove
from aiofiles.ospath import exists
from removebg import RemoveBg

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

RMBG_API = "XX4EyKfYviwpuckre6HsaHCU"
DOWN_PATH = "downloads/"
IMG_PATH = DOWN_PATH + "rmbg.jpg"


@CILIK.UBOT("rmbg", SUDO=True)
async def remove_bg(client, message):
    await add_top_cmd(message.command[0])
    if not RMBG_API:
        return
    Tm = await message.reply("`Analysing...`")
    replied = message.reply_to_message
    if replied.photo or replied.document or replied.sticker or replied.animation:
        if await exists(IMG_PATH):
            await aremove(IMG_PATH)
        await client.download_media(message=replied, file_name=IMG_PATH)
        await Tm.edit("`Removed background...`")
        try:
            rmbg = RemoveBg(RMBG_API, "rm_bg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            remove_img = IMG_PATH + "_no_bg.png"
            await client.send_photo(
                chat_id=message.chat.id,
                photo=remove_img,
                reply_to_message_id=message.id,
                disable_notification=True,
            )
            await Tm.delete()
        except Exception as e:
            print(e)
            await Tm.edit("<b>Error!</b>")
    else:
        await Tm.edit("Usage: <code>!rmbg</code> {reply to photo}")
