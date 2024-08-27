import requests

from config import TOKEN
from pprint import pprint
from get_daily_report import get_daily_pnl, get_positions_count

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

METHOD_NAME = {
    'getMe': 'getMe',
    'sendMessage': 'sendMessage'
}

daily_pnl = get_daily_pnl()
positions_per_day = get_positions_count()

url = f"{BASE_URL}{METHOD_NAME['sendMessage']}"
data = {
    'chat_id': 586622534,
    'text': f"{daily_pnl=}\n{positions_per_day=}"
}
response = requests.post(url, data)
