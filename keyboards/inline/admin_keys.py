from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


adminpanel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📢 Reklama Yuborish", callback_data='reklama'),
            InlineKeyboardButton(text="📊 Bot Statistikasi", callback_data='stats')
        ],
        [
            InlineKeyboardButton(text="🎬 Kino Qo'shish", callback_data="addkino"),
            InlineKeyboardButton(text="🚫 Kinoni O'chirish", callback_data="delkino"),
        ],
        [
            InlineKeyboardButton(text="🗑 Bazani O'chirish", callback_data='delete_users'),
            InlineKeyboardButton(text="🗄 Bazani Yuklash", callback_data='base')
        ],
        [
            InlineKeyboardButton(text="👤 Foydalanuvchiga Xabar Yuborish", callback_data='send')
        ],
    ],
)

allxabar = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👨🏻‍💻 Admin Nomidan", callback_data="adnom"),
            InlineKeyboardButton(text="🤖 Bot Nomidan", callback_data="botnom")
        ],
        [
            InlineKeyboardButton(text="✍🏻 Qo'lda Kiritish", callback_data="qolda"),
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="ortga")
        ],
    ]
)

xtan = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="ortga1")
        ],
    ]
)


BaseType = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚙️ Database", callback_data='database'),
            InlineKeyboardButton(text="📑 Excel", callback_data='excel')
        ],
        [
            InlineKeyboardButton(text="🔙 Ortga", callback_data="uyga")
        ]
    ]
)

DeleteUsers = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data='delete:verify'),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data='delete:back')
        ]
    ]
)

backDelete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Bekor qilish", callback_data='back:delete')
        ]
    ]
)

backall = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="base:back")
        ]
    ]
)