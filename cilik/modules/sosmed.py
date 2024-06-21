from asyncio import sleep

from pyrogram.enums import MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

__MODULE__ = "Downloader"
__HELP__ = f"""
<b>Media Downloader:</b>
<i>Fitur ini berfungsi untuk mendownload media dari platform seperti Tiktok / Instagram / Twitter / Google / YouTube.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.dl</code> [link]
└⋟ Untuk Mendownload Media Dari Tiktok/Instagram/Twitter/X.

<b>ᴄᴍᴅ:</b>
├⋟<code>.pic</code> [query]
├⋟ <b>example:</b> <code>.pic</code> lion digital art.
└⋟ Untuk Mendownload Gambar Dari Google.

<b>ᴄᴍᴅ:</b>
├⋟<code>.song</code> [judul lagu]
├⋟ <b>example:</b> <code>.song</code> Surat cinta untuk starla.
└⋟ Untuk Mendownload Lagu.

<b>ᴄᴍᴅ:</b>
├⋟<code>.vid</code> [judul video]
├⋟ <b>example:</b> <code>.vid</code> doraemon.
└⋟ Untuk Mendownload Video.

"""


@CILIK.UBOT("dl|download", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        link = message.reply_to_message.text or message.reply_to_message.caption
    if not link:
        await message.reply("Usage: <code>!dl or !download</code> {link}")
    else:
        Tm = await message.reply("<code>Downloading...</code>")
        if "tiktok" in link:
            bot = "downloader_tiktok_bot"
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await xnxx.delete()
            await sleep(3)
            async for sosmed in client.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                await Tm.edit("Uploading...")
                try:
                    await client.copy_media_group(
                        message.chat.id,
                        "@downloader_tiktok_bot",
                        sosmed.id,
                        captions="Done!\n\nSuccess downloaded from TikTok!",
                        reply_to_message_id=message.id,
                    )
                    await Tm.delete()
                except:
                    await sosmed.copy(
                        message.chat.id,
                        caption="Done!\n\nSuccess downloaded from TikTok!",
                    )
                    await Tm.delete()

            user_info = await client.resolve_peer(bot)
            return await client.send(
                DeleteHistory(peer=user_info, max_id=0, revoke=True)
            )

        elif "instagram" in link:
            bot = "SaveAsBot"
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await xnxx.delete()
            await sleep(5)
            async for sosmed in client.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                await Tm.edit("Uploading...")
                try:
                    await client.copy_media_group(
                        message.chat.id,
                        "@SaveAsBot",
                        sosmed.id,
                        captions="Done!\n\nSuccess downloaded from Instagram!",
                        reply_to_message_id=message.id,
                    )
                    await Tm.delete()
                except:
                    await sosmed.copy(
                        message.chat.id,
                        caption="Done!\n\nSuccess downloaded from Instagram!",
                    )
                    await Tm.delete()

            user_info = await client.resolve_peer(bot)
            return await client.send(
                DeleteHistory(peer=user_info, max_id=0, revoke=True)
            )

        elif "twitter" in link or "x.com" in link:
            bot = "xvideosdwbot"
            await client.join_chat("xcombotnews")
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await xnxx.delete()
            await sleep(5)
            async for sosmed in client.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                await Tm.edit("Uploading...")
                try:
                    await client.copy_media_group(
                        message.chat.id,
                        "@xvideosdwbot",
                        sosmed.id,
                        captions="Done!\n\nSuccess downloaded from X Twitter!",
                        reply_to_message_id=message.id,
                    )
                    await Tm.delete()

                except:
                    await sosmed.copy(
                        message.chat.id,
                        caption="Done!\n\nSuccess downloaded from X Twitter!",
                    )
                    await Tm.delete()

            user_info = await client.resolve_peer(bot)
            return await client.send(
                DeleteHistory(peer=user_info, max_id=0, revoke=True)
            )

        else:
            await message.reply("not valid link")
