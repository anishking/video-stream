import os
import time
import ffmpeg
import asyncio
from os import path
from asyncio import sleep
from youtube_dl import YoutubeDL
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME, BOT_USERNAME, CHAT_ID
from helpers.decorators import authorized_users_only
from helpers.filters import command


app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)

STREAM = {6}
VIDEO_CALL = {}

ydl_opts = {
        "format": "best",
        "addmetadata": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "videoformat": "mp4",
        "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)

@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def vstream(client, m: Message):
    if 1 in STREAM:
        await m.reply_text("😕 **sorry, there's another video streaming right now**\n\n» **wait for it to finish then try again!**")
        return
    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply("💭 **Give me a video or youtube url to stream**\n\n» Use the /vstream command by replying to the video or youtube url.")

    elif ' ' in m.text:
        msg = await m.reply_text("📥 **downloading video...**\n\n💭 __this process will take quite a while depending on the size of the video.__")
        text = m.text.split(' ', 1)
        url = text[1]
        if os.path.exists(f'stream-{CHAT_ID}.raw'):
            os.remove(f'stream-{CHAT_ID}.raw')
        try:
            info = ydl.extract_info(url, False)
            ydl.download([url])
            video = path.join("downloads", f"{info['id']}.{info['ext']}")
            await msg.edit("♻️ **converting video...**")
            os.system(f'ffmpeg -i "{video}" -vn -f s16le -ac 2 -ar 48000 -acodec pcm_s16le -filter:a "atempo=0.81" stream-{CHAT_ID}.raw -y')
        except Exception as e:
            await msg.edit(f"❌ **something went wrong...** \n\nError: `{e}`")
        await sleep(5)
        group_call = group_call_factory.get_file_group_call(f'stream-{CHAT_ID}.raw')
        try:
            await group_call.start(CHAT_ID)
            await group_call.set_video_capture(video)
            VIDEO_CALL[CHAT_ID] = group_call
            await msg.edit("💡 **video streaming started!**\n\n» **join to video chat to watch the video.**")
            try:
                STREAM.remove(0)
            except:
                pass
            try:
                STREAM.add(1)
            except:
                pass
        except FloodWait as e:
            await sleep(e.x)
            if not group_call.is_connected:
                await group_call.start(CHAT_ID)
                await group_call.set_video_capture(video)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit("💡 **video streaming started!**\n\n» **join to video chat to watch the video.**")
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
        except Exception as e:
            await msg.edit(f"❌ **something went wrong...** \n\nError: `{e}`")
            
    elif media.video or media.document:
        msg = await m.reply_text("📥 **downloading video...**\n\n💭 __this process will take quite a while depending on the size of the video.__")
        if os.path.exists(f'stream-{CHAT_ID}.raw'):
            os.remove(f'stream-{CHAT_ID}.raw')
        try:
            video = await client.download_media(media)
            await msg.edit("♻️ **converting video...**")
            os.system(f'ffmpeg -i "{video}" -vn -f s16le -ac 2 -ar 48000 -acodec pcm_s16le -filter:a "atempo=0.81" stream-{CHAT_ID}.raw -y')
        except Exception as e:
            await msg.edit(f"❌ **something went wrong...** \n`{e}`")
        await sleep(5)
        group_call = group_call_factory.get_file_group_call(f'stream-{CHAT_ID}.raw')
        try:
            await group_call.start(CHAT_ID)
            await group_call.set_video_capture(video)
            VIDEO_CALL[CHAT_ID] = group_call
            await msg.edit("💡 **video streaming started!**\n\n» **join to video chat to watch the video.**")
            try:
                STREAM.remove(0)
            except:
                pass
            try:
                STREAM.add(1)
            except:
                pass
        except FloodWait as e:
            await sleep(e.x)
            if not group_call.is_connected:
                await group_call.start(CHAT_ID)
                await group_call.set_video_capture(video)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit("💡 **video streaming started!**\n\n» **join to video chat to watch the video.**")
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
        except Exception as e:
            await msg.edit(f"❌ **something went wrong...** \nError: `{e}`")
    else:
        await m.reply_text("🔺 **please reply to a video or youtube link to stream video!**")
        return


@Client.on_message(command(["vstop", f"vstop@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def vstop(client, m: Message):
    if 0 in STREAM:
        await m.reply_text("😕 **no active streaming at this time**\n\n» start streaming by using /vstream command (reply to video)")
        return
    try:
        await VIDEO_CALL[CHAT_ID].stop()
        await m.reply_text("🔴 **streaming has ended !**\n\n✅ __userbot has been disconnected from the video chat__")
        try:
            STREAM.remove(1)
        except:
            pass
        try:
            STREAM.add(0)
        except:
            pass
    except Exception as e:
        await m.reply_text(f"❌ **something went wrong !** \nError: `{e}`")
