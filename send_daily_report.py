import requests

from config import TOKEN, message_recipient
from pprint import pprint
from get_daily_report import get_total_pnl, get_positions_count

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

METHOD_NAME = {
    'getMe': 'getMe',
    'sendMessage': 'sendMessage'
}

days = 0
total_pnl = get_total_pnl(days)
number_of_positions = get_positions_count(days)

url = f"{BASE_URL}{METHOD_NAME['sendMessage']}"
data = {
    'chat_id': message_recipient['monster'],
    'text': f"{total_pnl=}\n{number_of_positions=}"
}
response = requests.post(url, data)
