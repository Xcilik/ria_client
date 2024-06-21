import asyncio
import os
import subprocess
import sys
from datetime import datetime, timedelta

from pytz import timezone

from cilik import ubot
from cilik.core.database import *
from config import *


async def clear_welcome():
    for X in ubot._ubot:
        anu = await get_wlcm(X.me.id)
        if anu:
            await clear_wlcm(X.me.id)


# expired userbot
async def expired_userbot():
    time = datetime.now(timezone("Asia/Jakarta"))
    for X in ubot._ubot:
        try:
            exp = await get_date_end(X.me.id)
            anu = time.strftime("%d-%m-%Y")
            itu = exp.strftime("%d-%m-%Y")
            if anu == itu:
                await add_mati(X.me.id)
                await remove_ubot(X.me.id)
                await remove_date_end(X.me.id)
                await remove_jumlah_client(X.me.id)
                await X.log_out()
        except Exception:
            continue


# 1harisebelumexpired


async def ingat_expired():
    time_now = datetime.now(timezone("Asia/Jakarta"))
    memek = timedelta(days=1)
    for X in ubot._ubot:
        try:
            exp = await get_date_end(X.me.id)
            itu = (time_now + memek).strftime("%d-%m-%Y")  # Tambah 1 hari ke depan

            if itu == exp.strftime("%d-%m-%Y"):  # Bandingkan dengan kedaluwarsa
                await add_habis(X.me.id)

        except Exception:
            continue


# cek update


async def Updated():
    anu = await get_update(6746108876)
    if anu == "on":
        await add_update(6746108876, "off")
        print(f"server{SERVER_NUMBER} Updated...")
        subprocess.check_output(["git", "pull"]).decode("UTF-8")
        os.execl(sys.executable, sys.executable, "-m", "cilik")


async def CekUpdated():
    while not await asyncio.sleep(120):
        await Updated()
