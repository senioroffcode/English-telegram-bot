import sqlite3
from aiogram import types
from data.config import Kanal, ADMINS
from keyboards.inline.obunabol import check_button
from loader import dp, bot, db
from utils.misc import subscribe


@dp.message_handler(commands="start", state="*")
async def show_channel(message: types.Message):
    idsi = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username
    try:
        db.add_user(id=idsi, name=name, username=username)
        await message.answer(f"🎬Assalomu alaykum  {message.from_user.full_name}  botimizga xush kelibsiz.\n\n✍🏻 Kino kodini yuboring")
    except sqlite3.IntegrityError as err:
        await message.answer(f"🎬Assalomu alaykum  {message.from_user.full_name}  botimizga xush kelibsiz.\n\n✍🏻 Kino kodini yuboring")


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = "<b>👮🏻‍♂️ Obuna bo'lmagan kanallar:</b>\n\n"
    all_subscribed = True

    for channel in Kanal:
        status = await subscribe.check(user_id=call.from_user.id, channel=channel)
        if not status:
            result += f"<b>➡️ {channel}</b>\n"
            all_subscribed = False

    if all_subscribed:
        # Obuna bo'lganidan so'ng
        await call.message.delete()
        await call.message.answer(f"🎬Assalomu alaykum {message.from_user.full_name}  botimizga xush kelibsiz.\n\n✍🏻 Kino kodini yuboring")
    else:
        # Agar kanallarga obuna bo'lmasa
        await call.message.delete()
        result += "\nObuna bo'lib <b>'Obuna Bo'ldim ✅'</b> tugmasini bosing:"
        await call.message.answer(result, reply_markup=check_button, disable_web_page_preview=True)
