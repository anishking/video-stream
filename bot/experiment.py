import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}


@Client.on_message(filters.command("stream"))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("๐บ **please reply to a video or live stream url to stream video!**")
        else:
            video = m.text.split(None, 1)[1]
            msg = await m.reply("__starting live stream...__")
            chat_id = m.chat.id
            await asyncio.sleep(1)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(chat_id)
                await group_call.start_video(video)
                VIDEO_CALL[chat_id] = group_call
                await msg.edit(f"๐ก **started live streaming !**")
            except Exception as e:
                await msg.edit(f"**Error** -- `{e}`")
    elif replied.video or replied.document:
        msg = await m.reply("๐ฅ **downloading video...**\n\n๐ญ __this process will take quite a while depending on the size of the video.__")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.id
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(chat_id)
            await group_call.start_video(video)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("๐ก **video streaming started!**\n\nยป **join to video chat to watch the video.**")
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("๐บ **please reply to a video or video file to stream video!**")

@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply("๐ด **streaming has ended !**\n\nโ __userbot has been disconnected from the video chat__")
    except Exception as e:
        await m.reply(f"**๐ซ Error** - `{e}`")
