import logging

from config import TOKEN
from telegram import Update
from telegram.ext import Application, MessageHandler, \
    ContextTypes, CommandHandler, filters
from get_daily_report import get_daily_pnl, get_positions_per_day

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

# Set higher logging level for httpx to avoid all
# GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async  def handle_invalid_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        context._chat_id,
        "I can't to do anything yet. Wait for midnight and get your fucking report.")


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.ALL, handle_invalid_action))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
