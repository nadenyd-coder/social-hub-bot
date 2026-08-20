import os
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# SETTINGS
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "1394148142"))

INSTAGRAM = "_bk3_6"
TIKTOK = "bk.36_"
TELEGRAM = "bk_36"
DISCORD_ID = "1000576583721025608"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# =========================================================
# LANGUAGE SYSTEM
# =========================================================

# اللغة الافتراضية English
user_languages = {}


def get_language(user_id):
    return user_languages.get(user_id, "en")


# =========================================================
# TRANSLATIONS
# =========================================================

TEXTS = {

    "en": {
        "accounts": "My Accounts",
        "contact": "Contact Me",
        "share": "Share Social Hub",
        "about": "About",
        "language": "Language",
        "status": "Status: Online",
        "choose": "Choose an option:",
        "choose_account": "Choose an account:",
        "instagram": "Open Instagram",
        "tiktok": "Open TikTok",
        "telegram": "Open Telegram",
        "discord": "Open Discord",
        "copy": "Copy Username",
        "back": "Back",
        "home": "Home",
        "write_message": "Write your message below.",
        "cancel_text": "Type /cancel to cancel.",
        "sent": "Your message has been sent.",
        "cancelled": "Message cancelled.",
        "error": "An error occurred while sending the message.",
        "status_title": "Status",
        "status_text": "Social Hub is currently online.",
        "language_title": "Language",
        "welcome": (
            "Welcome.\n\n"
            "A simple place to find all my social accounts "
            "and contact me."
        ),
        "about": (
            "⚠️ WARNING — READ CAREFULLY\n\n"
            "You are about to discover the owner of this Social Hub.\n\n"
            "• Genius\n"
            "• Developer\n"
            "• Handsome\n"
            "• Gamer\n"
            "• Cyber Enthusiast\n"
            "• Visionary\n"
            "• Strategist\n"
            "• Digital Creator\n"
            "• Computer Enthusiast\n"
            "• Creative Mind\n\n"
            "Side effects may include:\n"
            "• Being impressed\n"
            "• Getting jealous\n"
            "• Questioning your own skills\n\n"
            "You have been warned.\n\n"
            "© 𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃"
        ),
    },

    "ar": {
        "accounts": "حساباتي",
        "contact": "مراسلتي",
        "share": "مشاركة Social Hub",
        "about": "حول",
        "language": "اللغة",
        "status": "الحالة: متصل",
        "choose": "اختر خياراً:",
        "choose_account": "اختر حساباً:",
        "instagram": "فتح إنستغرام",
        "tiktok": "فتح تيك توك",
        "telegram": "فتح تلغرام",
        "discord": "فتح ديسكورد",
        "copy": "نسخ اسم المستخدم",
        "back": "رجوع",
        "home": "الرئيسية",
        "write_message": "اكتب رسالتك أدناه.",
        "cancel_text": "اكتب /cancel للإلغاء.",
        "sent": "تم إرسال رسالتك.",
        "cancelled": "تم إلغاء الرسالة.",
        "error": "حدث خطأ أثناء إرسال الرسالة.",
        "status_title": "الحالة",
        "status_text": "Social Hub متصل حالياً.",
        "language_title": "اللغة",
        "welcome": (
            "أهلاً بك.\n\n"
            "مكان بسيط للوصول إلى جميع حساباتي "
            "والتواصل معي."
        ),
        "about": (
            "⚠️ تحذير — اقرأ بعناية\n\n"
            "أنت على وشك اكتشاف صاحب هذا الـ Social Hub.\n\n"
            "• عبقري\n"
            "• مطوّر\n"
            "• وسيم\n"
            "• لاعب ألعاب\n"
            "• شغوف بالتقنية السيبرانية\n"
            "• صاحب رؤية\n"
            "• استراتيجي\n"
            "• منشئ محتوى رقمي\n"
            "• مهتم بالحاسوب\n"
            "• عقل مبدع\n\n"
            "قد تشمل الآثار الجانبية:\n"
            "• الانبهار\n"
            "• الشعور بالغيرة\n"
            "• التشكيك بمهاراتك\n\n"
            "لقد تم تحذيرك.\n\n"
            "© 𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃"
        ),
    },

    "es": {
        "accounts": "Mis cuentas",
        "contact": "Contáctame",
        "share": "Compartir Social Hub",
        "about": "Acerca de",
        "language": "Idioma",
        "status": "Estado: En línea",
        "choose": "Elige una opción:",
        "choose_account": "Elige una cuenta:",
        "instagram": "Abrir Instagram",
        "tiktok": "Abrir TikTok",
        "telegram": "Abrir Telegram",
        "discord": "Abrir Discord",
        "copy": "Copiar usuario",
        "back": "Atrás",
        "home": "Inicio",
        "write_message": "Escribe tu mensaje abajo.",
        "cancel_text": "Escribe /cancel para cancelar.",
        "sent": "Tu mensaje ha sido enviado.",
        "cancelled": "Mensaje cancelado.",
        "error": "Ocurrió un error al enviar el mensaje.",
        "status_title": "Estado",
        "status_text": "Social Hub está actualmente en línea.",
        "language_title": "Idioma",
        "welcome": (
            "Bienvenido.\n\n"
            "Un lugar sencillo para encontrar todas mis "
            "redes sociales y contactarme."
        ),
        "about": (
            "⚠️ ADVERTENCIA — LEE CON ATENCIÓN\n\n"
            "Estás a punto de descubrir al dueño de este Social Hub.\n\n"
            "• Genio\n"
            "• Desarrollador\n"
            "• Guapo\n"
            "• Gamer\n"
            "• Entusiasta de la ciberseguridad\n"
            "• Visionario\n"
            "• Estratega\n"
            "• Creador digital\n"
            "• Entusiasta de los ordenadores\n"
            "• Mente creativa\n\n"
            "Los efectos secundarios pueden incluir:\n"
            "• Quedar impresionado\n"
            "• Sentir celos\n"
            "• Cuestionar tus propias habilidades\n\n"
            "Has sido advertido.\n\n"
            "© 𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃"
        ),
    },
}


