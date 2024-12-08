import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from YukkiMusic import app
from YukkiMusic.utils.database import get_served_chats
from config import OWNER_ID, LOG_GROUP_ID
from pyrogram.enums import ChatMemberStatus
from datetime import datetime, timedelta
from YukkiMusic.utils.decorators import AdminActual
from YukkiMusic.utils.databassse import is_welcome_enabled, enable_welcome, disable_welcome
from pyrogram.enums import ChatMembersFilter

urlm = "https://telegra.ph/file/a78511ddc8f5984416836.jpg"
photo_urls = [
    "https://envs.sh/Wi_.jpg",
    "https://envs.sh/Wi_.jpg",
]

@app.on_message(filters.new_chat_members, group=-2)
async def welcome_new_member(client: Client, message: Message):
    chat = message.chat
    dev_id = OWNER_ID
    bot_id = (await client.get_me()).id

    for new_member in message.new_chat_members:
        # ترحيب بمطور البوت
        if new_member.id == dev_id:
            info = await app.get_chat(dev_id)
            name = info.first_name
            markup = InlineKeyboardMarkup([[InlineKeyboardButton(name, user_id=dev_id)]])
            
            photos = [photo async for photo in client.get_chat_photos(dev_id, limit=1)]
            
            if not photos:
                await message.reply_text(
                    f"↢ مرحباً مطوري <a href='tg://user?id={dev_id}'>{name}</a> نورت الشات ياعزيزي🧸",
                    reply_markup=markup
                )
            else:
                await message.reply_photo(
                    photos[0].file_id,
                    caption=f"↢ مرحباً مطوري <a href='tg://user?id={dev_id}'>{name}</a> نورت الشات ياعزيزي🧸",
                    reply_markup=markup
                )
        
        # التعامل مع إضافة البوت إلى مجموعة جديدة
@app.on_message(filters.left_chat_member)
async def leftmem(client, message):
    logging.info("A member left the group")  # التحقق من تنفيذ الكود
    
    chat = await app.get_chat(message.chat.id)
    gti = chat.title
    link = await app.export_chat_invite_link(message.chat.id)

    user_id = message.left_chat_member.id

    chat_id = message.chat.id
    async for member in client.get_chat_members(chat_id):
        if member.status == ChatMemberStatus.OWNER:  # جلب منشئ المجموعة فقط
            owner_id = member.user.id
            owner_name = member.user.first_name

    buttons = [
        [
            InlineKeyboardButton(f"{owner_name}", url=f"tg://openmessage?user_id={owner_id}")
        ],[
            InlineKeyboardButton(gti, url=f"{link}")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await app.send_message(user_id, f"<b>- ليه تركت المجموعة ياحلو [ {message.left_chat_member.mention} ⁪⁬⁮⁮⁮⁮].\n\n</b>"
                                    f"<b>• اذا تبي ترجع للمجموعة {gti}\n</b>"
                                    f"<b>• رابط المجموعة في الاسفل\n</b>"
                                    f"<a href='{link}'>ㅤ</a>",
                                    reply_markup=reply_markup)
        
        # ترحيب بالأعضاء الجدد
        else:
            chat_id = message.chat.id  # الحصول على معرف الدردشة
            if not await is_welcome_enabled(chat_id):
                return
            async for member in client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
                if member.status == ChatMemberStatus.OWNER:
                    owner_id = member.user.id
                    owner_name = member.user.first_name
                    break
            
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(owner_name, url=f"tg://openmessage?user_id={owner_id}")]]
            )

            now = datetime.utcnow() + timedelta(hours=3)
            welcome_text = (
                f"<a href='{urlm}'>‌‌</a>"
                f"𝐰𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐠𝐫𝐨𝐮𝐩.🧸\n\n"
                f"{chat.title}\n\n"
                f"neme : {message.from_user.mention}\n"
                f"id : `{message.from_user.id}`\n"
                f"➥• Welcome  : {new_member.mention}\n"
                f"➥• User : @{new_member.username or 'No username'}\n"
                f"➥• time : {now.strftime('%I:%M %p')}\n"
                f"➥• date : {now.strftime('%Y/%m/%d')}"
            )

            await message.reply_text(welcome_text, reply_markup=keyboard)

# أمر للتعطيل
@app.on_message(filters.command(["تعطيل الترحيب الذكي"],"") & filters.group)
@AdminActual
async def disable_welcome_command(client, message: Message, _):
    chat_id = message.chat.id  # الحصول على معرف الدردشة
    if not await is_welcome_enabled(chat_id):
        await message.reply_text("<b>الترحيب الذكي معطل من قبل.</b>")
        return
    await disable_welcome(chat_id)
    await message.reply_text("<b>تم تعطيل الترحيب الذكي بنجاح.</b>")

#######&&&&&&#######

#امر للتفعيل
@app.on_message(filters.command(["تفعيل الترحيب الذكي"],"") & filters.group)
@AdminActual
async def enable_welcome_command(client, message: Message, _):
    chat_id = message.chat.id  # الحصول على معرف الدردشة
    if await is_welcome_enabled(chat_id):
        await message.reply_text("<b>الترحيب الذكي مفعل من قبل.</b>")
        return
    await enable_welcome(chat_id)
    await message.reply_text("<b>تم تفعيل الترحيب الذكي بنجاح.</b>")
