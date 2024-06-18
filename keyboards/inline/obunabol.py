from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

check_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Kanal 1", url="https://t.me/kinomobitv"),
        ],
        [
            InlineKeyboardButton(text="🎦 Barcha Kino Kodlari", url="https://t.me/kinomobitv")
        ],
        [
            InlineKeyboardButton(text="Obuna bo'ldim ✅", callback_data="check_subs")
        ]
    ]
)