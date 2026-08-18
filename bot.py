import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
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

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 1394148142

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing from GitHub Secrets")

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# =========================================================
# USER MESSAGE MAPPING
# Used so the owner can reply to a forwarded message.
# =========================================================

forwarded_users = {}

# =========================================================
# MAIN MENU
# =========================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("👤 My Accounts", callback_data="accounts")
        ],
        [
            InlineKeyboardButton("✉️ Message Owner", callback_data="message_owner")
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# ACCOUNTS MENU
# =========================================================

def accounts_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🎵 TikTok",
                url="https://www.tiktok.com/@bk.36_"
            ),
            InlineKeyboardButton(
                "📸 Instagram",
                url="https://www.instagram.com/_bk3_6/"
            ),
        ],
        [
            InlineKeyboardButton(
                "💬 Telegram",
                url="https://t.me/bk_36"
            ),
            InlineKeyboardButton(
                "🎮 Discord",
                url="https://discord.com/users/1000576583721025608"
            ),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="home")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# /start
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = (
        "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
        "Welcome 👋\n"
        "هنا تگدر توصل إلى حساباتي ومراسلة صاحب البوت.\n\n"
        f"👤 You: {user.first_name}"
    )

    await update.message.reply_text(
        text,
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

    if query.data == "home":
        text = (
            "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
            "اختار من القائمة:"
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

    elif query.data == "accounts":
        text = (
            "👤 <b>My Accounts</b>\n\n"
            "اختار الحساب اللي تريد تزوره:"
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=accounts_menu(),
        )

    elif query.data == "message_owner":
        text = (
            "✉️ <b>مراسلة صاحب البوت</b>\n\n"
            "اكتب رسالتك هنا، وأنا أوصلها لصاحب البوت.\n\n"
            "تگدر ترسل نص، صورة، فيديو أو ملف."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        context.user_data["contact_owner"] = True

    elif query.data == "about":
        text = (
            "🌐 <b>𝑺𝒐𝒄𝒊𝒂𝒍 𝑯𝒖𝒃</b>\n\n"
            "بوت يجمع حسابات التواصل الاجتماعي بمكان واحد.\n\n"
            "👤 Developer: bk.36_"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


# =========================================================
# SEND MESSAGE TO OWNER
# =========================================================

async def receive_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    message = update.message

    if not message:
        return

    # Ignore commands
    if message.text and message.text.startswith("/"):
        return

    # Only relay when user selected "Message Owner"
    if not context.user_data.get("contact_owner"):
        return

    user_info = (
        f"📩 <b>New Social Hub Message</b>\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🔗 Username: "
        f"{'@' + user.username if user.username else 'None'}\n\n"
    )

    try:
        # Send information about the sender
        info_message = await context.bot.send_message(
            chat_id=OWNER_ID,
            text=user_info,
            parse_mode="HTML",
        )

        # Copy the actual message to the owner
        copied = await message.copy(
            chat_id=OWNER_ID
        )

        # Save relation between owner's message and visitor
        forwarded_users[copied.message_id] = user.id

        await message.reply_text(
            "✅ تم إرسال رسالتك إلى صاحب البوت."
        )

        context.user_data["contact_owner"] = False

    except Exception as e:
        logger.exception("Error sending message to owner: %s", e)

        await message.reply_text(
            "❌ صار خطأ أثناء إرسال الرسالة. حاول مرة ثانية."
        )


# =========================================================
# OWNER REPLY SYSTEM
# =========================================================

async def owner_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = update.message

    if not message:
        return

    # Only owner can use this
    if update.effective_user.id != OWNER_ID:
        return

    if not message.reply_to_message:
        return

    replied_message_id = message.reply_to_message.message_id

    user_id = forwarded_users.get(replied_message_id)

    if not user_id:
        await message.reply_text(
            "⚠️ ما لكيت الشخص المرتبط بهذه الرسالة."
        )
        return

    try:
        await message.copy(chat_id=user_id)

        await message.reply_text(
            "✅ تم إرسال ردك."
        )

    except Exception as e:
        logger.exception("Error replying to user: %s", e)

        await message.reply_text(
            "❌ ما قدرت أرسل الرد."
        )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.exception(
        "Unhandled exception:",
        exc_info=context.error
    )


# =========================================================
# START BOT
# =========================================================

def main():
    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Owner replies must be handled before normal messages
    application.add_handler(
        MessageHandler(
            filters.REPLY & ~filters.COMMAND,
            owner_reply
        )
    )

    application.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            receive_message
        )
    )

    application.add_error_handler(error_handler)

    print("✅ Social Hub Bot is running...")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