# =========================================================
# MAIN MENU
# =========================================================

def main_menu(language=None):

    # القائمة الأولى الافتراضية English + عربي
    if language is None:

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "My Accounts — حساباتي",
                    callback_data="accounts"
                )
            ],
            [
                InlineKeyboardButton(
                    "Contact Me — مراسلتي",
                    callback_data="contact"
                )
            ],
            [
                InlineKeyboardButton(
                    "Share Social Hub — مشاركة البوت",
                    callback_data="share"
                )
            ],
            [
                InlineKeyboardButton(
                    "About — حول",
                    callback_data="about"
                )
            ],
            [
                InlineKeyboardButton(
                    "Language — اللغة",
                    callback_data="language"
                )
            ],
            [
                InlineKeyboardButton(
                    "Status: Online — الحالة: متصل",
                    callback_data="status"
                )
            ],
        ])

    t = TEXTS[language]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["accounts"],
                callback_data="accounts"
            )
        ],
        [
            InlineKeyboardButton(
                t["contact"],
                callback_data="contact"
            )
        ],
        [
            InlineKeyboardButton(
                t["share"],
                callback_data="share"
            )
        ],
        [
            InlineKeyboardButton(
                t["about"],
                callback_data="about"
            )
        ],
        [
            InlineKeyboardButton(
                t["language"],
                callback_data="language"
            )
        ],
        [
            InlineKeyboardButton(
                t["status"],
                callback_data="status"
            )
        ],
    ])


# =========================================================
# ACCOUNTS MENU
# =========================================================

def accounts_menu(language):

    t = TEXTS[language]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["instagram"],
                callback_data="instagram"
            )
        ],
        [
            InlineKeyboardButton(
                t["tiktok"],
                callback_data="tiktok"
            )
        ],
        [
            InlineKeyboardButton(
                t["telegram"],
                callback_data="telegram"
            )
        ],
        [
            InlineKeyboardButton(
                t["discord"],
                callback_data="discord"
            )
        ],
        [
            InlineKeyboardButton(
                t["copy"],
                callback_data="copy_usernames"
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="home"
            )
        ],
    ])


# =========================================================
# LANGUAGE MENU
# =========================================================

