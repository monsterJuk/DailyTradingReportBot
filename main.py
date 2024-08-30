#!/usr/bin/env python

"""Bot for create and send tradings reports from MEXC.com"""

import logging

from config import TOKEN
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, \
    ContextTypes, CommandHandler, ConversationHandler, filters
from get_daily_report import get_total_pnl, get_positions_count

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

# Set higher logging level for httpx to avoid all
# GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


main_keyboard = [['/daily_report', '/custom_report']]

SELECT, CUSTOM_REPORT = range(2)

welcome_text = "Select report type"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await context.bot.send_message(
        context._chat_id,
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))


async def get_daily_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_pnl = get_total_pnl(0)
    number_of_positions = get_positions_count(0)

    daily_report_text = f"{total_pnl=}\n{number_of_positions=}"

    await context.bot.send_message(
        context._chat_id,
        daily_report_text
    )

    return SELECT


async def custom_report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    start_text = "Enter period (days)"

    await context.bot.send_message(
        context._chat_id,
        start_text,
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )

    return CUSTOM_REPORT


async def get_custom_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        number_of_days = int(update.message.text)
    except ValueError:
        await context.bot.send_message(
            context._chat_id,
            "Please input number of days"
        )

    total_pnl = get_total_pnl(number_of_days)
    number_of_positions = get_positions_count(number_of_days)

    custom_report_text = f"{total_pnl=}\n{number_of_positions=}"

    await context.bot.send_message(
        context._chat_id,
        custom_report_text,
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )

    return SELECT


async  def handle_invalid_select_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invalid_select_text = "Press the button below to select a report type"

    await context.bot.send_message(
        context._chat_id,
        invalid_select_text,
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )

    return SELECT


async def handle_invalid_input_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invalid_input_text = "Please input number of days"

    await context.bot.send_message(
        context._chat_id,
        invalid_input_text,
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('custom_report', custom_report_handler),
            CommandHandler('daily_report', get_daily_report)
        ],
        states={
            SELECT: [
                CommandHandler('daily_report', get_daily_report),
                CommandHandler('custom_report', custom_report_handler),
                MessageHandler(filters.ALL, handle_invalid_select_type)
            ],
            CUSTOM_REPORT: [
                MessageHandler(filters.TEXT, get_custom_report),
                MessageHandler(filters.ALL, handle_invalid_input_type)
            ]
        },
        fallbacks=[]
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
