from asyncio import sleep

from pyrogram.types import Message

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

__MODULE__ = "Animation"
__HELP__ = f"""
<b>Bot Animation:</b>
<i>Fitur ini merupakan fitur hiburan karena bot akan menampilkan animasi sesuai dengan perintah yang diberikan.</i> 

<b>ᴄᴍᴅ:</b>
├⋟<code>.love</code>
└⋟ Animasi Love.

<b>ᴄᴍᴅ:</b>
├⋟<code>.sayang</code> 
└⋟ Animasi sayang.

<b>ᴄᴍᴅ:</b>
├⋟<code>.dino</code> 
└⋟ Animasi dino.

<b>ᴄᴍᴅ:</b>
├⋟<code>.heli</code> 
└⋟ Animasi Helikopter.

<b>ᴄᴍᴅ:</b>
├⋟<code>.peler</code> 
└⋟ Animasi anu.
"""


@CILIK.UBOT("p|P", SUDO=True)
async def _(client, message: Message):
    await add_top_cmd(message.command[0])
    await message.edit("Assalamualaikum")


@CILIK.UBOT("l|L", SUDO=True)
async def _(client, message: Message):
    await add_top_cmd(message.command[0])
    await message.edit("Waalaikumsalam")


@CILIK.UBOT("hai|hay", SUDO=True)
async def _(client, message):
    xx = message
    await xx.edit(f"**Hai ,  Assalamualaikum**")
    await sleep(1)
    await xx.edit("Kalian Nungguin aku gak??")
    await sleep(1)
    await xx.edit("Ih ga mau🤢")
    await sleep(1)
    await xx.edit("gasukaa😫")
    await sleep(1)
    await xx.edit("GELAYY🤮")


@CILIK.UBOT("lipkol", SUDO=True)
async def _(client, message):
    xx = message
    await xx.edit("Eh...")
    await sleep(2)
    await xx.edit("Suara kamu ga jelas")
    await sleep(2)
    await xx.edit("Kayanya kalau call pribadi lebih jelas")
    await sleep(2)
    await xx.edit("Gamau nyoba?")


