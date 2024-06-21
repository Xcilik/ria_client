import asyncio
import re
from datetime import datetime, timedelta

from pytimeparse import parse
from pytz import timezone

from cilik.core.handler import CILIK, checkplan


@CILIK.UBOT("remind|reminder")
@checkplan
async def reminders(client, message):
    if len(message.command) < 3:
        return await message.reply("Usage: `!remind` {waktu} {text}")

    now = datetime.now(timezone("Asia/Jakarta"))

    if message.reply_to_message:
        name = message.text.split(None, 1)[1].strip()
        data = name.split(" ", 1)
        if len(data) > 1:
            waktu = data[0]
            text = data[1].strip()
        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)
        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)

            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message(
                    message.chat.id,
                    text,
                    schedule_date=waktu_jadwal,
                    reply_to_message_id=message.reply_to_message.id,
                )
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(
                message.chat.id,
                text,
                schedule_date=waktu_jadwal,
                reply_to_message_id=message.reply_to_message.id,
            )
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(
                message.chat.id,
                text,
                schedule_date=waktu_jadwal,
                reply_to_message_id=message.reply_to_message.id,
            )

    else:
        name = message.text.split(None, 1)[1].strip()
        data = name.split(" ", 1)
        if len(data) > 1:
            waktu = data[0]
            text = data[1].strip()

        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)

        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)
            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message(
                    message.chat.id, text, schedule_date=waktu_jadwal
                )
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(message.chat.id, text, schedule_date=waktu_jadwal)
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(message.chat.id, text, schedule_date=waktu_jadwal)


@CILIK.UBOT("remindme|reminderme")
@checkplan
async def remindersme(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `!remindme` {waktu} {text/reply}")

    now = datetime.now(timezone("Asia/Jakarta"))

    if message.reply_to_message:
        waktu = message.text.split()[1]
        text = message.reply_to_message.text
        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)
        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)

            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message("me", text, schedule_date=waktu_jadwal)
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)

    else:
        if len(message.command) < 3:
            return await message.reply("Usage: `!remindme` {waktu} {text/reply}")
        name = message.text.split(None, 1)[1].strip()
        data = name.split(" ", 1)
        if len(data) > 1:
            waktu = data[0]
            text = data[1].strip()

        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)

        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)
            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message("me", text, schedule_date=waktu_jadwal)
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)


@CILIK.UBOT("sremind|sreminder")
@checkplan
async def sreminders(client, message):
    if len(message.command) < 3:
        return await message.reply("Usage: `!sremind` {waktu} {text}")

    now = datetime.now(timezone("Asia/Jakarta"))

    if message.reply_to_message:
        name = message.text.split(None, 1)[1].strip()
        data = name.split(" ", 1)
        if len(data) > 1:
            waktu = data[0]
            text = data[1].strip()
        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)
        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)

            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message(
                    message.chat.id,
                    text,
                    schedule_date=waktu_jadwal,
                    reply_to_message_id=message.reply_to_message.id,
                )
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            delet = await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(
                message.chat.id,
                text,
                schedule_date=waktu_jadwal,
                reply_to_message_id=message.reply_to_message.id,
            )
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(
                message.chat.id,
                text,
                schedule_date=waktu_jadwal,
                reply_to_message_id=message.reply_to_message.id,
            )
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()

    else:
        name = message.text.split(None, 1)[1].strip()
        data = name.split(" ", 1)
        if len(data) > 1:
            waktu = data[0]
            text = data[1].strip()

        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)

        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)
            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message(
                    message.chat.id, text, schedule_date=waktu_jadwal
                )
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            delet = await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(message.chat.id, text, schedule_date=waktu_jadwal)
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message(message.chat.id, text, schedule_date=waktu_jadwal)

            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()


@CILIK.UBOT("sremindme|sreminderme")
@checkplan
async def sremindersme(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `!sremindme` {waktu} {text/reply}")

    now = datetime.now(timezone("Asia/Jakarta"))

    if message.reply_to_message:
        waktu = message.text.split()[1]
        text = message.reply_to_message.text
        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)
        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)

            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message("me", text, schedule_date=waktu_jadwal)
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            delet = await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()

    else:
        if len(message.command) < 3:
            return await message.reply("Usage: `!sremindme` {waktu} {text/reply}")
        name = message.text.split(None, 1)[1].strip()
        data = name.split(" ", 1)
        if len(data) > 1:
            waktu = data[0]
            text = data[1].strip()

        angka_belakang_x = re.search(r"x(\d+)", waktu, re.IGNORECASE)

        if angka_belakang_x:
            angka_belakang_x = int(angka_belakang_x.group(1))
            pars = re.sub(r"x\d+", "", waktu, flags=re.IGNORECASE)
            waktuon = parse(pars)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__.\nBerulang {angka_belakang_x} waktu"
            )
            for _ in range(angka_belakang_x):
                waktu_jadwal += timedelta(seconds=waktuon)
                await client.send_message("me", text, schedule_date=waktu_jadwal)
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        elif ":" in waktu:
            jam, menit = map(int, waktu.split(":"))
            waktu_jadwal = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            delet = await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)
            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
        else:
            waktuon = parse(waktu)
            if waktuon == None:
                return await message.reply("Format waktu salah!")

            waktu_jadwal = now + timedelta(seconds=waktuon)
            delet = await message.reply(
                f"🕒 Pengingat untuk diriku telah ditetapkan pada __{waktu_jadwal.strftime('%Y-%m-%d %H:%M:%S %Z')}__."
            )
            await client.send_message("me", text, schedule_date=waktu_jadwal)

            await asyncio.sleep(2)
            await message.delete()
            await delet.delete()
