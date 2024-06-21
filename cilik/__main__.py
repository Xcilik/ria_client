import asyncio
import sys
from asyncio import get_event_loop_policy
from atexit import register
from datetime import datetime, timedelta
from os import execl

from pyrogram import idle
from pyrogram.errors import RPCError
from pytz import timezone

from cilik import *
from cilik.core.database import *
from cilik.core.functions import *
from user_data import USER_ID


# LOOPING AUTO RESTART
async def auto_restart():
    now = datetime.now(timezone("Asia/Jakarta"))
    target_time = now.replace(hour=5, minute=55, second=0, microsecond=0)
    if now >= target_time:
        target_time += timedelta(days=1)
    time_until_target = target_time - now
    await asyncio.sleep(time_until_target.total_seconds())

    await ingat_expired()
    await expired_userbot()
    await dirr()

    def go_restart():
        execl(sys.executable, sys.executable, "-m", "cilik")

    register(go_restart)
    sys.exit(0)


# LOOP STARTING CLIENT
async def start_ubot(user_id):
    try:
        await ubot.start()
    except RPCError:
        await remove_ubot(user_id)
        await remove_client(user_id)
        await add_revoke(user_id)
        await add_prem(user_id)
        console.warning(f"✅ {user_id} delete from database")
        return
    except Exception:
        pass

    await add_client(ubot.me.id)

    pref = await get_prefix_bot(ubot.me.id)
    if pref:
        await set_pref(ubot.me.id, pref)

    usernames = ["Cuapcuapin", "katalogbottelegram"]

    for username in usernames:
        try:
            await ubot.join_chat(username)
        except Exception:
            continue

    await asyncio.gather(loadPlugins(), idle())


# RUNNING ASYNCIO
if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(start_ubot(USER_ID))
    console.info("Client stoped")
