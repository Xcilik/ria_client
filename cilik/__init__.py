import logging
import os
import re
import subprocess
import sys
from os import execl
from typing import Callable

from aiofiles.os import remove as aremove
from aiofiles.ospath import exists as aexists
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyromod import listen
from pytgcalls import PyTgCalls

from config import USERNAME_BOT
from user_data import *

aiohttpsession = ClientSession()

username_bot = USERNAME_BOT


# LOGS CODE
class ConnectionHandler(logging.Handler):
    def emit(self, record):
        for X in ["AUTH_KEY_UNREGISTERED", "OSError", "socketpair"]:
            if X in record.getMessage():
                os.execl(sys.executable, sys.executable, "-m", "cilik")


logging.basicConfig(
    level=logging.INFO,
    format="[ %(levelname)s ] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler(), ConnectionHandler()],
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)

console = logging.getLogger(__name__)


# CLASS CLIENT
class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []
    _prefix = {}
    _get_my_peer = {}
    _get_my_id = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="SmallUbot")
        self.call_py = PyTgCalls(self)

    def on_message(self, filters=None, group=0):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def set_prefix(self, user_id, prefix):
        self._prefix[self.me.id] = prefix

    async def start(self):
        await super().start()
        await self.call_py.start()
        handler = await get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = [".", "-", "!", "^"]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        console.info(f"Starting Client {self.me.id}|{self.me.first_name}")


async def get_prefix(user_id):
    return ubot._prefix.get(user_id, ".")


def anjay(cmd):
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(_, client, message):
        if message.text:
            text = message.text.strip()
            username = client.me.username or ""
            prefixes = await get_prefix(client.me.id)

            if not text:
                return False

            for prefix in prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix) :]

                for command in cmd.split("|"):
                    if not re.match(
                        rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                        without_prefix,
                        flags=re.IGNORECASE if not False else 0,
                    ):
                        continue

                    without_command = re.sub(
                        rf"{command}(?:@?{username})?\s?",
                        "",
                        without_prefix,
                        count=1,
                        flags=re.IGNORECASE if not False else 0,
                    )
                    message.command = [command] + [
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]

                    return True

        return False

    return filters.create(func)


# client
ubot = Ubot(name="cilik", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

# database
from cilik.core.database import *
