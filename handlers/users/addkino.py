from aiogram.dispatcher.filters.state import StatesGroup, State
############### ADMIN PANEL ####################
import aiogram.utils.executor
from aiogram import types
from aiogram.types import Message, CallbackQuery, ContentTypes, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
import os
from data.config import ADMINS
from keyboards.inline.admin_keys import adminpanel, DeleteUsers, backDelete, BaseType, backall, allxabar, xtan
from loader import dp, bot, db
from states.states import sendAd, verifyDeleteUsers, send_user, answer, adpanel, bazayuk

answer_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👮‍♂️ Adminga javob berish", callback_data="answer_admin")
        ]
    ]
)

cancel_adminAnswer = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Bekor qilish", callback_data="cancel_adminAnswer")
        ],
    ],
)


def answer_user_key(id):
    key = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Javob yozish", callback_data=f'{id}')
            ]
        ]
    )
    return key


from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("admin"), user_id=ADMINS[0], state="*")
async def admin_command_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Assalomu alaykum {message.from_user.full_name} Admin Panelga xush kelibsiz",
                         reply_markup=adminpanel)
    await adpanel.yubor.set()


@dp.callback_query_handler(state=adpanel.yubor)
async def ste1(call: CallbackQuery, state: FSMContext):
    texts = call.data
    if texts == "reklama":
        await call.message.edit_text(
            "<b>📢 Reklama yuborish uchun (Rasm, video, havola, ulashish, text) yuboring!</b>\n\n❗️ Yuborilganidan "
            "so'ng uni tahrirlab yoki bekor qilib bo'lmaydi. Shuning uchun oldin reklama postini tayyorlab oling.",
            reply_markup=backall)
        await call.answer(cache_time=60)
        await sendAd.text.set()
    elif texts == "stats":
        count = db.count_users()[0]
        await call.answer(f"Bot foydalanuvchilari: {count} ta", show_alert=True)
        await call.answer(cache_time=60)
    elif texts == "delete_users":
        await call.message.edit_text("<b>✅ Tasdiqlash</b>\n\n"
                                     "Bot foydalanuvchilarini o'chirish uchun tasdiqlash kodini kiriting",
                                     reply_markup=backall)
        await verifyDeleteUsers.code.set()
    elif texts == "base":
        await call.message.edit_text("💾 Foydalanuvchi ma'lumotlar bazasini qay formatda yuklab olmoqchisiz👇🏻",
                                     reply_markup=BaseType)
        await bazayuk.byuk.set()
    elif texts == "send":
        await call.message.edit_text(
            "<b>👮🏻‍♂️ Xabarni foydalanuvchiga qay xolatda yubormoqchisiz?</b>\n\nQuyidagi tugmalardan birini tanlang👇🏻",
            reply_markup=allxabar)
        await send_user.tanla.set()
    elif texts == "addkino":
        await call.message.delete()
        await call.message.answer("<b>👮🏻‍♂️ Botga kino qo'shish uchun menga video havola ulashing:</b>")
        await AddKino.WaitingForVideo.set()
    elif texts == "delkino":
        await call.message.delete()
        await call.message.answer("🗑<b> Kinoni o'chirish uchun kino kodini yuboring:</b>")
        await DeleteKino.WaitingForKod.set()


