import os
from os import listdir, mkdir
from shutil import rmtree

from aiofiles.os import remove as aremove


async def dirr():
    for file in os.listdir():
        if file.endswith((".jpg", ".jpeg", ".mp4", ".mp3")):
            await aremove(file)
    if "downloads" in listdir():
        rmtree("downloads", ignore_errors=True)
    mkdir("downloads")
    if "cache" in listdir():
        rmtree("cache", ignore_errors=True)
    mkdir("cache")
