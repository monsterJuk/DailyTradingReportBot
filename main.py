
import logging

from config import TOKEN, eligible_users
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, \
    ContextTypes, CommandHandler, ConversationHandler, filters
from get_daily_report_utc import get_total_pnl, \
    get_positions_count, get_datetime_info

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
not_eligible_text = "Sorry you are not eligible for using this bot"


def check_user_eligibility(user_id) -> bool:
    return True if user_id in eligible_users.values() else False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if check_user_eligibility(context._user_id):
        await context.bot.send_message(
            context._chat_id,
            welcome_text,
            reply_markup=ReplyKeyboardMarkup(
                main_keyboard,
                resize_keyboard=True)
        )

        return SELECT

    else:
        await context.bot.send_message(
            context._chat_id,
            not_eligible_text
        )


async def get_daily_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    datetime_info = get_datetime_info()
    total_pnl = get_total_pnl()
    number_of_positions = get_positions_count()

    daily_report_text = f"{total_pnl=}\n{number_of_positions=}\n\
Current datetime: {datetime_info['current_datetime']}"

    await context.bot.send_message(
        context._chat_id,
        daily_report_text
    )

    return SELECT


async def custom_report_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    start_text = "Enter period (days)"

    await context.bot.send_message(
        context._chat_id,
        start_text,
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard,
            resize_keyboard=True)
    )

    return CUSTOM_REPORT


async def get_custom_report(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    try:
        number_of_days = int(update.message.text)
    except ValueError:
        await context.bot.send_message(
            context._chat_id,
            "Please input number of days"
        )

    datetime_info = get_datetime_info(number_of_days)
    total_pnl = get_total_pnl(number_of_days)
    number_of_positions = get_positions_count(number_of_days)

    custom_report_text = f"{total_pnl=}\n{number_of_positions=}\n\
    Current datetime: {datetime_info['current_datetime']}"

    await context.bot.send_message(
        context._chat_id,
        custom_report_text,
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard,
            resize_keyboard=True)
    )

    return SELECT


async def handle_invalid_select_type(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
        
    invalid_select_text = "Press the button below to select a report type"

    await context.bot.send_message(
        context._chat_id,
        invalid_select_text,
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard,
            resize_keyboard=True)
    )

    return SELECT


async def handle_invalid_input_type(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    invalid_input_text = "Please input number of days"

    await context.bot.send_message(
        context._chat_id,
        invalid_input_text,
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard,
            resize_keyboard=True)
    )


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
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

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
