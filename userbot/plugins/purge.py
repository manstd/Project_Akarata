# Userbot module for purging unneeded messages(usually spam or ot).

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from ..utils import admin_cmd, edit_or_reply, errors_handler, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP


@bot.on(admin_cmd(outgoing=True, pattern="purge$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purge$"))
@errors_handler
async def fastpurger(purg):
    # For .purge command, purge all messages starting from the reply.
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count += 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await edit_or_reply(
            purg,
            "`No message specified.`",
        )
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        "Pembersihan cepat selesai!\nDibersihkan " + str(count) + " pesan.",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "#PURGE \nPembersihan " + str(count) + " pesan berhasil.",
        )
    await sleep(2)
    await done.delete()


@bot.on(admin_cmd(outgoing=True, pattern="purgeme"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purgeme"))
@errors_handler
async def purgeme(delme):
    # For .purgeme, delete x count of your latest message.
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Purge complete!` Purged " + str(count) + " messages.",
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "#PURGEME \nPurge of " + str(count) + " messages done successfully.",
        )
    await sleep(2)
    i = 1
    await smsg.delete()


@bot.on(admin_cmd(outgoing=True, pattern="del$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="del$"))
@errors_handler
async def delete_it(delme):
    """ For .del command, delete the replied message. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "#DEL \nMenghapus pesan berhasil"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Aku tidak bisa menghapus pesan"
                )


CMD_HELP.update(
    {
        "purge": "__**Nama Plugin :** Purge__\
    \n\n✅** CMD ➥** `.p`\
    \n**Fungsi   ➥  **Untuk membersihkan pesan, balas untuk menggunakannya.\
    \n\n✅** CMD ➥** `.purgeme` <x>\
    \n**Fungsi   ➥  **Hapus x total pesan baru.\
    \n\n✅** CMD ➥** `.d`\
    \n**Fungsi   ➥  **Hapus pesan yang kamu balas.\
    \n\n✅** CMD ➥** `.edit` <pesanbaru>\
    \n**Fungsi   ➥  **Timpa pesan, balas pesan untuk mengedit <pesanbaru>."
    }
)