def language_menu():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "English",
                callback_data="set_en"
            )
        ],
        [
            InlineKeyboardButton(
                "العربية",
                callback_data="set_ar"
            )
        ],
        [
            InlineKeyboardButton(
                "Español",
                callback_data="set_es"
            )
        ],
        [
            InlineKeyboardButton(
                "Back",
                callback_data="home"
            )
        ],
    ])


# =========================================================
# USER INFO
# =========================================================

def get_user_info(user):

    username = (
        f"@{user.username}"
        if user.username
        else "No Username"
    )

    time_now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return (
        f"Name: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: <code>{user.id}</code>\n"
        f"Time: {time_now}"
    )


# =========================================================
# NOTIFICATION
# =========================================================

async def send_notification(
    context,
    action,
    user
):

    try:

        text = (
            "Visitor Activity\n\n"
            f"Action: {action}\n\n"
            f"{get_user_info(user)}"
        )

        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=text,
            parse_mode="HTML",
        )

    except Exception as error:

        logger.error(
            "Notification error: %s",
            error
        )


# =========================================================
# START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    # إذا ما اختار لغة، تظهر القائمة الرئيسية
    # English + عربي
    language = user_languages.get(user.id)

    t = TEXTS["en"]

    await update.message.reply_text(
        "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
        f"{t['welcome']}\n\n"
        "Choose an option — اختر خياراً:",
        parse_mode="HTML",
        reply_markup=main_menu(language),
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user
    language = get_language(user.id)
    t = TEXTS[language]


    # =====================================================
    # HOME
    # =====================================================

    if query.data == "home":

        if user.id in user_languages:

            await query.edit_message_text(
                "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
                + t["choose"],
                reply_markup=main_menu(language),
            )

        else:

            await query.edit_message_text(
                "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
                "Choose an option — اختر خياراً:",
                reply_markup=main_menu(),
            )


    # =====================================================
    # ACCOUNTS
    # =====================================================

    elif query.data == "accounts":

        await query.edit_message_text(
            t["choose_account"],
            reply_markup=accounts_menu(language),
        )


    # =====================================================
    # INSTAGRAM
    # =====================================================

    elif query.data == "instagram":

        await send_notification(
            context,
            "Instagram account button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    t["instagram"],
                    url=f"https://instagram.com/{INSTAGRAM}"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="accounts"
                )
            ],
            [
                InlineKeyboardButton(
                    t["home"],
                    callback_data="home"
                )
            ],
        ])

        await query.edit_message_text(
            f"Instagram\n\n@{INSTAGRAM}",
            reply_markup=keyboard,
        )


    # =====================================================
    # TIKTOK
    # =====================================================

    elif query.data == "tiktok":

        await send_notification(
            context,
            "TikTok account button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    t["tiktok"],
                    url=f"https://www.tiktok.com/@{TIKTOK}"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="accounts"
                )
            ],
            [
                InlineKeyboardButton(
                    t["home"],
                    callback_data="home"
                )
            ],
        ])

        await query.edit_message_text(
            f"TikTok\n\n@{TIKTOK}",
            reply_markup=keyboard,
        )


    # =====================================================
    # TELEGRAM
    # =====================================================

    elif query.data == "telegram":

        await send_notification(
            context,
            "Telegram account button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    t["telegram"],
                    url=f"https://t.me/{TELEGRAM}"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="accounts"
                )
            ],
            [
                InlineKeyboardButton(
                    t["home"],
                    callback_data="home"
                )
            ],
        ])

        await query.edit_message_text(
            f"Telegram\n\n@{TELEGRAM}",
            reply_markup=keyboard,
        )


    # =====================================================
    # DISCORD
    # =====================================================

    elif query.data == "discord":

        await send_notification(
            context,
            "Discord account button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    t["discord"],
                    url=f"https://discord.com/users/{DISCORD_ID}"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="accounts"
                )
            ],
            [
                InlineKeyboardButton(
                    t["home"],
                    callback_data="home"
                )
            ],
        ])

        await query.edit_message_text(
            f"Discord\n\nID: {DISCORD_ID}",
            reply_markup=keyboard,
        )


    # =====================================================
    # COPY USERNAMES
    # =====================================================

    elif query.data == "copy_usernames":

        await send_notification(
            context,
            "Copy Username button pressed",
            user
        )

        await query.edit_message_text(
            "Instagram: @" + INSTAGRAM + "\n"
            "TikTok: @" + TIKTOK + "\n"
            "Telegram: @" + TELEGRAM + "\n"
            "Discord ID: " + DISCORD_ID,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="accounts"
                    )
                ],
                [
                    InlineKeyboardButton(
                        t["home"],
                        callback_data="home"
                    )
                ],
            ]),
        )


    # =====================================================
    # ABOUT
    # =====================================================

    elif query.data == "about":

        await send_notification(
            context,
            "About button pressed",
            user
        )

        await query.edit_message_text(
            t["about"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="home"
                    )
                ]
            ]),
        )


    # =====================================================
    # CONTACT
    # =====================================================

    elif query.data == "contact":

        await send_notification(
            context,
            "Contact Me button pressed",
            user
        )

        context.user_data["contact_mode"] = True

        await query.edit_message_text(
            f"{t['write_message']}\n\n"
            f"{t['cancel_text']}",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["home"],
                        callback_data="home"
                    )
                ]
            ]),
        )


    # =====================================================
    # SHARE
    # =====================================================

    elif query.data == "share":

        bot_username = context.bot.username

        share_url = (
            f"https://t.me/{bot_username}"
            if bot_username
            else "https://t.me/"
        )

        share_text = (
            "Check out Social Hub\n"
            "https://t.me/"
            + (bot_username or "")
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Share",
                    switch_inline_query=share_text
                )
            ],
            [
                InlineKeyboardButton(
                    t["home"],
                    callback_data="home"
                )
            ],
        ])

        await query.edit_message_text(
            t["share"] + "\n\n" + share_url,
            reply_markup=keyboard,
        )


    # =====================================================
    # STATUS
    # =====================================================

    elif query.data == "status":

        await query.edit_message_text(
            f"{t['status_title']}\n\n"
            f"{t['status_text']}",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["home"],
                        callback_data="home"
                    )
                ]
            ]),
        )


    # =====================================================
    # LANGUAGE
    # =====================================================

    elif query.data == "language":

        await query.edit_message_text(
            "Language",
            reply_markup=language_menu(),
        )


    # =====================================================
    # SET ENGLISH
    # =====================================================

    elif query.data == "set_en":

        user_languages[user.id] = "en"

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            + TEXTS["en"]["choose"],
            reply_markup=main_menu("en"),
        )


    # =====================================================
    # SET ARABIC
    # =====================================================

    elif query.data == "set_ar":

        user_languages[user.id] = "ar"

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            + TEXTS["ar"]["choose"],
            reply_markup=main_menu("ar"),
        )


    # =====================================================
    # SET SPANISH
    # =====================================================

    elif query.data == "set_es":

        user_languages[user.id] = "es"

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            + TEXTS["es"]["choose"],
            reply_markup=main_menu("es"),
        )


