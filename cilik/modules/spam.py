import asyncio

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, checkplan

__MODULE__ = "Spam"
__HELP__ = f"""
<b>Spamming:</b>
<i>Fitur ini berfungsi untuk mengirim pesan secara berulang / spam.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.spam</code> [jumlah - text]
├⋟ Untuk spam pesan.
└⋟ <b>example:</b> <code>.spam 100 hay</code>

<b>ᴄᴍᴅ:</b>
├⋟<code>.spam</code> [reply_user - jumlah - text]
└⋟ Untuk spam pesan ke user yang di reply.

<b>ᴄᴍᴅ:</b>
├⋟<code>.ds</code> [jumlah] [waktu] [pesan]
├⋟ Untuk delay spam pesan.
└⋟ <b>example:</b> <code>.ds 100 10 hay</code>

<b>ᴄᴍᴅ:</b>
├⋟<code>.listspam</code> 
└⋟ Untuk melihat list delayspam

<b>ᴄᴍᴅ:</b>
├⋟<code>.stopspam</code> [id_spam]
└⋟ Untuk menghentikan delayspam
"""
SPAM_COUNT = [0]


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 50


@CILIK.UBOT("spam", SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    if message.reply_to_message:
        spam = await message.reply("`Spamming...`")
        reply_id = message.reply_to_message.id
        quantity = int(message.text.split(None, 2)[1])
        spam_text = message.text.split(None, 2)[2]
        await asyncio.sleep(1)
        await message.delete()
        await spam.delete()
        for i in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_id
            )
            await asyncio.sleep(0.1)
    else:
        if len(message.text.split()) < 2:
            await message.reply_text("Usage: `!spam` {jumlah spam} {text}")
        else:
            spam = await message.reply("Waiting. . .")
            quantity = int(message.text.split(None, 2)[1])
            spam_text = message.text.split(None, 2)[2]
            await asyncio.sleep(1)
            await message.delete()
            await spam.delete()
            for i in range(quantity):
                await client.send_message(message.chat.id, spam_text)
                await asyncio.sleep(0.1)


running_spams = {}


@CILIK.UBOT("ds|delayspam", SUDO=True)
@checkplan
async def delayspam(client, message):
    await add_top_cmd(message.command[0])
    chat = message.chat.id
    args = message.text.split()[1:]  # Extract arguments excluding the command
    if len(args) < 2:
        return await message.reply("Usage: `!ds` {jumlah} {waktu} {pesan/reply}")

    jumlah = int(args[0])
    waktu = float(args[1])

    # Cek apakah pesan yang diberikan adalah balasan atau bukan
    if message.reply_to_message and not args[2:]:
        pesan = message.reply_to_message.text or message.reply_to_message.caption
    else:
        pesan = " ".join(args[2:])

    if not pesan:
        return await message.reply("<b>Berikan Text/Reply!</b>")

    kk = await message.reply(
        f"Starting delayspam number of messages {jumlah} with time {waktu}"
    )

    async def send_messages():
        nonlocal jumlah, waktu, chat, pesan, kk
        for _ in range(jumlah):
            await client.send_message(chat, pesan)
            await asyncio.sleep(waktu)
            await kk.delete()

        del running_spams[kk.id]  # Hapus spam yang telah selesai

    task = asyncio.create_task(send_messages())
    running_spams[kk.id] = task  # Tambahkan ke daftar spam yang sedang berjalan


@CILIK.UBOT("listspam", SUDO=True)
@checkplan
async def list_spams(client, message):
    await add_top_cmd(message.command[0])
    running_spam_ids = list(running_spams.keys())
    if not running_spam_ids:
        return await message.reply("Tidak ada spam yang sedang berjalan.")

    response = "List Spam yang Sedang Berjalan:\n"
    for idx, spam_id in enumerate(running_spam_ids, start=1):
        response += f"{idx}. Spam ID: <code>{spam_id}</code>\n"

    await message.reply(response)


@CILIK.UBOT("stopspam", SUDO=True)
@checkplan
async def stop_spam(client, message):
    await add_top_cmd(message.command[0])
    args = message.text.split()[1:]  # Extract arguments excluding the command
    if not args:
        return await message.reply("Berikan ID spam yang ingin dihentikan.")

    spam_id_to_stop = int(args[0])

    if spam_id_to_stop not in running_spams:
        return await message.reply("ID spam tidak ditemukan atau sudah selesai.")

    running_spams[spam_id_to_stop].cancel()
    del running_spams[spam_id_to_stop]
    await message.reply(f"Spam dengan ID {spam_id_to_stop} telah dihentikan.")
