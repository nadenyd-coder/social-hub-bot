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

# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "1394148142"))

INSTAGRAM = "_bk3_6"
TIKTOK = "bk.36_"
TELEGRAM = "bk_36"
DISCORD_ID = "1000576583721025608"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================
# MAIN MENU
# =========================

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 My Accounts",
                callback_data="accounts"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Message Owner",
                callback_data="contact"
            )
        ],
        [
            InlineKeyboardButton(
                "About",
                callback_data="about"
            )
        ],
    ])


# =========================
# ACCOUNTS MENU
# =========================

def accounts_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📸 Instagram",
                callback_data="instagram"
            )
        ],
        [
            InlineKeyboardButton(
                "🎵 TikTok",
                callback_data="tiktok"
            )
        ],
        [
            InlineKeyboardButton(
                "✈️ Telegram",
                callback_data="telegram"
            )
        ],
        [
            InlineKeyboardButton(
                "🎮 Discord",
                callback_data="discord"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="home"
            )
        ],
    ])


# =========================
# USER INFO
# =========================

def user_info(user):
    username = (
        f"@{user.username}"
        if user.username
        else "No Username"
    )

    time_now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return (
        f"👤 Name: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: <code>{user.id}</code>\n"
        f"Time: {time_now}"
    )


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
        "Welcome.\n"
        "Choose an option:",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user = query.from_user

    # =========================
    # HOME
    # =========================

    if query.data == "home":

        await query.edit_message_text(
            "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
            "Choose an option:",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


    # =========================
    # ACCOUNTS
    # =========================

    elif query.data == "accounts":

        await query.edit_message_text(
            "👤 <b>My Accounts</b>\n\n"
            "Choose an account:",
            parse_mode="HTML",
            reply_markup=accounts_menu(),
        )


    # =========================
    # INSTAGRAM
    # =========================

    elif query.data == "instagram":

        await send_notification(
            context,
            "📸 Instagram button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📸 Open Instagram",
                    url=f"https://instagram.com/{INSTAGRAM}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"📸 <b>Instagram</b>\n\n"
            f"Account: @{INSTAGRAM}\n\n"
            f"Click below to open the account:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =========================
    # TIKTOK
    # =========================

    elif query.data == "tiktok":

        await send_notification(
            context,
            "🎵 TikTok button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎵 Open TikTok",
                    url=f"https://www.tiktok.com/@{TIKTOK}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"🎵 <b>TikTok</b>\n\n"
            f"Account: @{TIKTOK}\n\n"
            f"Click below to open the account:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =========================
    # TELEGRAM
    # =========================

    elif query.data == "telegram":

        await send_notification(
            context,
            "✈️ Telegram button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✈️ Open Telegram",
                    url=f"https://t.me/{TELEGRAM}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"✈️ <b>Telegram</b>\n\n"
            f"Account: @{TELEGRAM}\n\n"
            f"Click below to open the account:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =========================
    # DISCORD
    # =========================

    elif query.data == "discord":

        await send_notification(
            context,
            "🎮 Discord button pressed",
            user
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎮 Open Discord",
                    url=f"https://discord.com/users/{DISCORD_ID}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="accounts"
                )
            ],
        ])

        await query.edit_message_text(
            f"🎮 <b>Discord</b>\n\n"
            f"ID: <code>{DISCORD_ID}</code>\n\n"
            f"Click below to open the profile:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =========================
    # ABOUT
    # =========================

    elif query.data == "about":

        # إرسال إشعار لصاحب البوت
        await send_notification(
            context,
            "⚠️ About button pressed",
            user
        )

        about_text = (
            "⚠️ <b>WARNING — READ CAREFULLY</b>\n\n"
            "You are about to discover the owner of this Social Hub.\n\n"
            "Genius\n"
            "Programmer\n"
            "Handsome\n"
            "Gamer\n\n"
            "Side effects may include:\n"
            "• Being impressed\n"
            "• Getting jealous\n"
            "• Questioning your own skills\n\n"
            "You have been warned.\n\n"
            "© 𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="home"
                )
            ]
        ])

        await query.edit_message_text(
            about_text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )


    # =========================
    # MESSAGE OWNER
    # =========================

    elif query.data == "contact":

        # إشعار عند مجرد فتح خيار المراسلة
        await send_notification(
            context,
            "💬 Message Owner button pressed",
            user
        )

        context.user_data["contact_mode"] = True

        await query.edit_message_text(
            "💬 <b>Message Owner</b>\n\n"
            "Write your message and I will send it to the owner.\n\n"
            "To cancel, type /cancel",
            parse_mode="HTML",
        )


# =========================
# NOTIFICATION
# =========================

async def send_notification(
    context: ContextTypes.DEFAULT_TYPE,
    action,
    user
):

    try:

        text = (
            f"{action}\n\n"
            f"{user_info(user)}"
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


# =========================
# MESSAGE HANDLER
# =========================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user = update.effective_user
    message = update.message

    # -------------------------
    # CANCEL
    # -------------------------

    if message.text == "/cancel":

        context.user_data["contact_mode"] = False

        await message.reply_text(
            "❌ Message cancelled.",
            reply_markup=main_menu(),
        )

        return


    # -------------------------
    # NORMAL MESSAGE
    # -------------------------

    if not context.user_data.get("contact_mode"):

        await message.reply_text(
            "Use /start to open the menu."
        )

        return


    # -------------------------
    # SEND MESSAGE TO OWNER
    # -------------------------

    username = (
        f"@{user.username}"
        if user.username
        else "No Username"
    )

    owner_message = (
        "📩 <b>New Message From Social Hub</b>\n\n"
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
            "✅ Your message has been sent.",
            reply_markup=main_menu(),
        )

    except Exception as error:

        logger.error(
            "Message sending error: %s",
            error
        )

        await message.reply_text(
            "❌ An error occurred while sending the message."
        )

    context.user_data["contact_mode"] = False


# =========================
# RUN BOT
# =========================

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
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("cancel", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("Social Hub Bot is running...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