@dp.message_handler(state=sendAd.text, content_types=ContentTypes.ANY)
async def rek_text(message: Message, state: FSMContext):
    await state.finish()
    import time
    users = db.select_all_users()
    x = 0
    y = 0
    i = await message.answer("✅ Reklama yuborilyapti, iltimos kutib turing...")

    start_time = time.time()  # Replace with the actual start time

    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],
                                   from_chat_id=message.from_user.id,
                                   message_id=message.message_id)
            x += 1
        except:
            y += 1
        await asyncio.sleep(0.05)

    end_time = time.time()  # Replace with the actual end time
    elapsed_time = end_time - start_time

    start_time_str = time.strftime("%H:%M:%S", time.localtime(start_time))
    end_time_str = time.strftime("%H:%M:%S", time.localtime(end_time))

    elapsed_minutes = elapsed_time / 60
    count = db.count_users()[0]
    await i.delete()
    await message.answer(f"<b>✅ Reklama quyidagi ko'rinishda yuborildi:</b>\n\n"
                         f"👥 <b>Qabul qildi:</b> {x} ta\n"
                         f"❌ <b>Yuborilmadi:</b> {y} ta\n"
                         f"⏳ <b>Boshlangan vaqti:</b> {start_time_str}\n"
                         f"⌛️ <b>Tugash vaqti:</b> {end_time_str}\n"
                         f"⏰ <b>Sarflangan vaqt:</b> {int(elapsed_minutes)} daqiqa\n➖➖➖➖➖➖➖➖➖\n🟢<b> Faol obunachilar:</b> {x} ta\n🔴<b> Faolsiz obunachilar:</b> {y} ta\n🧾 <b>Jami obunachilar:</b> {count} ta")
    await message.answer(
        "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
        reply_markup=adminpanel)
    await adpanel.yubor.set()


@dp.message_handler(state=verifyDeleteUsers.code)
async def verifyCode(message: Message):
    if message.text == " afdgjygkGKDJagJHGAJSGF1432UIGLhGJHGBHJjhgjhg ":
        await message.answer(
            "Kod to'g'ri. Endi pastdagi tugmani bosish orqali foydalanuvchilarni o'chirishingiz mumkin",
            reply_markup=DeleteUsers)
    else:
        await message.answer("Kod xato. Qayta urinib ko'ring yoki bekor qiling", reply_markup=backDelete)
        await verifyDeleteUsers.code.set()


@dp.callback_query_handler(state='*', text='back:delete')
async def backdelete(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
        reply_markup=adminpanel)


