import asyncio
import json
from asyncio import sleep
from datetime import datetime

import requests
from pyrogram import raw
from pyrogram.enums import ChatMemberStatus, ChatType

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

__MODULE__ = "Misc"
__HELP__ = f"""
<b>Misc Feature:</b>
<i>Merupakan kumpulan fitur yang berguna untuk aktivitas kamu di <b>Telegram.</b>

<b>ᴄᴍᴅ:</b>
├⋟<code>.adzan</code> [nama kota]
└⋟ Untuk mengetahui jadwal adzan di lokasi anda.

<b>ᴄᴍᴅ:</b>
├⋟<code>.carbon</code> [text]
└⋟ Carbonised Text

<b>ᴄᴍᴅ:</b>
├⋟<code>.staff</code>
└⋟ Untuk mengetahui daftar admin didalam grup.

<b>ᴄᴍᴅ:</b>
├⋟<code>.msg</code> [reply to user - text]
└⋟ Untuk mengirim pesan secara rahasia.

<b>ᴄᴍᴅ:</b>
├⋟<code>.rmbg</code> [reply to photo]
└⋟ Untuk menghapus background dari foto.

<b>ᴄᴍᴅ:</b>
├⋟<code>.logo</code> [text]
└⋟ Membuat logo name.

<b>ᴄᴍᴅ:</b>
├⋟<code>.limit</code>
└⋟ Untuk cek limit akun anda.

<b>ᴄᴍᴅ:</b>
├⋟<code>.stats</code>
└⋟ Akun status (jumlah group/Channel yang kamu join) (jumlah users yang di akunmu)


<b>Afk:</b>
<i>Fitur ini berfungsi untuk mmemberi informasi kepada orang lain bahwa kamu sedang tidak aktif dengan alasan yang diberikan.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.afk</code> [alasan]
└⋟ Untuk mengaktifkan mode afk.

<b>Contoh:</b> .afk lagi makan siang
"""


@CILIK.UBOT("limit", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    await client.unblock_user("SpamBot")
    response = await client.send(
        raw.functions.messages.StartBot(
            bot=await client.resolve_peer("SpamBot"),
            peer=await client.resolve_peer("SpamBot"),
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    spambot_msg = response.updates[1].message.id + 1
    status = await client.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await message.reply(f"{status.text}")


@CILIK.UBOT("stats", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    yanto = await message.reply_text("📊 <code>Collecting...</code>")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh = await client.get_me()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == ChatType.BOT:
            b += 1
        elif dialog.chat.type == ChatType.GROUP:
            g += 1
        elif dialog.chat.type == ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in (
                ChatMemberStatus.OWNER,
                ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == ChatType.CHANNEL:
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await yanto.edit_text(
        """📊 <b>Stats Me</b>

<b>Private Chats :</b> <code>{}</code>
<b>Groups:</b> <code>{}</code>
<b>Super Groups:</b> <code>{}</code>
<b>Channels:</b> <code>{}</code>
<b>Admins:</b> <code>{}</code>
<b>Bots:</b> <code>{}</code>
<b>⏱ It Took:</b> <code>{}</code>""".format(
            u, g, sg, c, a_chat, b, ms
        )
    )


@CILIK.UBOT("adzan", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    LOKASI = message.text.split(None, 1)[1]
    if len(message.command) < 2:
        return await message.reply("<b>Berikan nama kota!</b>")
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = await asyncio.run_sync(requests.get, url)
    if request.status_code != 200:
        await message.reply(f"Maaf Tidak Menemukan Kota <code>{LOKASI}</code>")
    result = json.loads(request.text)
    catresult = f"""
Jadwal Shalat Hari Ini

<b>Tanggal</b> <code>{result['items'][0]['date_for']}</code>
<b>Kota</b> <code>{result['query']} | {result['country']}</code>

<b>Terbit:</b> <code>{result['items'][0]['shurooq']}</code>
<b>Subuh:</b> <code>{result['items'][0]['fajr']}</code>
<b>Zuhur:</b> <code>{result['items'][0]['dhuhr']}</code>
<b>Ashar:</b> <code>{result['items'][0]['asr']}</code>
<b>Maghrib:</b> <code>{result['items'][0]['maghrib']}</code>
<b>Isya:</b> <code>{result['items'][0]['isha']}</code>
"""
    await message.reply(catresult)