# =========================================================
# MESSAGE HANDLER
# =========================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user = update.effective_user
    message = update.message

    language = get_language(user.id)
    t = TEXTS[language]


    # =====================================================
    # CANCEL
    # =====================================================

    if message.text == "/cancel":

        context.user_data["contact_mode"] = False

        await message.reply_text(
            t["cancelled"],
            reply_markup=main_menu(language),
        )

        return


    # =====================================================
    # NOT IN CONTACT MODE
    # =====================================================

    if not context.user_data.get("contact_mode"):

        await message.reply_text(
            t["choose"],
            reply_markup=main_menu(language),
        )

        return


    # =====================================================
    # MESSAGE OWNER
    # =====================================================

    username = (
        f"@{user.username}"
        if user.username
        else "No Username"
    )

    owner_message = (
        "New Message — Social Hub\n\n"
        f"Name: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: <code>{user.id}</code>\n\n"
        f"Message:\n{message.text}"
    )

    try:

        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=owner_message,
            parse_mode="HTML",
        )

        await message.reply_text(
            t["sent"],
            reply_markup=main_menu(language),
        )

    except Exception as error:

        logger.error(
            "Message sending error: %s",
            error
        )

        await message.reply_text(
            t["error"]
        )

    context.user_data["contact_mode"] = False


# =========================================================
# RUN BOT
# =========================================================

def main():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN is missing from GitHub Secrets"
        )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "cancel",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print(
        "Social Hub Bot is running..."
    )

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
