import re
from asyncio import sleep
from datetime import datetime

from pyrogram import enums, filters
from pytz import timezone

from cilik import ubot, username_bot
from cilik.core.database import *
from cilik.core.handler import CILIK, FILTERS
from cilik.utils.functions import get_arg

__MODULE__ = "Pmpermit"
__HELP__ = f"""
<b>Pesan balasan otomatis:</b>
<i>Fitur ini berfungsi untuk pesan balasan otomatis di setiap user yang melakukan chat pribadi, apabila user melakukan spam maka akan terblokir otomatis oleh bot, pesan balasan otomatis ini bisa di custom sesuai keinginan mu.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.pmpermit</code> [on / off]
└⋟ Untuk mematikan / menghidupkan fungsi PMPERMIT.

<b>ᴄᴍᴅ:</b>
├⋟<code>.setpmlimit</code> [1-10]
└⋟ Set limit teks PMPERMIT.

<b>ᴄᴍᴅ:</b>
├⋟<code>.setpmpermit</code> [Reply to message]
└⋟ Untuk mengcustom text PMPERMIT.

<b>ᴄᴍᴅ:</b>
├⋟<code>.getpmpermit</code>
└⋟ Untuk melihat text PMPERMIT.

<b>ᴄᴍᴅ:</b>
├⋟<code>.ok | .setuju | .allow</code>
└⋟ Untuk menerima pesan.

<b>ᴄᴍᴅ:</b>
├⋟<code>.no | .tolak | .deny</code>
└⋟ Untuk menolak pesan.

"""

ID_MAKER = [
    957122139,
    1784606556,
    6092681579,
    966484443,
    5794653305,
    1224143544,
    5747817390,
    2038932389,
    641527902,
    5218851742,
    5595647814,
    1305160817,
    5200055234,
    5609521329,
    5186620503,
    1991937261,
    5178772086,
    5595689691,
    1724750096,
    1897354060,
    5619544109,
    5868153157,
    2094897980,
    5073789750,
    1924496320,
]
PM_WARNS = {}
OLD_MSG = {}

PM_MSG = """
**PMSecurity of {}** ({})

Jangan spam nanti anda terblokir otomatis oleh bot

© __Powered by__ **[Ria Userbot](t.me/riaa_userbot)**
"""

# Cache variable
guard_status_cache = {}


async def get_guard_status_cache(user_id):
    if user_id in guard_status_cache:
        return guard_status_cache[user_id]
    else:
        guard_status = await get_guard(user_id)
        guard_status_cache[user_id] = guard_status
        return guard_status


@CILIK.UBOT("pmpermit", SUDO=True)
async def pmguard(client, message):
    await add_top_cmd(message.command[0])
    arg = get_arg(message)
    user_id = client.me.id
    if not arg:
        await message.reply("Usage: `!pmpermit` on/off")
        return
    await add_guard(user_id, arg)
    guard_status_cache[user_id] = arg  # Update the cache
    await message.reply(f"Sukses PmPermit <b>{arg.upper()}</b>", quote=True)


@CILIK.UBOT("setpmpermit", SUDO=True)
async def setpmmsg(client, message):
    await add_top_cmd(message.command[0])
    if len(message.command) < 1:
        return await message.reply("Usage: `!setpmpermit` {text/reply}")
    text = message.text.markdown if message.text else message.caption.markdown
    if message.reply_to_message:
        if message.reply_to_message.text:

            pmpermit_name = "pmpermit"
            pesan = re.sub(
                r"\[.*?\]\(buttonurl:.*?\)", "", message.reply_to_message.text.markdown
            )
            buttons = re.findall(
                r"\[.*?\]\(buttonurl:.*?\)", message.reply_to_message.text.markdown
            )

            if buttons:
                await save_pmpermit_button(client.me.id, pmpermit_name, buttons)
                await save_pmpermit(client.me.id, pmpermit_name, pesan)
            else:
                await save_pmpermit(client.me.id, pmpermit_name, pesan)
                cekbut = await get_pmpermit_button(client.me.id, pmpermit_name)
                if cekbut:
                    await rm_pmpermit_button(client.me.id, pmpermit_name)

            await message.reply("PmPermit Msg has been successfully set!", quote=True)
        else:
            pmpermit_name = "pmpermit"
            copy = await client.copy_message(
                "me", message.chat.id, message.reply_to_message.id
            )
            await save_pmpermit(client.me.id, pmpermit_name, copy.id)
            cekbut = await get_pmpermit_button(client.me.id, pmpermit_name)
            if cekbut:
                await rm_pmpermit_button(client.me.id, pmpermit_name)
            await message.reply("PmPermit Msg has been successfully set!", quote=True)
    else:
        data = text.split(None, 1)[1].strip()
        pmpermit_name = "pmpermit"

        pesan = re.sub(r"\[.*?\]\(buttonurl:.*?\)", "", data)
        buttons = re.findall(r"\[.*?\]\(buttonurl:.*?\)", data)

        if buttons:
            await save_pmpermit_button(client.me.id, pmpermit_name, buttons)
            await save_pmpermit(client.me.id, pmpermit_name, pesan)
        else:
            await save_pmpermit(client.me.id, pmpermit_name, pesan)
            cekbut = await get_pmpermit_button(client.me.id, pmpermit_name)
            if cekbut:
                await rm_pmpermit_button(client.me.id, pmpermit_name)

        await message.reply("PmPermit Msg has been successfully set!", quote=True)


