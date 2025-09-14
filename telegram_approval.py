import logging  # Used for debugging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Application → main bot runner.
# CommandHandler → listens for commands like /start.
# CallbackQueryHandler → handles button clicks (yes/no).
# MessageHandler → listens to normal text messages (rating).

import os
from dotenv import load_dotenv

load_dotenv()

import datetime  # used for date and time
from head import connect_to_gsheets  # to connect to sheet
from post_gen import final_work  # function that builds post

# Api token and chat_id
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
# BOT Gives output like this
# 2025-09-07 15:30 - telegram.bot - INFO - Bot started

# stored in memory for reuse on feedback
new_post = None


# -------------------------------
# Generate post and get (yes/no) approval
# -------------------------------


# RUNS without /start calling for simplicity
async def start(app, feedback=""):
    # new post collect
    global new_post
    new_post = final_work(feedback=feedback)

    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data="yes"),
            InlineKeyboardButton("❌ No", callback_data="no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await app.bot.send_message(
        chat_id=CHAT_ID,
        text=f"📢 New Post Proposal:\n\n{new_post}\n\nApprove?",
        reply_markup=reply_markup,
    )


# -------------------------------
# Collects response of type (yes/no)
# If yes-> rating_handler
# If no-> get to start
# -------------------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global new_post
    query = update.callback_query
    await query.answer()

    if query.data == "yes":
        await query.edit_message_text(
            text=f"✅ Approved Post:\n\n{new_post}\n\nNow rate (1-10):"
        )
        # Next: wait for rating message
    elif query.data == "no":
        # Generate a new post
        feedback = f"""
        Unfortunately, i did not like the last post you gave me which was {new_post}\n
        Generate the post again and make some necessary changes .
        """
        await query.edit_message_text("❌ Rejected. Generating a new post...")
        await start(context.application, feedback=feedback)


# -------------------------------
# Get ratings after approval of post , then the bot stops
# -------------------------------
async def rating_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global new_post
    try:
        rating = int(update.message.text.strip())
        if 1 <= rating <= 10:
            worksheet = connect_to_gsheets()
            worksheet.append_row([str(datetime.date.today()), new_post, "Yes", rating])
            await update.message.reply_text("💾 Saved to Google Sheet ✅")
            context.application.stop_running()
        else:
            await update.message.reply_text("⚠️ Please send a number 1-10")
    except ValueError:
        await update.message.reply_text("⚠️ Send a valid number (1-10)")


# -------------------------------
# Synchronizes all the tasks
# -------------------------------
def get_telegram_approval():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rating_handler))

    # Handlers
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("rating", rating_handler))
    app.add_handler(CommandHandler("start", lambda u, c: start(app)))
    app.add_handler(
        CommandHandler(
            "help",
            lambda u, c: u.message.reply_text("Just reply with 1–10 after approval."),
        )
    )
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rating_handler))

    # Start bot + send post immediately

    async def on_startup(app: Application):
        await start(app)

    app.post_init = on_startup

    # Run bot
    app.run_polling()
