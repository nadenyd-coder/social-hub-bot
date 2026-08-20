Social Hub Bot — bot.py

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

# لا نخزن اللغة بشكل دائم.
# تبقى فقط أثناء تشغيل البوت.
user_languages = {}


def get_language(user_id):
    return user_languages.get(user_id)


# =========================================================
# TRANSLATIONS
# =========================================================

TEXTS = {

    "en": {
        "accounts": "My Accounts",
        "contact": "Contact Me",
        "about": "About",
        "language": "Language",
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
        "language_title": "Language",
        "welcome": (
            "Welcome.\n\n"
            "A simple place to find all my social accounts "
            "and contact me."
        ),
        "about_text": (
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
        "contact": "تواصل معي",
        "about": "نبذة عني",
        "language": "اللغة",
        "choose": "اختر من القائمة:",
        "choose_account": "اختر حسابًا:",
        "instagram": "فتح Instagram",
        "tiktok": "فتح TikTok",
        "telegram": "فتح Telegram",
        "discord": "فتح Discord",
        "copy": "نسخ اسم المستخدم",
        "back": "رجوع",
        "home": "الرئيسية",
        "write_message": "اكتب رسالتك أدناه.",
        "cancel_text": "اكتب /cancel للإلغاء.",
        "sent": "تم إرسال رسالتك.",
        "cancelled": "تم إلغاء الرسالة.",
        "error": "حدث خطأ أثناء إرسال الرسالة.",
        "language_title": "اللغة",
        "welcome": (
            "أهلًا بك.\n\n"
            "مكان بسيط للوصول إلى جميع حساباتي "
            "والتواصل معي."
        ),
        "about_text": (
            "⚠️ تحذير — اقرأ بعناية\n\n"
            "أنت على وشك التعرّف إلى صاحب هذا الـ Social Hub.\n\n"
            "• عبقري\n"
            "• مطوّر\n"
            "• وسيم\n"
            "• لاعب ألعاب\n"
            "• شغوف بالأمن السيبراني\n"
            "• صاحب رؤية\n"
            "• استراتيجي\n"
            "• صانع محتوى رقمي\n"
            "• شغوف بالحاسوب\n"
            "• عقل مبدع\n\n"
            "قد تشمل الآثار الجانبية:\n"
            "• الانبهار\n"
            "• الغيرة\n"
            "• إعادة النظر في مهاراتك\n\n"
            "لقد تم تحذيرك.\n\n"
            "© 𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃"
        ),
    },

    "es": {
        "accounts": "Mis cuentas",
        "contact": "Contáctame",
        "about": "Acerca de mí",
        "language": "Idioma",
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
        "language_title": "Idioma",
        "welcome": (
            "Bienvenido.\n\n"
            "Un lugar sencillo para encontrar todas mis "
            "redes sociales y contactarme."
        ),
        "about_text": (
            "⚠️ ADVERTENCIA — LEE CON ATENCIÓN\n\n"
            "Estás a punto de conocer al dueño de este Social Hub.\n\n"
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

    "tr": {
        "accounts": "Hesaplarım",
        "contact": "Benimle İletişime Geç",
        "about": "Hakkımda",
        "language": "Dil",
        "choose": "Bir seçenek seçin:",
        "choose_account": "Bir hesap seçin:",
        "instagram": "Instagram'ı Aç",
        "tiktok": "TikTok'u Aç",
        "telegram": "Telegram'ı Aç",
        "discord": "Discord'u Aç",
        "copy": "Kullanıcı Adını Kopyala",
        "back": "Geri",
        "home": "Ana Sayfa",
        "write_message": "Mesajınızı aşağıya yazın.",
        "cancel_text": "İptal etmek için /cancel yazın.",
        "sent": "Mesajınız gönderildi.",
        "cancelled": "Mesaj iptal edildi.",
        "error": "Mesaj gönderilirken bir hata oluştu.",
        "language_title": "Dil",
        "welcome": (
            "Hoş geldiniz.\n\n"
            "Tüm sosyal hesaplarımı bulabileceğiniz "
            "ve benimle iletişime geçebileceğiniz basit bir alan."
        ),
        "about_text": (
            "⚠️ UYARI — DİKKATLİ OKUYUN\n\n"
            "Bu Social Hub'ın sahibini keşfetmek üzeresiniz.\n\n"
            "• Dahi\n"
            "• Geliştirici\n"
            "• Yakışıklı\n"
            "• Oyuncu\n"
            "• Siber Güvenlik Meraklısı\n"
            "• Vizyoner\n"
            "• Stratejist\n"
            "• Dijital İçerik Üreticisi\n"
            "• Bilgisayar Meraklısı\n"
            "• Yaratıcı Zihin\n\n"
            "Yan etkiler şunları içerebilir:\n"
            "• Etkilenmek\n"
            "• Kıskanmak\n"
            "• Kendi yeteneklerinizi sorgulamak\n\n"
            "Uyarıldınız.\n\n"
            "© 𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃"
        ),
    },
}


# =========================================================
# MAIN MENU
# =========================================================

def main_menu(language=None):

    # الوضع الافتراضي دائماً English + عربي
    if language is None or language in ("en", "ar"):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "My Accounts — حساباتي",
                    callback_data="accounts"
                )
            ],
            [
                InlineKeyboardButton(
                    "Contact Me — تواصل معي",
                    callback_data="contact"
                )
            ],
            [
                InlineKeyboardButton(
                    "About — نبذة عني",
                    callback_data="about"
                )
            ],
            [
                InlineKeyboardButton(
                    "Language — اللغة",
                    callback_data="language"
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
                "Türkçe",
                callback_data="set_tr"
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
# USER INFORMATION
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

    # اللغة لا تُحفظ بعد إعادة تشغيل البوت.
    # وإذا لم يختار المستخدم لغة بعد، تكون الرئيسية English + عربي.
    language = user_languages.get(user.id)

    if language is None:

        await update.message.reply_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            "Welcome — أهلًا بك\n\n"
            "Choose an option — اختر من القائمة:",
            reply_markup=main_menu(),
        )

    else:

        t = TEXTS[language]

        await update.message.reply_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            f"{t['welcome']}\n\n"
            f"{t['choose']}",
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

    # إذا لم يحدد لغة، نستخدم الإنجليزية للنصوص الداخلية.
    current_language = language if language else "en"
    t = TEXTS[current_language]


    # =====================================================
    # HOME
    # =====================================================

    if query.data == "home":

        # English والعربية = الرئيسية دائماً English + عربي
        if current_language in ("en", "ar"):

            await query.edit_message_text(
                "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
                "Welcome — أهلًا بك\n\n"
                "Choose an option — اختر من القائمة:",
                reply_markup=main_menu(current_language),
            )

        else:

            await query.edit_message_text(
                "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
                f"{t['choose']}",
                reply_markup=main_menu(current_language),
            )


    # =====================================================
    # MY ACCOUNTS
    # =====================================================

    elif query.data == "accounts":

        await send_notification(
            context,
            "My Accounts opened",
            user
        )

        await query.edit_message_text(
            t["choose_account"],
            reply_markup=accounts_menu(current_language),
        )


    # =====================================================
    # INSTAGRAM
    # =====================================================

    elif query.data == "instagram":

        await send_notification(
            context,
            "Instagram account opened",
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
            "TikTok account opened",
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
            "Telegram account opened",
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
            "Discord account opened",
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
            "About opened",
            user
        )

        await query.edit_message_text(
            t["about_text"],
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
    # CONTACT ME
    # =====================================================

    elif query.data == "contact":

        await send_notification(
            context,
            "Contact Me opened",
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
    # LANGUAGE
    # =====================================================

    elif query.data == "language":

        await query.edit_message_text(
            "Language",
            reply_markup=language_menu(),
        )


    # =====================================================
    # ENGLISH
    # =====================================================

    elif query.data == "set_en":

        user_languages[user.id] = "en"

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            "Welcome — أهلًا بك\n\n"
            "Choose an option — اختر من القائمة:",
            reply_markup=main_menu("en"),
        )


    # =====================================================
    # ARABIC
    # =====================================================

    elif query.data == "set_ar":

        user_languages[user.id] = "ar"

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            "Welcome — أهلًا بك\n\n"
            "Choose an option — اختر من القائمة:",
            reply_markup=main_menu("ar"),
        )


    # =====================================================
    # SPANISH
    # =====================================================

    elif query.data == "set_es":

        user_languages[user.id] = "es"

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            "Elige una opción:",
            reply_markup=main_menu("es"),
        )


    # =====================================================
    # TURKISH
    # =====================================================

    elif query.data == "set_tr":

        user_languages[user.id] = "tr"

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            "Bir seçenek seçin:",
            reply_markup=main_menu("tr"),
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

    if language is None:
        language = "en"

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
