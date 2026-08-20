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

BOT_USERNAME = "Social_Hub"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


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
# MAIN MENU
# =========================================================

def main_menu():

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
                switch_inline_query="Check out Social Hub"
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


# =========================================================
# ACCOUNTS MENU
# =========================================================

def accounts_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "Instagram — إنستغرام",
                callback_data="instagram"
            )
        ],

        [
            InlineKeyboardButton(
                "TikTok — تيك توك",
                callback_data="tiktok"
            )
        ],

        [
            InlineKeyboardButton(
                "Telegram — تلغرام",
                callback_data="telegram"
            )
        ],

        [
            InlineKeyboardButton(
                "Discord — ديسكورد",
                callback_data="discord"
            )
        ],

        [
            InlineKeyboardButton(
                "Copy Username — نسخ اسم المستخدم",
                callback_data="copy_usernames"
            )
        ],

        [
            InlineKeyboardButton(
                "Back — رجوع",
                callback_data="home"
            )
        ],
    ])


# =========================================================
# START / WELCOME
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    welcome_text = (
        "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
        "Welcome — أهلاً بك\n\n"
        "A simple place to find all my social accounts "
        "and contact me.\n\n"
        "مكان بسيط للوصول إلى جميع حساباتي والتواصل معي."
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=main_menu(),
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


    # =====================================================
    # HOME
    # =====================================================

    if query.data == "home":

        await query.edit_message_text(
            "𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃\n\n"
            "Choose an option — اختر خياراً:",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


    # =====================================================
    # MY ACCOUNTS
    # =====================================================

    elif query.data == "accounts":

        await query.edit_message_text(
            "My Accounts — حساباتي\n\n"
            "Choose an account — اختر حساباً:",
            parse_mode="HTML",
            reply_markup=accounts_menu(),
        )


    # =====================================================
    # INSTAGRAM
    # =====================================================

    elif query.data == "instagram":

        await send_notification(
            context,
            "Instagram button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "Open Instagram — فتح إنستغرام",
                    url=f"https://instagram.com/{INSTAGRAM}"
                )
            ],

            [
                InlineKeyboardButton(
                    "Back — رجوع",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"Instagram — إنستغرام\n\n"
            f"@{INSTAGRAM}\n\n"
            "Click below to open the account — "
            "اضغط أدناه لفتح الحساب:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =====================================================
    # TIKTOK
    # =====================================================

    elif query.data == "tiktok":

        await send_notification(
            context,
            "TikTok button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "Open TikTok — فتح تيك توك",
                    url=f"https://www.tiktok.com/@{TIKTOK}"
                )
            ],

            [
                InlineKeyboardButton(
                    "Back — رجوع",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"TikTok — تيك توك\n\n"
            f"@{TIKTOK}\n\n"
            "Click below to open the account — "
            "اضغط أدناه لفتح الحساب:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =====================================================
    # TELEGRAM
    # =====================================================

    elif query.data == "telegram":

        await send_notification(
            context,
            "Telegram button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "Open Telegram — فتح تلغرام",
                    url=f"https://t.me/{TELEGRAM}"
                )
            ],

            [
                InlineKeyboardButton(
                    "Back — رجوع",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"Telegram — تلغرام\n\n"
            f"@{TELEGRAM}\n\n"
            "Click below to open the account — "
            "اضغط أدناه لفتح الحساب:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =====================================================
    # DISCORD
    # =====================================================

    elif query.data == "discord":

        await send_notification(
            context,
            "Discord button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "Open Discord — فتح ديسكورد",
                    url=f"https://discord.com/users/{DISCORD_ID}"
                )
            ],

            [
                InlineKeyboardButton(
                    "Back — رجوع",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"Discord — ديسكورد\n\n"
            f"ID: <code>{DISCORD_ID}</code>\n\n"
            "Click below to open the profile — "
            "اضغط أدناه لفتح الحساب:",
            parse_mode="HTML",
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
            "Usernames — أسماء المستخدمين\n\n"
            f"Instagram: @{INSTAGRAM}\n"
            f"TikTok: @{TIKTOK}\n"
            f"Telegram: @{TELEGRAM}\n"
            f"Discord ID: {DISCORD_ID}\n\n"
            "Copy them manually — انسخها يدوياً.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "Back — رجوع",
                        callback_data="accounts"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "Home — الرئيسية",
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

        about_text = (
            "⚠️ <b>WARNING — READ CAREFULLY</b>\n\n"

            "You are about to discover the owner "
            "of this Social Hub.\n\n"

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
        )

        await query.edit_message_text(
            about_text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "Back — رجوع",
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
            "Contact Me button pressed",
            user
        )

        context.user_data["contact_mode"] = True

        await query.edit_message_text(
            "Contact Me — مراسلتي\n\n"
            "Write your message below and I will receive it.\n\n"
            "اكتب رسالتك أدناه وسأستلمها.\n\n"
            "Type /cancel to cancel — "
            "اكتب /cancel للإلغاء.",
            parse_mode="HTML",
        )


    # =====================================================
    # LANGUAGE
    # =====================================================

    elif query.data == "language":

        await send_notification(
            context,
            "Language button pressed",
            user
        )

        await query.edit_message_text(
            "Language — اللغة\n\n"
            "English + العربية\n\n"
            "The interface currently uses both languages "
            "for a simple and clear experience.\n\n"
            "الواجهة تستخدم اللغتين حالياً لتكون بسيطة وواضحة.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "Back — رجوع",
                        callback_data="home"
                    )
                ]

            ]),
        )


    # =====================================================
    # STATUS
    # =====================================================

    elif query.data == "status":

        await send_notification(
            context,
            "Status button pressed",
            user
        )

        await query.edit_message_text(
            "Status — الحالة\n\n"
            "Online — متصل\n\n"
            "Social Hub is currently running.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "Back — رجوع",
                        callback_data="home"
                    )
                ]

            ]),
        )


# =========================================================
# SEND NOTIFICATION TO OWNER
# =========================================================

async def send_notification(
    context: ContextTypes.DEFAULT_TYPE,
    action,
    user
):

    try:

        text = (
            f"Visitor Activity\n\n"
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


    # =====================================================
    # CANCEL
    # =====================================================

    if message.text == "/cancel":

        context.user_data["contact_mode"] = False

        await message.reply_text(
            "Message cancelled — تم إلغاء الرسالة.",
            reply_markup=main_menu(),
        )

        return


    # =====================================================
    # NORMAL MESSAGE
    # =====================================================

    if not context.user_data.get("contact_mode"):

        await message.reply_text(
            "Use /start to open the menu."
        )

        return


    # =====================================================
    # SEND MESSAGE TO OWNER
    # =====================================================

    username = (
        f"@{user.username}"
        if user.username
        else "No Username"
    )

    owner_message = (
        "New Message — رسالة جديدة\n\n"

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
            "Message sent — تم إرسال الرسالة.",
            reply_markup=main_menu(),
        )

    except Exception as error:

        logger.error(
            "Message sending error: %s",
            error
        )

        await message.reply_text(
            "An error occurred — حدث خطأ أثناء الإرسال."
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
