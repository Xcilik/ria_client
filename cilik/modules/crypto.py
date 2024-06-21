import asyncio

import requests
from pyrogram.raw.functions.messages import DeleteHistory

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK

__MODULE__ = "Crypto"
__HELP__ = f"""
<b>Crypto Currency:</b>
<i>Fitur ini berguna untuk melihat harga coin Crypto serta mengconvert dari mata uang yang satu ke mata uang Crypto lain nya.</i> 

<b>ᴄᴍᴅ:</b>
├⋟<code>.conv</code> [amount] [from] [to]
├⋟ <b>example:</b> <code>.conv</code> 2 btc eth.
└⋟ Untuk Menngconvert mata uang Crypto.

<b>ᴄᴍᴅ:</b>
├⋟<code>.price</code> [coin]
├⋟ <b>example:</b> <code>.price</code> btc.
└⋟ Untuk melihat harga coin crypto di market.

<b>ᴄᴍᴅ:</b>
├⋟<code>.calc</code> [coin] [value]
├⋟ <b>example:</b> <code>.calc</code> btc 100.
└⋟  Hitung jumlah koin.

List Crypto Currency
<a href=https://www.cryptocompare.com/coins/list/all/USD/1>HERE</a>
"""
CRYPTO_API_KEY = "f07c9026a8b17c9eea33f32d5dd832c067289ae228dd433e79dce3be0ac5a6f9"


async def convert_currency(amount, from_currency, to_currency):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={from_currency}&tsyms={to_currency}&api_key={CRYPTO_API_KEY}"
    response = await asyncio.run_sync(requests.get, url)
    data = response.json()
    converted_amount = data[to_currency] * amount
    return converted_amount


@CILIK.UBOT("conv|convert", SUDO=True)
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
        await message.reply("Usage: <code>!conv</code> {amount} {from} {to}")
    else:
        try:
            command, amount, from_currency, to_currency = message.text.split(" ")
            amount = float(amount)
        except ValueError:
            await message.reply_text("Usage: <code>!conv</code> {amount} {from} {to}")
            return

        # Lakukan konversi mata uang
        converted_amount = await convert_currency(
            amount, from_currency.upper(), to_currency.upper()
        )

        # Kirim hasil konversi ke pengguna
        result_text = f"{amount} {from_currency.upper()} = {converted_amount} {to_currency.upper()}"
        await message.reply_text(result_text)


@CILIK.UBOT("cek|fbi", SUDO=True)
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
        await message.reply("<b>Berikan user_id/username!</b>")
    else:
        bot = "MissRose_bot"
        await client.unblock_user(bot)
        await client.send_message(bot, f"/info {link}")
        await asyncio.sleep(1.5)
        async for sosmed in client.search_messages(bot, query="User"):
            try:
                await asyncio.gather(
                    *[sosmed.copy(message.chat.id, reply_to_message_id=message.id)]
                )
                user_info = await client.resolve_peer("@MissRose_bot")
                return await client.send(
                    DeleteHistory(peer=user_info, max_id=0, revoke=True)
                )
            except Exception:
                await message.reply("<b>Error.</b>")


@CILIK.UBOT("price", SUDO=True)
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
        await message.reply("Usage: <b>!price</b> {coin}")
    else:
        anu = await message.reply(f"`Get price {link.upper()}...`")
        bot = "tomketloversbot"
        await client.unblock_user(bot)
        mek = await client.send_message(bot, f"/p {link}")
        await asyncio.sleep(3)
        await mek.delete()
        async for sosmed in client.search_messages(bot):
            if "This" in sosmed.text:
                return await anu.edit("Coin not found!")
            else:
                try:
                    await asyncio.gather(
                        *[
                            sosmed.copy(
                                message.chat.id, reply_to_message_id=message.id
                            ),
                            anu.delete(),
                        ]
                    )
                    user_info = await client.resolve_peer("tomketloversbot")
                    return await client.send(
                        DeleteHistory(peer=user_info, max_id=0, revoke=True)
                    )
                except Exception:
                    await message.reply("<b>Error.</b>")


@CILIK.UBOT("calc", SUDO=True)
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
        await message.reply("Example: <code>!calc</code> btc 100")
    else:
        anu = await message.reply(f"`Calculating {link.upper()}...`")
        bot = "tomketloversbot"
        await client.unblock_user(bot)
        mek = await client.send_message(bot, f"/calc {link}")
        await asyncio.sleep(4)
        await mek.delete()
        async for sosmed in client.search_messages(bot):
            if "That" in sosmed.text:
                return await anu.edit(
                    "That coin could not be found. Here's an example\nEx: .calc btc 100!"
                )
            else:
                try:
                    await asyncio.gather(
                        *[
                            sosmed.copy(
                                message.chat.id, reply_to_message_id=message.id
                            ),
                            anu.delete(),
                        ]
                    )
                    user_info = await client.resolve_peer("tomketloversbot")
                    return await client.send(
                        DeleteHistory(peer=user_info, max_id=0, revoke=True)
                    )
                except Exception:
                    await message.reply("<b>Error.</b>")
