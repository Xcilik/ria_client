from asyncio import get_event_loop
from functools import partial

import wget
from aiofiles.os import remove as aremove
from aiofiles.ospath import exists as aexists
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, checkplan


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


@CILIK.UBOT("vid|video", SUDO=True)
async def yt_video(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Berikan Judul!</b>",
        )
    try:
        search = (
            SearchVideos(
                str(message.text.split(None, 1)[1]),
                offset=1,
                mode="dict",
                max_results=1,
            )
            .result()
            .get("search_result")
        )
        link = f"https://youtu.be/{search[0]['id']}"
    except Exception as error:
        return await message.reply(f"<b>Error: {error}</b>")
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    infomsg = await message.reply(f"<code>Downloading videos...</code>")
    try:
        ytdl_data = await run_sync(ydl.extract_info, link, download=True)
        file_path = ydl.prepare_filename(ytdl_data)
        videoid = ytdl_data["id"]
        title = ytdl_data["title"]
        url = f"https://youtu.be/{videoid}"
        duration = ytdl_data["duration"]
        channel = ytdl_data["uploader"]
        views = f"{ytdl_data['view_count']:,}".replace(",", ".")
        thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    except Exception as error:
        return await infomsg.edit(f"<b>Error:</b> {error}")
    thumbnail = wget.download(thumbs)
    await client.send_video(
        message.chat.id,
        video=file_path,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption="<b>💡 Informasi {}</b>\n\n<b>🏷 Nama:</b> {}\n<b>🧭 Durasi:</b> {}\n<b>👀 Dilihat:</b> {}\n<b>📢 Channel:</b> {}\n<b>🔗 Tautan:</b> <a href={}>Youtube</a>\n\n<b>⚡ Powered By:</b> <i>Cilik smallbot</i>".format(
            "video",
            title,
            duration,
            views,
            channel,
            url,
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_path):
        if files and await aexists(files):
            await aremove(files)


@CILIK.UBOT("song|lagu", SUDO=True)
async def yt_audio(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Berikan judul!</b>",
        )
    try:
        search = (
            SearchVideos(
                str(message.text.split(None, 1)[1]),
                offset=1,
                mode="dict",
                max_results=1,
            )
            .result()
            .get("search_result")
        )
        link = f"https://youtu.be/{search[0]['id']}"
    except Exception as error:
        return await message.reply(f"<b>Error:</b> {error}")
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    infomsg = await message.reply(f"<code>Downloading songs...</code>")
    try:
        ytdl_data = await run_sync(ydl.extract_info, link, download=True)
        file_path = ydl.prepare_filename(ytdl_data)
        videoid = ytdl_data["id"]
        title = ytdl_data["title"]
        url = f"https://youtu.be/{videoid}"
        duration = ytdl_data["duration"]
        channel = ytdl_data["uploader"]
        views = f"{ytdl_data['view_count']:,}".replace(",", ".")
        thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    except Exception as error:
        return await infomsg.edit(f"<b>Error:</b> {error}")
    thumbnail = wget.download(thumbs)
    await client.send_audio(
        message.chat.id,
        audio=file_path,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        caption="<b>💡 Informasi {}</b>\n\n<b>🏷 Nama:</b> {}\n<b>🧭 Durasi:</b> {}\n<b>👀 Dilihat:</b> {}\n<b>📢 Channel:</b> {}\n<b>🔗 Tautan:</b> <a href={}>Youtube</a>\n\n<b>⚡ Powered By:</b> <i>Cilik smallbot</i>".format(
            "Audio",
            title,
            duration,
            views,
            channel,
            url,
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_path):
        if files and await aexists(files):
            await aremove(files)


@CILIK.UBOT("play", SUDO=True)
@checkplan
async def yt_audio(client, message):
    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio_telegram:
        infomsg = await message.reply(f"<code>Downloading songs...</code>")
        file_path = await message.reply_to_message.download()
        try:
            await client.call_py.leave_group_call(message.chat.id)
        except Exception:
            await client.call_py.join_group_call(
                message.chat.id, AudioPiped(file_path, HighQualityAudio())
            )
            await infomsg.edit(f"Done! Playing Songs")
            await aremove(file_path)
            return
        await client.call_py.join_group_call(
            message.chat.id, AudioPiped(file_path, HighQualityAudio())
        )
        await infomsg.edit(f"Done! Playing Songs")

        await aremove(file_path)

    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Berikan judul/link youtube/reply!**",
            )
        try:
            search = (
                SearchVideos(
                    str(message.text.split(None, 1)[1]),
                    offset=1,
                    mode="dict",
                    max_results=1,
                )
                .result()
                .get("search_result")
            )
            link = f"https://youtu.be/{search[0]['id']}"
        except Exception as error:
            return await message.reply(f"<b>Error:</b> {error}")
        ydl = YoutubeDL(
            {
                "quiet": True,
                "no_warnings": True,
                "format": "bestaudio[ext=m4a]",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "nocheckcertificate": True,
                "geo_bypass": True,
            }
        )
        infomsg = await message.reply(f"<code>Playing songs...</code>")
        try:
            ytdl_data = await run_sync(ydl.extract_info, link, download=True)
            file_path = ydl.prepare_filename(ytdl_data)
            videoid = ytdl_data["id"]
            ytdl_data["title"]
            url = f"https://youtu.be/{videoid}"
            ytdl_data["duration"]
            ytdl_data["uploader"]
            views = f"{ytdl_data['view_count']:,}".replace(",", ".")
            thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
        except Exception as error:
            return await infomsg.edit(f"<b>Error:</b> {error}")
        thumbnail = wget.download(thumbs)
        try:
            await client.call_py.leave_group_call(message.chat.id)
        except Exception:
            await client.call_py.join_group_call(
                message.chat.id, AudioPiped(file_path, HighQualityAudio())
            )
            await infomsg.edit(f"Done! Playing: `{message.text.split(None, 1)[1]}`")
            await aremove(file_path)
            return
        await client.call_py.join_group_call(
            message.chat.id, AudioPiped(file_path, HighQualityAudio())
        )
        await infomsg.edit(f"Done! Playing: `{message.text.split(None, 1)[1]}`")
        for files in (thumbnail, file_path):
            if files and await aexists(files):
                await aremove(files)