@CILIK.UBOT("hbd", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    msg = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        msg = message.reply_to_message.from_user.first_name

    elif not msg:
        return await message.reply(
            ".hbd [nama yang ultah] atau balas pesan ke yang ultah"
        )

    animation_interval = 3
    animation_ttl = range(0, 10)
    await message.edit(f"𝐻𝑎𝑝𝑝𝑦 𝐵𝑖𝑟𝑡𝒉𝑑𝑎𝑦 {msg} 🎉🎉")
    animation_chars = [
        "[𝐻𝑎𝑝𝑝𝑦](https://telegra.ph/file/2fbc53ea22ec4471929fa.jpg)",
        "[­🎉🎉🎉](https://telegra.ph/file/e4e5729634f5c8c0c9e06.jpg)",
        "[𝐵𝑖𝑟𝑡𝒉𝑑𝑎𝑦🎊🎂](https://telegra.ph/file/d60d1697b9ac267371fd6.jpg)",
        "[­𝑇𝑜 𝑌𝑜𝑢🎂](https://telegra.ph/file/0a5d688271f8259b43a9f.jpg)",
        "[𝐻𝑎𝑝𝑝𝑦 𝐵𝑖𝑟𝑡𝒉𝑑𝑎𝑦🎉🎉](https://telegra.ph/file/2fd7cf79f3478ee3c9a27.jpg)",
        "[🎂🎂](https://telegra.ph/file/0f39e15093b70d3502bda.jpg)",
        "[🎁🎈🎈🎉](https://telegra.ph/file/59d6d8e8b1b9d3b112fc3.jpg)",
        "[🎉🎉🎉](https://telegra.ph/file/8021015799addb650f107.jpg)",
        f"**Selamat Ulang Tahun {msg} ✨✨✨**",
    ]
    for i in animation_ttl:

        await sleep(animation_interval)
        await message.edit(animation_chars[i % 10])


@CILIK.UBOT("lope|love", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 10)
    await message.edit("❤️🧡💚💙💜")
    animation_chars = [
        "🧡💚💙💜❤️",
        "💚💙💜❤️🧡",
        "💙💜❤️🧡💚",
        "💜❤️🧡💚💙",
        "❤️🧡💚💙💜",
        "🧡💚💙💜❤️",
        "💚💙💜❤️🧡",
        "💙💜❤️🧡💚",
        "💜❤️🧡💚💙",
        "❤️🧡💚💙💜",
    ]
    for i in animation_ttl:

        await sleep(animation_interval)
        await message.edit(animation_chars[i % 14])


@CILIK.UBOT("ah", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 3
    animation_ttl = range(0, 103)
    await message.edit("ah ah ah")
    animation_chars = [
        "Cerita ❤️ Cinta ",
        "  😐             😕 \n/👕\\         <👗\\ \n 👖               /|",
        "  😉          😳 \n/👕\\       /👗\\ \n  👖            /|",
        "  😚            😒 \n/👕\\         <👗> \n  👖             /|",
        "  😍         ☺️ \n/👕\\      /👗\\ \n  👖          /|",
        "  😍          😍 \n/👕\\       /👗\\ \n  👖           /|",
        "  😘   😊 \n /👕\\/👗\\ \n   👖   /|",
        " 😳  😁 \n /|\\ /👙\\ \n /     / |",
        "😈    /😰\\ \n<|\\      👙 \n /🍆    / |",
        "😅 \n/(),✊😮 \n /\\         _/\\/|",
        "😎 \n/\\_,__😫 \n  //    //       \\",
        "😖 \n/\\_,💦_😋  \n  //         //        \\",
        "  😭      ☺️ \n  /|\\   /(👶)\\ \n  /!\\   / \\ ",
        "TAMAT 😅",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await message.edit(animation_chars[i % 103])


@CILIK.UBOT("cinta")
async def _(client, message: Message):
    if message.forward_from:
        return
    await message.edit("Mencari cinta...")
    animation_chars = [
        "Connecting Ke Server Cinta",
        "Mencari Target Cinta",
        "Mengirim Cintaku.. 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
        "Mengirim Cintaku.. 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
        "Mengirim Cintaku.. 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
        "Mengirim Cintaku.. 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
        "Mengirim Cintaku.. 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
        "Mengirim Cintaku.. 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ ",
        "Mengirim Cintaku.. 84%\n█████████████████████▒▒▒▒ ",
        "Mengirim Cintaku.. 100%\n█████████CINTAKU███████████ ",
        "Cintaku Sekarang Sepenuhnya Terkirim Padamu, Dan Sekarang Aku Sangat Mencintai Mu, I Love You 💞",
    ]
    animation_interval = 2
    animation_ttl = range(11)
    for i in animation_ttl:
        await sleep(animation_interval)
        await message.edit(animation_chars[i % 11])


@CILIK.UBOT("babi", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 12)
    await message.edit("🐽 Ngok ngok...")
    animation_chars = [
        "_  _  _  _  _  _🐖💨",
        "_  _  _  _  _🐖💨 _",
        "_  _  _  _🐖💨 _  _",
        "_  _  _🐖💨 _  _  _",
        "_  _🐖💨 _  _  _  _",
        "_🐖💨 _  _  _  _  _",
        "🐖💨",
        "🪨 _🐖💨",
        "🪨🐖💨",
        "🔥",
        "R.I.P",
    ]
    for i in animation_ttl:

        await sleep(animation_interval)
        await message.edit(animation_chars[i % 12])


@CILIK.UBOT("balap", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 25)
    await message.edit("~ Balapan ~")
    animation_chars = [
        "Brem brem brem . . .",
        "🛺",
        "_   _   _   _   _  🛺",
        "_   _   _   _   🛺  _",
        "_   _   _   🛺  _   _",
        "_   _   🛺  _   _   _",
        "_   🛺  _   _   _   _",
        "🛺  _   _   _   _   _",
        "🦍",
        "Wah ada mobil 🦍",
        "Wah ada mobil gua balap ahh 🦍",
        "🛺   _   _   _   _   🦍💨",
        "_   🛺   _   _   🦍💨💨 _",
        "_   _   🛺   🦍💨💨💨_  _",
        "_  _   _   🛺 🦍💨💨💨💨_   _   _",
        "🛺🦍💨💨 _   _   _   _",
        "🛺🦍",
        "💥",
        "_   _   _   _   🚑 🚑",
        "_   _   _  🚑 🚑 _   _",
        "_   _  🚑 🚑 _   _   _",
        "🚑 🚑 _   _   _   _  _",
        "🚑 🚑",
        "~ Tamat ~",
    ]
    for i in animation_ttl:

        await sleep(animation_interval)
        await message.edit(animation_chars[i % 25])


@CILIK.UBOT("dino", SUDO=True)
async def _(client, message: Message):
    typew = await message.edit("DIN DINNN.....")
    await sleep(0.5)
    await typew.edit("DINOOOOSAURUSSSSS!")
    await sleep(0.5)
    await typew.edit("<code>🏃                        🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                       🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                      🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                     🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃   LARII            🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                   🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                  🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                 🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃               🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃              🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃             🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃            🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃           🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃WOARGH!   🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃           🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃            🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃             🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃              🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃               🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                 🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                  🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                   🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                    🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                     🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃  Huh-Huh           🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                   🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                  🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                 🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃                🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃               🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃              🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃             🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃            🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃           🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃          🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃         🦖.</code>")
    await sleep(0.5)
    await typew.edit("DIA SEMAKIN MENDEKAT!!!")
    await sleep(0.5)
    await typew.edit("<code>🏃       🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃      🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃     🦖.</code>")
    await sleep(0.5)
    await typew.edit("<code>🏃    🦖.</code>")
    await sleep(0.5)
    await typew.edit("Dahlah Pasrah Aja")
    await sleep(0.5)
    await typew.edit("<code>🧎🦖</code>")
    await sleep(2)
    await typew.edit("-TAMAT-")
    await sleep(0.5)
    await typew.edit("Ending yang sangat <b>Membanggongkan</b>")


@CILIK.UBOT("ayam", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 25)
    await message.edit("~ Anak Ayam ~")
    animation_chars = [
        "Peok Peok . . .",
        "🐥",
        "_   _   _   _   _  🐥🐥🐥",
        "_   _   _   _   🐥🐣🐥  _",
        "_   _   _   🐣🐥🐥  _   _",
        "_   _   🐣🐥🐣  _   _   _",
        "_   🐥🐣🐥  _   _   _   _",
        "🐣🐥🐥  _   _   _   _   _",
        "🐅",
        "Wah ada anak ayam nih 🐅",
        "gua kejar ahh 🐅",
        "🐥🐥🐣   _   _   _   _   🐅💨",
        "_  🐥🐣🐥  _   _   🐅💨💨 _",
        "_  _  🐣🐥🐥   🐅💨💨💨_  _",
        "_  _  _  🐣🐥🐣 🐅💨💨💨💨_  _  _",
        "🐥🐣🐥🐅💨💨 _   _   _   _",
        "🐣🐥🐥🐅",
        "💥",
        "_   _   _   _   🚑 🚑",
        "_   _   _  🚑 🚑 _   _",
        "_   _  🚑 🚑 _   _   _",
        "🚑 🚑 _   _   _   _  _",
        "🚑 🚑",
        "~ Tamat ~",
        "<i>Ending yang sangat Mengwencanayo</i>",
    ]
    for i in animation_ttl:

        await sleep(animation_interval)
        await message.edit(animation_chars[i % 25])


@CILIK.UBOT("heli", SUDO=True)
async def _(client, message: Message):
    await message.edit(
        "▬▬▬.◙.▬▬▬ \n"
        "═▂▄▄▓▄▄▂ \n"
        "◢◤ █▀▀████▄▄▄▄◢◤ \n"
        "█▄ █ █▄ ███▀▀▀▀▀▀▀╬ \n"
        "◥█████◤ \n"
        "══╩══╩══ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ Hallo Semuanya :) \n"
        "╬═╬☻/ \n"
        "╬═╬/▌ \n"
        "╬═╬/ \\ \n",
    )


@CILIK.UBOT("sayang", SUDO=True)
async def _(client, message: Message):
    e = await message.edit("I LOVEE YOUUU 💕")
    await e.edit("💝💘💓💗")
    await sleep(0.5)
    await e.edit("💞💕💗💘")
    await sleep(0.5)
    await e.edit("💝💘💓💗")
    await sleep(0.5)
    await e.edit("💞💕💗💘")
    await sleep(0.5)
    await e.edit("💘💞💗💕")
    await sleep(0.5)
    await e.edit("💘💞💕💗")
    await sleep(0.5)
    await e.edit("SAYANG KAMU 💝💖💘")
    await sleep(0.5)
    await e.edit("💝💘💓💗")
    await sleep(0.5)
    await e.edit("💞💕💗💘")
    await sleep(0.5)
    await e.edit("💘💞💕💗")
    await sleep(0.5)
    await e.edit("SAYANG")
    await sleep(0.5)
    await e.edit("KAMU")
    await sleep(0.5)
    await e.edit("SELAMANYA 💕")
    await sleep(0.5)
    await e.edit("💘💘💘💘")
    await sleep(0.5)
    await e.edit("SAYANG")
    await sleep(0.5)
    await e.edit("KAMU")
    await sleep(0.5)
    await e.edit("SAYANG")
    await sleep(0.5)
    await e.edit("KAMU")
    await sleep(0.5)
    await e.edit("I LOVE YOUUUU")
    await sleep(0.5)
    await e.edit("MY BABY")
    await sleep(0.5)
    await e.edit("💕💞💘💝")
    await sleep(0.5)
    await e.edit("💘💕💞💝")
    await sleep(0.5)
    await e.edit("SAYANG KAMU💞")


@CILIK.UBOT("janda", SUDO=True)
async def _(client, message: Message):
    msg = await message.reply("<b>Mencari Janda untuk anda.</b>")
    await sleep(2)
    await msg.edit(
        "´´´´´████████´´\n"
        "´´`´███▒▒▒▒███´´´´´\n"
        "´´´███▒●▒▒●▒██´´´\n"
        "´´´███▒▒👄▒▒██´´\n"
        "´´██████▒▒███´´´´´\n"
        "´██████▒▒▒▒███´´\n"
        "██████▒▒▒▒▒▒███´´´´\n"
        "´´▓▓▓▓▓▓▓▓▓▓▓▓▓▒´´\n"
        "´´▒▒▒▒▓▓▓▓▓▓▓▓▓▒´´´´´\n"
        "´.▒▒▒´´▓▓▓▓▓▓▓▓▒´´´´´\n"
        "´.▒▒´´´´▓▓▓▓▓▓▓▒\n"
        "..▒▒.´´´´▓▓▓▓▓▓▓▒\n"
        "´▒▒▒▒▒▒▒▒▒▒▒▒\n"
        "´´´´´´´´´███████´´´´\n"
        "´´´´´´´´████████´´´´´´\n"
        "´´´´´´´█████████´´´´´\n"
        "´´´´´´██████████´´´\n"
        "´´´´´´██████████´´\n"
        "´´´´´´´█████████´\n"
        "´´´´´´´█████████´\n"
        "´´´´´´´´████████´´´\n"
        "         ▒▒▒▒▒\n"
        "         ▒▒▒▒\n"
        "         ▒▒▒▒\n"
        "        ▒▒ ▒▒\n"
        "       ▒▒  ▒▒\n"
        "      ▒▒   ▒▒\n"
        "    _▒▒    ▒▒\n"
        "    ▒▒     ▒▒\n"
        "    ▒▒     ▒▒\n"
        "  ███     ███\n"
        " ███      ███\n"
        "█ ████    █ ███\n"
    )


@CILIK.UBOT("small", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 0.6
    animation_ttl = range(0, 24)
    await message.edit("<b>S</b>")
    animation_chars = [
        "S",
        "SM",
        "SMA",
        "SMALL",
        "SMALL UBOT",
        "SMALL UBO🚅",
        "SMALL UB🚅🚃🚃",
        "SMALL U🚅🚃🚃🚃",
        "SMALL🚅🚃🚃🚃🚃",
        "SMAL🚅🚃🚃🚃🚃🚃",
        "SMA🚅🚃🚃🚃🚃🚃🚃",
        "SM🚅🚃🚃🚃🚃🚃🚃🚃",
        "S🚅🚃🚃🚃🚃🚃🚃🚃🚃",
        "🚅🚃🚃🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃",
        "🚃🚃🚃",
        "🚃🚃",
        "🚃",
        "🔥CILIK SMALLBOT🔥 is Alive",
    ]
    for i in animation_ttl:

        await sleep(animation_interval)
        await message.edit(animation_chars[i % 24])


@CILIK.UBOT("plane", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 0.5
    animation_ttl = range(0, 14)
    await message.edit("🛫 Wushhhhhh...")
    animation_chars = [
        "✈-------------",
        "-✈------------",
        "--✈-----------",
        "---✈----------",
        "----✈---------",
        "-----✈--------",
        "------✈-------",
        "-------✈------",
        "--------✈-----",
        "---------✈----",
        "----------✈---",
        "-----------✈--",
        "------------✈-",
        "-------------✈",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await message.edit(animation_chars[i % 14])


@CILIK.UBOT("ily", SUDO=True)
async def _(client, message: Message):
    await message.delete()
    await client.send_message(
        message.chat.id,
        "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️\n"
        "❤️╔╦╦╦╦╦╦╦╦╦╦╦╦╗❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬██████╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬██╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬██╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬██╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬██╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬██████╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬████╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬██╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬██╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬██╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬██╬╬█╬╬╬╣❤️\n"
        "❤️╠╬╬╬██████╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬████╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬█╬╬╬╬█╬╬╬╣❤️\n"
        "❤️╠╬╬██╬╬╬╬██╬╬╣❤️\n"
        "❤️╠╬╬██╬╬╬╬██╬╬╣❤️\n"
        "❤️╠╬╬╬█╬╬╬╬█╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬████╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬███╬╬╬╬███╬╣❤️\n"
        "❤️╠╬╬██╬╬╬╬██╬╬╣❤️\n"
        "❤️╠╬╬╬█╬╬╬╬█╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬█╬╬█╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬██╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬████████╬╬╣❤️\n"
        "❤️╠╬╬╬██╬╬╬╬█╬╬╣❤️\n"
        "❤️╠╬╬╬██╬█╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬█████╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬██╬█╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬██╬╬╬╬█╬╬╣❤️\n"
        "❤️╠╬╬████████╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╠█╬╬█╬╬█╬╬█╬█╣❤️\n"
        "❤️╠█╬╬█╬█╬█╬█╬█╣❤️\n"
        "❤️╠████╬█╬█╬█╬█╣❤️\n"
        "❤️╠╬╬╬█╬█╬█╬█╬█╣❤️\n"
        "❤️╠█╬╬█╬█╬█╬█╬█╣❤️\n"
        "❤️╠████╬╬█╬╬███╣❤️\n"
        "❤️╠╬╬╬╬╬╬╬╬╬╬╬╬╣❤️\n"
        "❤️╚╩╩╩╩╩╩╩╩╩╩╩╩╝❤️\n"
        "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️\n",
    )


@CILIK.UBOT("peler", SUDO=True)
async def _(client, message: Message):
    await message.edit("MAU LIAT PELER GAK???")
    await sleep(1)
    await message.edit("NIH DIAA....")
    await sleep(1)
    await message.edit(
        "░░░░▓█───────▄▄▀▀█──────\n"
        "░░░░▒░█────▄█▒░░▄░█─────\n"
        "░░░░░░░▀▄─▄▀▒▀▀▀▄▄▀──SIJONI─\n"
        "░░░░░░░░░█▒░░░░▄▀────PANJANG\n"
        "▒▒▒░░░░▄▀▒░░░░▄▀───DAN─\n"
        "▓▓▓▓▒░█▒░░░░░█▄───PEMBERANI─\n"
        "█████▀▒░░░░░█░▀▄───CROTT──\n"
        "█████▒▒░░░▒█░░░▀▄─AHHH──\n"
        "███▓▓▒▒▒▀▀▀█▄░░░░█──────\n"
        "▓██▓▒▒▒▒▒▒▒▒▒█░░░░█─────\n"
        "▓▓█▓▒▒▒▒▒▒▓▒▒█░░░░░█────\n"
        "░▒▒▀▀▄▄▄▄█▄▄▀░░░░░░░█─\n"
    )


@CILIK.UBOT("monyet", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 47)
    await message.edit("~ Adegan di Hutan ~")
    animation_chars = [
        "Hutan yang tenang...",
        "🌳🌳🌳🌳🌳",
        "Suatu monyet muncul...",
        "🐒",
        "Monyet itu melihat pisang...",
        "🍌",
        "Dia mengintip ke kiri dan kanan...",
        "👀👀",
        "Tidak ada siapapun...",
        "Dia mengambil pisang itu...",
        "🐒🍌",
        "Teriakan kecil",
        "🐒🍌🤫",
        "Dan mulai lari...",
        "_   _   _   _   _  🐒",
        "_   _   _   _   🐒  _",
        "_   _   _   🐒  _   _",
        "_   _   🐒  _   _   _",
        "_   🐒  _   _   _   _",
        "🐒  _   _   _   _   _",
        "_   _   _   _   _   _  🏃‍♂️",
        "_   _   _   _   _  🏃‍♂️ _",
        "_   _   _   _  🏃‍♂️ _   _",
        "_   _   _  🏃‍♂️ _   _   _",
        "_   _  🏃‍♂️ _   _   _   _",
        "_  🏃‍♂️ _   _   _   _   _",
        "🌳  _   _   _   _   _",
        "🌳🌳  _   _   _   _",
        "🌳🌳🌳  _   _   _",
        "🌳🌳🌳🌳  _   _",
        "🌳🌳🌳🌳🌳 _",
        "🌳🌳🌳🌳🌳🌳",
        "Tiba-tiba, dia bertemu seekor gorila...",
        "🦍",
        "Gorila itu marah...",
        "🦍😡",
        "Monyet itu ketakutan...",
        "🐒😱",
        "Tetapi dia tetap berlari...",
        "🏃‍♂️",
        "Gorila mulai mengejar...",
        "🦍🏃‍♂️",
        "Monyet mencoba menghindar...",
        "🐒🔄",
        "Akhirnya, mereka bertabrakan...",
        "💥🦍🐒",
        "~ Tamat ~",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await message.edit(animation_chars[i % 47])


@CILIK.UBOT("buaya", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 27)
    await message.edit("~ Adegan di Sungai ~")
    animation_chars = [
        "Sebuah sungai yang tenang...",
        "🌊🌊🌊🌊🌊",
        "Seorang kelinci muncul...",
        "🐇",
        "Kelinci ingin menyeberang sungai...",
        "🐇➡️🌉",
        "Dia berjalan di atas jembatan...",
        "🐇🚶‍♂️🌉",
        "Tiba-tiba, buaya muncul...",
        "🐊",
        "Buaya mulai mengejar kelinci...",
        "🐊🏃‍♂️",
        "Kelinci panik...",
        "🐇😱",
        "Dia berlari lebih cepat...",
        "🐇💨",
        "_   🐇💨💨 _",
        "_   _   🐇💨💨💨_  _",
        "_  _   _   🐇💨💨💨💨_   _   _",
        "Buaya semakin mendekat...",
        "🐊💨",
        "Kelinci hampir mencapai ujung jembatan...",
        "🐇🌉➡️",
        "Tetapi buaya berhasil menangkapnya...",
        "🐊🐇",
        "💀",
        "~ Tamat ~",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await message.edit(animation_chars[i % 27])


@CILIK.UBOT("jin", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 20)
    await message.edit("~ Adegan di Padang Pasir ~")
    animation_chars = [
        "Sebuah padang pasir yang luas...",
        "🏜️🏜️🏜️🏜️🏜️",
        "Seorang penjelajah muncul...",
        "🚶‍♂️",
        "Penjelajah mencari petunjuk...",
        "🔍",
        "Tiba-tiba, lampu ajaib muncul...",
        "💡",
        "Jin keluar dari lampu...",
        "💨",
        "🧞‍♂️",
        "Jin memberikan tiga permintaan...",
        "💫",
        "Penjelajah memberikan permintaannya...",
        "🙏",
        "Jin mengabulkan permintaan tersebut...",
        "✨",
        "Penjelajah memperoleh keinginannya...",
        "🌟",
        "~ Tamat ~",
        "Apa si anjerrr",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await message.edit(animation_chars[i % 20])


@CILIK.UBOT("gundu", SUDO=True)
async def _(client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1.5
    animation_ttl = range(0, 17)
    await message.edit("~ Adegan di Lingkungan Perumahan ~")
    animation_chars = [
        "Sebuah lingkungan perumahan yang ramai...",
        "🏠🏠🏠🏠🏠",
        "Seorang anak muncul dengan gundu...",
        "👦🪀",
        "Anak itu melemparkan gundu ke atas...",
        "🪀➡️🌌",
        "Gundu berputar-putar di udara...",
        "🌀🪀🌀",
        "Tiba-tiba, gundu melambung tinggi...",
        "🌠🪀",
        "Orang-orang berteriak kagum...",
        "👏🪀🎉",
        "Anak itu bangga dengan kemampuannya...",
        "😎🪀",
        "Tetapi, ada yang tidak senang...",
        "😠",
        "Seseorang berkata !",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await message.edit(animation_chars[i % 17])
    await sleep(2)
    await message.reply_sticker(
        "CAACAgUAAxkDAAEFlnNl9Ap2uoz9fdDem2AWQQURWV6WYAACJQsAAsgf6FWT_Q_e746oBh4E"
    )


@CILIK.UBOT("coli", SUDO=True)
async def _(client, message: Message):
    xx = message
    await xx.edit("`H`")
    await xx.edit("`Hm`")
    await xx.edit("`Hmm`")
    await xx.edit("`Hmmm`")
    await xx.edit("`Hmmmm`")
    await xx.edit("`Hmmmmm`")
    await sleep(2)
    await xx.edit("`Hujan Hujan Gini Ange😔`")
    await sleep(2)
    await xx.edit("`Enaknya Coli🤤`")
    await sleep(1)
    await xx.edit("`8✊===D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8===✊D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8✊===D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8===✊D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8✊===D`")
    await sleep(2)
    await xx.edit("`Ahhh🤤`")
    await sleep(1)
    await xx.edit("`8✊===D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8===✊D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8✊===D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8===✊D`")
    await xx.edit("`8==✊=D`")
    await xx.edit("`8=✊==D`")
    await xx.edit("`8✊===D`")
    await xx.edit("`crotss💦`")
    await xx.edit("`crotss💦💦`")
    await xx.edit("`crotss💦💦💦🤤`")
    await sleep(2)
    await xx.edit("`H`")
    await xx.edit("`Hm`")
    await xx.edit("`Hmm`")
    await xx.edit("`Hmmm😔`")
    await sleep(2)
    await xx.edit("`Ini Untuk Yang Terkahir`")
    await sleep(2)
    await xx.edit("`Kenapa Ya Gw Coli Tadi😔`")
    await sleep(2)
    await xx.edit("`Dah la besok besok ga mau lagi`")