@CILIK.UBOT("setpmlimit", SUDO=True)
async def pmguard(client, message):
    await add_top_cmd(message.command[0])
    arg = get_arg(message)
    user_id = client.me.id
    if not arg:
        await message.reply("Usage: `!setpmlimit` {1-10}")
        return
    await set_pm_limit(user_id, int(arg))
    await message.reply(f"Successfully changed the limit to {arg}", quote=True)


@CILIK.UBOT("getpmpermit", SUDO=True)
async def get_pmmessages(client, message):
    await add_top_cmd(message.command[0])
    anu = await get_pmpermit(client.me.id, "pmpermit")
    button = await get_pmpermit_button(client.me.id, "pmpermit")
    if anu is None:
        await message.reply(PM_MSG)
    else:
        if button:
            await message.reply(
                f"{anu}\n\n{button}", quote=True, parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply(anu, quote=True, parse_mode=enums.ParseMode.HTML)


@CILIK.UBOT("ok|setuju|approve|allow", FILTERS.ME_PRIVATE, SUDO=True)
async def allow(client, message):
    await add_top_cmd(message.command[0])
    if int(message.chat.id) in OLD_MSG:
        try:
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=OLD_MSG[int(message.chat.id)]
            )
        except BaseException:
            pass
    user_ = await client.get_users(int(message.chat.id))
    firstname = user_.first_name
    if not await is_user_approved(client.me.id, int(message.chat.id)):
        await approve_user(client.me.id, int(message.chat.id))
    else:
        await message.edit("The user is already on the whitelist!")
        await sleep(3)
        await message.delete()
        return
    await message.edit(
        "__Approved to pm [{}](tg://user?id={})__".format(
            firstname, int(message.chat.id)
        ),
    )
    await sleep(3)
    await message.delete()


@CILIK.UBOT("no|tolak|deny", FILTERS.ME_PRIVATE, SUDO=True)
async def deny(client, message):
    await add_top_cmd(message.command[0])
    user_ = await client.get_users(int(message.chat.id))
    firstname = user_.first_name
    if await is_user_approved(client.me.id, int(message.chat.id)):
        await disapprove_user(client.me.id, int(message.chat.id))
    else:
        await message.edit("The user has not been whitelisted!")
        await sleep(2)
        await message.delete()
        return
    await message.edit(
        "__Disaproved to pm [{}](tg://user?id={})__".format(
            firstname, int(message.chat.id)
        ),
    )
    await sleep(3)
    await message.delete()


@ubot.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69
)
async def reply_pm(client, message):
    guard_status = await get_guard_status_cache(client.me.id)
    if guard_status == "on":
        if not message.from_user:
            return
        if message.chat.id == 777000:
            return
        if await is_user_approved(client.me.id, int(message.chat.id)):
            return
        if message.from_user.id in ID_MAKER:
            await approve_user(client.me.id, int(message.chat.id))
            return
        pm_warns = await get_pm_limit(client.me.id)
        user_ = message.from_user
        if int(message.chat.id) not in PM_WARNS:
            PM_WARNS[int(message.chat.id)] = 0
        else:
            PM_WARNS[int(message.chat.id)] += 1

        if PM_WARNS[int(message.chat.id)] > (int(pm_warns) - 1):
            await message.reply(
                f"<code>There he is! I Give You {int(pm_warns)} Peringatan.\nYou are now Reported and Banned</code>\n<b>Reason:</b> <code>SPAM LIMIT REACHED !</code>"
            )
            await client.block_user(user_.id)
            if int(message.chat.id) in OLD_MSG:
                OLD_MSG.pop(int(message.chat.id))
            if int(message.chat.id) in PM_WARNS:
                PM_WARNS.pop(int(message.chat.id))
            blockeda = f"<b>#Blocked_PMPERMIT</b> \n<b>User :</b> <code>{user_.id}</code>\n<b>Reason :</b> <code>Spam Limit Reached.</code>"
            await client.send_message("me", blockeda)
            return

        if int(message.chat.id) in OLD_MSG:
            try:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=OLD_MSG[int(message.chat.id)]
                )
            except BaseException:
                pass
        warn = f"{int(PM_WARNS[int(message.chat.id)]) + 1}/{int(pm_warns)}"
        anu = await get_pmpermit(client.me.id, "pmpermit")
        if anu is None:
            iya = await client.send_message(
                message.chat.id,
                PM_MSG.format(client.me.mention, warn),
            )
            OLD_MSG[int(message.chat.id)] = iya.id

        else:
            buttons = await get_pmpermit_button(client.me.id, "pmpermit")
            if buttons:
                try:
                    x = await client.get_inline_bot_results(
                        username_bot,
                        f"pmpermit_button pmpermit {warn} {message.from_user.first_name} {message.from_user.username} {message.from_user.id} {message.from_user.mention}",
                    )
                    OLD_MSG[int(message.chat.id)] = message.id + 1
                    for m in x.results:
                        await client.send_inline_bot_result(
                            message.chat.id, x.query_id, m.id
                        )

                except Exception as error:
                    return await message.reply(str(error))
            else:
                iya = await message.reply(
                    text=anu.format(
                        me=client.me.mention,
                        warn=warn,
                        name=message.from_user.first_name,
                        username=(
                            f"@{message.from_user.username}"
                            if message.from_user.username
                            else None
                        ),
                        mention=message.from_user.mention,
                        id=message.from_user.id,
                        date=(datetime.now(timezone("Asia/Jakarta"))).strftime(
                            "%A, %d-%B-%Y"
                        ),
                        time=(datetime.now(timezone("Asia/Jakarta"))).strftime(
                            "%H:%M:%S %Z"
                        ),
                    ),
                )
                OLD_MSG[int(message.chat.id)] = iya.id
