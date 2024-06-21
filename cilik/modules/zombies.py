from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK, FILTERS

__MODULE__ = "Zombies"
__HELP__ = f"""
<b>Cleaning Deleted Account:</b>
<i>Fitur ini berfungsi untuk menggeluarkan / membersihkan semua akun terhapus di dalam group.</i>

<b>ᴄᴍᴅ:</b>
├⋟<code>.cleanzombie</code> 
└⋟ Untuk mengeluarkan akun terhapus di grup.
"""


@CILIK.UBOT("cleanzombie|kickdel", FILTERS.ME_GROUP, SUDO=True)
async def _(client, message):
    await add_top_cmd(message.command[0])
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await message.reply("`Finding zombie...`")

    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(f"<b>Banned {banned_users} Deleted Accounts!</b>")
    else:
        await m.edit("There are no deleted accounts in this chat")
