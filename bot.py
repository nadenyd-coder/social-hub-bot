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

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================
# MAIN MENU
# =========================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 My Accounts", callback_data="accounts")],
        [InlineKeyboardButton("💬 Message Owner", callback_data="contact")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ])


# =========================
# ACCOUNTS MENU
# =========================

def accounts_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("🎵 TikTok", callback_data="tiktok")],
        [InlineKeyboardButton("✈️ Telegram", callback_data="telegram")],
        [InlineKeyboardButton("🎮 Discord", callback_data="discord")],
        [InlineKeyboardButton("🔙 Back", callback_data="home")],
    ])


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
        "Welcome 👋\n"
        "اختار من القائمة:",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# =========================
# BUTTONS
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    # -------------------------
    # HOME
    # -------------------------

    if query.data == "home":
        await query.edit_message_text(
            "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
            "اختار من القائمة:",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

    # -------------------------
    # ACCOUNTS
    # -------------------------

    elif query.data == "accounts":
        await query.edit_message_text(
            "👤 <b>My Accounts</b>\n\n"
            "اختار الحساب:",
            parse_mode="HTML",
            reply_markup=accounts_menu(),
        )

    # -------------------------
    # INSTAGRAM
    # -------------------------

    elif query.data == "instagram":

        await send_visit_notification(
            context,
            user,
            "Instagram",
            f"@{INSTAGRAM}"
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
            f"اضغط لفتح الحساب:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    # -------------------------
    # TIKTOK
    # -------------------------

    elif query.data == "tiktok":

        await send_visit_notification(
            context,
            user,
            "TikTok",
            f"@{TIKTOK}"
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
            f"اضغط لفتح الحساب:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    # -------------------------
    # TELEGRAM
    # -------------------------

    elif query.data == "telegram":

        await send_visit_notification(
            context,
            user,
            "Telegram",
            f"@{TELEGRAM}"
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
            f"اضغط لفتح الحساب:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    # -------------------------
    # DISCORD
    # -------------------------

    elif query.data == "discord":

        await send_visit_notification(
            context,
            user,
            "Discord",
            DISCORD_ID
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
            f"اضغط لفتح الحساب:",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    # -------------------------
    # CONTACT OWNER
    # -------------------------

    elif query.data == "contact":

        context.user_data["contact_mode"] = True

        await query.edit_message_text(
            "💬 <b>Message Owner</b>\n\n"
            "اكتب رسالتك الآن وسأرسلها لصاحب البوت.\n\n"
            "للإلغاء اكتب /cancel",
            parse_mode="HTML",
        )

    # -------------------------
    # ABOUT
    # -------------------------

    elif query.data == "about":

        await query.edit_message_text(
            "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
            "بوت يجمع حسابات التواصل الاجتماعي بمكان واحد.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back",
                        callback_data="home"
                    )
                ]
            ]),
        )


# =========================
# VISIT NOTIFICATION
# =========================

async def send_visit_notification(
    context: ContextTypes.DEFAULT_TYPE,
    user,
    platform,
    account
):

    username = (
        f"@{user.username}"
        if user.username
        else "بدون Username"
    )

    time_now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    message = (
        "🔔 <b>Someone opened an account button</b>\n\n"
        f"🌐 Platform: <b>{platform}</b>\n"
        f"🔗 Account: {account}\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🔹 Username: {username}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🕐 Time: {time_now}"
    )

    try:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=message,
            parse_mode="HTML",
        )
    except Exception as error:
        logger.error(
            "Could not send notification: %s",
            error
        )


# =========================
# MESSAGES TO OWNER
# =========================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user = update.effective_user
    message = update.message

    if message.text == "/cancel":
        context.user_data["contact_mode"] = False

        await message.reply_text(
            "❌ تم إلغاء المراسلة.",
            reply_markup=main_menu(),
        )
        return

    if not context.user_data.get("contact_mode"):
        await message.reply_text(
            "استخدم /start لفتح القائمة."
        )
        return

    username = (
        f"@{user.username}"
        if user.username
        else "بدون Username"
    )

    text = (
        "📩 <b>New Message</b>\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🔹 Username: {username}\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"💬 Message:\n{message.text}"
    )

    try:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=text,
            parse_mode="HTML",
        )

        await message.reply_text(
            "✅ تم إرسال رسالتك.",
            reply_markup=main_menu(),
        )

    except Exception as error:
        logger.error(
            "Could not send owner message: %s",
            error
        )

        await message.reply_text(
            "❌ حدث خطأ أثناء إرسال الرسالة."
        )

    context.user_data["contact_mode"] = False


# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

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

    print("✅ Social Hub Bot is running...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