@dp.callback_query_handler(state='*', text='delete:verify')
async def deleteVerify(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db.delete_users()
    textm = await call.message.edit_text("✅ Bot foydalanuvchilari o'chirildi")
    await asyncio.sleep(4)
    await textm.edit_text("<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
                          reply_markup=adminpanel)


@dp.callback_query_handler(state='*', text='delete:back')
async def deleteback(call: CallbackQuery, state: FSMContext):
    await state.finish()
    textm = await call.message.edit_text("❌ Bekor qilindi")
    await asyncio.sleep(4)
    await call.message.edit_text(
        "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
        reply_markup=adminpanel)
    await adpanel.yubor.set()


@dp.callback_query_handler(state='*', text='base:back')
async def baseBack(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
        reply_markup=adminpanel)
    await adpanel.yubor.set()


@dp.callback_query_handler(state=bazayuk.byuk)
async def database(call: CallbackQuery, state: FSMContext):
    baza = call.data
    if baza == "database":
        doc = InputFile('data/main.db')
        await call.message.answer_document(document=doc, caption="💾 Sqlite db formatida yuklab olindi.")
        await state.finish()
        await call.message.delete()
        await call.message.answer(
            "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
            reply_markup=adminpanel)
        await adpanel.yubor.set()
    elif baza == "excel":
        users = db.select_all_users()
        workbook = xl.Workbook("users.xlsx")
        bold_format = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet("Users")
        worksheet.write('A1', 'ID', bold_format)
        worksheet.write('B1', 'Ism', bold_format)
        worksheet.write('C1', 'Username', bold_format)
        rowIndex = 2
        for user in users:
            fullname = user[1]
            username = user[2]
            tg_id = user[0]
            worksheet.write('A' + str(rowIndex), tg_id)
            worksheet.write('B' + str(rowIndex), fullname)
            worksheet.write('C' + str(rowIndex), f"@{username}")
            rowIndex += 1
        workbook.close()
        file = InputFile(path_or_bytesio="users.xlsx")
        await call.message.answer_document(document=file, caption="📑 Excel formatida yuklab olindi.")
        os.remove(path="users.xlsx")
        await state.finish()
        await call.message.delete()
        await call.message.answer(
            "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
            reply_markup=adminpanel)
        await adpanel.yubor.set()
    elif baza == "uyga":
        await state.finish()
        await call.message.edit_text(
            "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
            reply_markup=adminpanel)
        await adpanel.yubor.set()


@dp.callback_query_handler(state='*', text='ortga1')
async def baseBack(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "<b>👮🏻‍♂️ Xabarni foydalanuvchiga qay xolatda yubormoqchisiz?</b>\n\nQuyidagi tugmalardan birini tanlang👇🏻",
        reply_markup=allxabar)
    await send_user.tanla.set()


@dp.callback_query_handler(state=send_user.tanla)
async def send(call: CallbackQuery, state: FSMContext):
    teksh = call.data
    if teksh == "adnom":
        await call.message.edit_text(
            "<b>👨🏻‍💻 Admin nomidan xabar yozish uchun Foydalanuvchi 🆔 ID sini kiriting.</b>👇🏻",
            reply_markup=backall)
        await send_user.adminx.set()
    elif teksh == "botnom":
        await call.message.edit_text(
            "<b>🤖 Bot nomidan xabar yozish uchun Foydalanuvchi 🆔 ID sini kiriting.</b>👇🏻",
            reply_markup=backall)
        await send_user.botx.set()
    elif teksh == "qolda":
        await call.message.edit_text(
            "<b>✍🏻 O'zingiz xabar yozish uchun Foydalanuvchi 🆔 ID sini kiriting.</b>👇🏻",
            reply_markup=backall)
        await send_user.qold.set()
    elif teksh == "ortga":
        await state.finish()
        await call.message.edit_text(
            "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
            reply_markup=adminpanel)
        await adpanel.yubor.set()


@dp.message_handler(state=send_user.adminx)
async def id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer(
        f"<b>🆔 ID Raqam:</b> <code>{message.text}</code>\n📝 <b>Xabar:</b> ...\n\nFoydalanuvchiga xabar yuborish uchun yozing👇🏻",
        reply_markup=xtan)
    await send_user.adsend.set()


@dp.message_handler(state=send_user.adsend)
async def stepone(message: Message, state: FSMContext):
    await state.update_data(habar=message.text)
    data = await state.get_data()
    idi = data.get('id')
    habar = data.get('habar')
    status = False
    try:
        await bot.send_message(chat_id=idi,
                               text=f"<b>👨🏻‍💻 Xurmatli foydalanuvchi 'Bot Admini' sizga xabar yubordi:</b>\n\n{habar}",
                               parse_mode=types.ParseMode.HTML)
        status = True
    except aiogram.exceptions.ChatNotFound:
        status = False
        await message.answer(
            f"🆔 ID raqam xato kiritildi yoki ID raqam bo'yicha foydalanuvchi mavjud emas.\n\nID raqamni qayta "
            f"kiritib ko'ring👇🏻",
            reply_markup=cancel_adminAnswer)
        await send_user.adminx.set()
    if status:
        await message.answer(f"<b>✅ Yuborildi</b>\n\n"
                             f"ID: [<code>{idi}</code>]\n"
                             f"Xabar: {habar}\n\n"
                             f"Xabaringiz muvaffaqiyatli yuborildi", parse_mode=types.ParseMode.HTML)
        await state.finish()
        await message.answer(
            "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
            reply_markup=adminpanel)
        await adpanel.yubor.set()


@dp.message_handler(state=send_user.botx)
async def id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer(
        f"<b>🆔 ID Raqam:</b> <code>{message.text}</code>\n📝 <b>Xabar:</b> ...\n\nFoydalanuvchiga xabar yuborish uchun yozing👇🏻",
        reply_markup=xtan)
    await send_user.botsend.set()


@dp.message_handler(state=send_user.botsend)
async def stepone(message: Message, state: FSMContext):
    await state.update_data(habar=message.text)
    data = await state.get_data()
    idi = data.get('id')
    habar = data.get('habar')
    status = False
    try:
        await bot.send_message(chat_id=idi,
                               text=f"<b>🤖 Xurmatli foydalanuvchi bizning bot sizga quyidagi xabar beradi:</b>\n\n{habar}",
                               parse_mode=types.ParseMode.HTML)
        status = True
    except aiogram.exceptions.ChatNotFound:
        status = False
        await message.answer(
            f"🆔 ID raqam xato kiritildi yoki ID raqam bo'yicha foydalanuvchi mavjud emas.\n\nID raqamni qayta "
            f"kiritib ko'ring👇🏻",
            reply_markup=cancel_adminAnswer)
        await send_user.adminx.set()
    if status:
        await message.answer(f"<b>✅ Yuborildi</b>\n\n"
                             f"ID: [<code>{idi}</code>]\n"
                             f"Xabar: {habar}\n\n"
                             f"Xabaringiz muvaffaqiyatli yuborildi", parse_mode=types.ParseMode.HTML)
        await state.finish()
        await message.answer(
            "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
            reply_markup=adminpanel)
        await adpanel.yubor.set()


@dp.message_handler(state=send_user.qold)
async def id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer(
        f"<b>🆔 ID Raqam:</b> <code>{message.text}</code>\n📝 <b>Xabar:</b> ...\n\nFoydalanuvchiga xabar yuborish uchun yozing👇🏻",
        reply_markup=xtan)
    await send_user.qolsend.set()


@dp.message_handler(state=send_user.qolsend)
async def stepone(message: Message, state: FSMContext):
    await state.update_data(habar=message.text)
    data = await state.get_data()
    idi = data.get('id')
    habar = data.get('habar')
    status = False
    try:
        await bot.send_message(chat_id=idi,
                               text=f"{habar}",
                               parse_mode=types.ParseMode.HTML)
        status = True
    except aiogram.exceptions.ChatNotFound:
        status = False
        await message.answer(
            f"🆔 ID raqam xato kiritildi yoki ID raqam bo'yicha foydalanuvchi mavjud emas.\n\nID raqamni qayta "
            f"kiritib ko'ring👇🏻",
            reply_markup=cancel_adminAnswer)
        await send_user.adminx.set()
    if status:
        await message.answer(f"<b>✅ Yuborildi</b>\n\n"
                             f"ID: [<code>{idi}</code>]\n"
                             f"Xabar: {habar}\n\n"
                             f"Xabaringiz muvaffaqiyatli yuborildi", parse_mode=types.ParseMode.HTML)
        await state.finish()
        await message.answer(
            "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
            reply_markup=adminpanel)
        await adpanel.yubor.set()


@dp.callback_query_handler(state='*', text='cancel_adminAnswer')
async def cancelAdminAnswer(call: CallbackQuery, state: FSMContext):
    await state.finish()
    cancelText = await call.message.edit_text("🟢 Bekor qilindi")
    await call.message.answer(
        "<b> 👮🏻‍♂️ Admin Paneldasiz.</b> Quyidagi turli funksiyalardan foydalanishingiz mumkin👇🏻",
        reply_markup=adminpanel)
    await asyncio.sleep(2)
    await cancelText.delete()


############### ADMIN PANEL #####################


class AddKino(StatesGroup):
    WaitingForVideo = State()
    WaitingForName = State()
    WaitingForLang = State()
    WaitingForQuality = State()
    WaitingForGenre = State()
    WaitingForKod = State()


@dp.message_handler(content_types=types.ContentType.VIDEO, state=AddKino.WaitingForVideo)
async def process_video(message: types.Message, state: FSMContext):
    videoid = message.video.file_id
    await state.update_data(videoid=videoid)

    await message.answer("🎬 <b>Kino nomini yozib yuboring:</b>")
    await AddKino.WaitingForName.set()


@dp.message_handler(state=AddKino.WaitingForName)
async def process_name(message: types.Message, state: FSMContext):
    kinoname = message.text
    await state.update_data(kinoname=kinoname)

    await message.answer("🌐 <b>Kino tili (misol uchun: O'zbek tili)</b>")
    await AddKino.WaitingForLang.set()


@dp.message_handler(state=AddKino.WaitingForLang)
async def process_lang(message: types.Message, state: FSMContext):
    kinotili = message.text
    await state.update_data(kinotili=kinotili)

    await message.answer("💽 <b>Kino sifatini yozib yuboring:</b>\n\n<i>Misol uchun (HD, Full HD, 4K, 1080p, 720p)</i>")
    await AddKino.WaitingForQuality.set()


@dp.message_handler(state=AddKino.WaitingForQuality)
async def process_quality(message: types.Message, state: FSMContext):
    kinosifat = message.text
    await state.update_data(kinosifat=kinosifat)

    await message.answer("<b>🎭 Kinoning Janrini yozib yuboring:</b>")
    await AddKino.WaitingForGenre.set()


@dp.message_handler(state=AddKino.WaitingForGenre)
async def process_genre(message: types.Message, state: FSMContext):
    kinojanr = message.text
    await state.update_data(kinojanr=kinojanr)

    await message.answer("🎥<b> Kino kodini kiriting:</b> Siz yuborgan kod bilan kino izlanadi.")
    await AddKino.WaitingForKod.set()


@dp.message_handler(state=AddKino.WaitingForKod)
async def process_kod(message: types.Message, state: FSMContext):
    kod = message.text
    data = await state.get_data()
    videoid = data.get("videoid")
    kinoname = data.get("kinoname")
    kinotili = data.get("kinotili")
    kinosifat = data.get("kinosifat")
    kinojanr = data.get("kinojanr")
    db.create_table_kino()

    # Kinoni bazaga qo'shish
    db.add_kino(videoid=videoid, view=0, kod=kod,
                kinoname=kinoname, kinotili=kinotili, kinosifat=kinosifat, kinojanr=kinojanr)

    await state.finish()
    await message.answer("<b>🎬 Kino bazaga muvaffaqiyatli qo'shildi.</b>")


class DeleteKino(StatesGroup):
    WaitingForKod = State()


@dp.message_handler(state=DeleteKino.WaitingForKod, content_types=types.ContentType.TEXT)
async def del_kino_process(message: types.Message, state: FSMContext):
    kod_to_delete = message.text.strip()
    movie_info = db.get_movie_info_by_kod(kod_to_delete)
    if movie_info:
        db.delete_kino_by_kod(kod_to_delete)
        await message.answer(f"✅ <b>Kino (Kod: {kod_to_delete}) o'chirildi.</b>")
    else:
        await message.answer("<b>🎬 Kod bo'yicha xech qanday kino topilmadi.</b>\n\n📑 Barcha kino kodlari: @uzkinomovie")
    await state.finish()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_text(message: types.Message, state: FSMContext):
    response_text = message.text
    if response_text.isdigit():
        movie_info = db.get_movie_info_by_kod(response_text)
        if movie_info:
            videoid, kinoname, kinojanr, kinotili, kinosifat, view, kod = movie_info
            ulashish = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🎬 Do'stlartga Ulashish",
                                             switch_inline_query=f"/start bosing. Kino kodi: {kod}")
                    ]
                ]
            )
            # Ko'rishlar soni
            db.increment_view(kod)

            response_text = (
                f"🎬<b> Kino nomi:</b> {kinoname}\n\n"
                f"🎭<b> Janri:</b> {kinojanr}\n"
                f"🚩<b> Tili:</b> {kinotili}\n"
                f"🎥<b> Sifati:</b> {kinosifat}\n"
                f"👥<b> Ko'rishlar:</b> {view} ta\n\n🎞<b> Kino kodi:</b> <code>{kod}</code>\n\n"
                f"📺 Eng sara filmlar: @uzkinomovie\n📑 Barcha kino kodlari: @uzkinomovie"
            )
            await message.answer_video(video=videoid, caption=response_text, parse_mode="HTML", reply_markup=ulashish)
        else:
            await message.reply("<b>🎬 Kod bo'yicha xech qanday kino topilmadi.</b>\n\n📑 Barcha kino kodlari: @uzkinomovie")
    else:
        await message.reply("<b>🎬 Iltimos kino kodini yuboring:</b>\n\nKod faqat raqamdan iborat bo'lishi kerak.")
