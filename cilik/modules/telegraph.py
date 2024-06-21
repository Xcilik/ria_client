from aiofiles.os import remove as aremove
from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from cilik import username_bot
from cilik.core.handler import CILIK

telegraph = Telegraph()


@CILIK.UBOT("tgm")
async def _(client, message):
    XD = await message.reply("<code>Telegraph...</code>")
    if not message.reply_to_message:
        await XD.edit("<b>Reply to message/photo!</b>")
        return

    try:
        get_result = telegraph.create_account(short_name="cilik")
    except exceptions.RetryAfterError as err:
        await XD.edit(
            f"<b>Error:</b> Flood control exceeded. Retry in {err.retry_after} seconds."
        )
        return

    get_result["auth_url"]

    if message.reply_to_message.photo:
        m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await XD.edit(f"<b>ERROR:</b> <code>{exc}</code>")
            await aremove(m_d)
            return
        U_done = f"https://telegra.ph/{media_url[0]}"

        try:
            x = await client.get_inline_bot_results(username_bot, f"tg_m {U_done}")
            for m in x.results:
                await client.send_inline_bot_result(
                    message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
                )
            await XD.delete()
        except Exception as error:
            await XD.edit(str(error))

        await aremove(m_d)

    elif message.reply_to_message.sticker:
        m_d = await message.reply_to_message.download()
        with Image.open(m_d) as im:
            im = im.convert("RGB")
            im.save("output.jpg", "JPEG")
        try:
            media_url = upload_file("output.jpg")
        except exceptions.TelegraphException as exc:
            await XD.edit(f"<b>ERROR:</b> <code>{exc}</code>")
            await aremove(m_d)
            return
        U_done = f"https://telegra.ph/{media_url[0]}"

        try:
            x = await client.get_inline_bot_results(username_bot, f"tg_m {U_done}")
            for m in x.results:
                await client.send_inline_bot_result(
                    message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
                )
            await XD.delete()
        except Exception as error:
            await XD.edit(str(error))

        await aremove(m_d)

    elif message.reply_to_message.text:
        page_title = f"{client.me.first_name} {client.me.last_name or ''}"
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await XD.edit(f"<b>ERROR:</b> <code>{exc}</code>")
            return
        wow_graph = f"https://telegra.ph/{response['path']}"
        try:
            x = await client.get_inline_bot_results(username_bot, f"tg_m {wow_graph}")
            for m in x.results:
                await client.send_inline_bot_result(
                    message.chat.id, x.query_id, m.id, reply_to_message_id=message.id
                )
            await XD.delete()
        except Exception as error:
            await XD.edit(str(error))
