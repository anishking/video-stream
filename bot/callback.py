from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from config import ASSISTANT_NAME as bn


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
  await query.edit_message_text(
    f"""ā HOW TO USE THIS BOT:

1.) first, add me to your group.
2.) then promote me as admin and give all permissions except anonymous admin.
3.) add @{bn} to your group.
4.) turn on the voice chat first before start to stream video.
5.) type /vstream (reply to video) to start streaming.
6.) type /vstop to end the video streaming.

š **note: stream & stop command can only be executed by group admin only!**

ā” __Maintained by Veez Project Team__""",
    reply_markup=InlineKeyboardMarkup(
      [[
        InlineKeyboardButton(
          "š” Go Back", callback_data="cbstart")
      ]]
    ))


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
  await query.edit_message_text(f"āØ **Hello there, I am a telegram video streaming bot.**\n\nš­ **I was created to stream videos in group video chats easily.**\n\nā **To find out how to use me, please press the help button below** šš»",
                                reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "ā HOW TO USE THIS BOT", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "š Terms & Condition", callback_data="cbinfo")
                       ],[
                          InlineKeyboardButton(
                             "š¬ Group", url="https://t.me/VeezSupportGroup"),
                          InlineKeyboardButton(
                             "š£ Channel", url="https://t.me/levinachannel")
                       ],[
                          InlineKeyboardButton(
                             "š©š»āš» Developer", url="https://t.me/dlwrml")
                       ],[
                          InlineKeyboardButton(
                             "š All Command List", callback_data="cblist")
                       ]]
                    ))


@Client.on_callback_query(filters.regex("cbinfo"))
async def cbinfo(_, query: CallbackQuery):
  await query.edit_message_text(
    f"""š **bot information !**

š¤ __This bot was created to stream video in telegram group video chats using several methods from WebRTC.__

š” __Powered by PyTgcalls the Async client API for the Telegram Group Calls, and Pyrogram the telegram MTProto API Client Library and Framework in Pure Python for Users and Bots.__

šØš»āš» __Thanks to the developers who participated in the development of this bot, the list of devs can be seen below:__

š©š»āāļø Ā» [Levina](https://github.com/levina-lab)
š¤µš» Ā» [Sammy-XD](https://github.com/Sammy-XD)
š©š»āāļø Ā» [Achu](https://github.com/Achu2234)

__This bot licensed under GNU-GPL 3.0 License__""",
    reply_markup=InlineKeyboardMarkup(
      [[
        InlineKeyboardButton(
          "š” Go Back", callback_data="cbstart")
      ]]
    ),
    disable_web_page_preview=True
  )

@Client.on_callback_query(filters.regex("cblist"))
async def cblist(_, query: CallbackQuery):
  await query.edit_message_text(
    f"""š All Command List:

Ā» /vstream (reply to video or file) - to stream video
Ā» /vstop - end the video streaming
Ā» /song (song name) - download song from YT
Ā» /vsong (video name) - download video from YT
Ā» /lyric (song name) - lyric scrapper

š FUN CMD:

Ā» /asupan - check it by yourself
Ā» /chika - check it by yourself
Ā» /wibu - check it by yourself
Ā» /truth - check it by yourself
Ā» /dare - check it by yourself

š° EXTRA CMD:

Ā» /alive - check bot alive status
Ā» /ping - check bot ping status
Ā» /uptime - check bot uptime status
Ā» /sysinfo - check bot system information

ā” __Maintained by Veez Project Team__""",
    reply_markup=InlineKeyboardMarkup(
      [[
        InlineKeyboardButton(
          "š” Go Back", callback_data="cbstart")
      ]]
    ))


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    await query.message.delete()
