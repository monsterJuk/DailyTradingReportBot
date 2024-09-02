from config import API_KEY, SECRET_KEY
import requests
import datetime
import time
import hmac
import hashlib

BASE_URL = 'https://contract.mexc.com/'


def _get_server_time():
    return int(time.time()*1000)


def get_datetime_info(days=0):
    # 24 hours in microseconds
    day_duration = 86400000

    current_date = datetime.datetime.today().replace(
        microsecond=0
    )

    timestamp_start_day = int(
        current_date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0).timestamp()) * 1000\
            - days * day_duration

    if not days:
        timestamp_end_day = int(
            current_date.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999).timestamp()) * 1000
    else:
        timestamp_end_day = int(
            current_date.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999).timestamp()) * 1000\
            - day_duration

    result = {
        'current_datetime': current_date,
        'timestamp_start_day': timestamp_start_day,
        'timestamp_end_day': timestamp_end_day
    }

    return result


def _sign_v1(sign_params=None):
    if sign_params:
        sign = "%s%s%s" % (API_KEY, _get_server_time(), sign_params)
    else:
        sign = "%s%s" % (API_KEY, _get_server_time())
    sign = hmac.new(
        SECRET_KEY.encode('utf-8'),
        sign.encode('utf-8'),
        hashlib.sha256).hexdigest()

    return sign


def get_history_positions(page_num: int, page_size=None, symbol=None) -> list:
    """get history positions"""
    method = 'GET'
    path = '/api/v1/private/position/list/history_positions'
    url = '{}{}'.format(BASE_URL, path)
    data_original = {
        'page_num': page_num
    }
    if page_size:
        data_original["page_size"] = page_size
    if symbol:
        data_original["symbol"] = symbol
    data = '&'.join('{}={}'.format(i, data_original[i]) for i in sorted(data_original))
    sign = _sign_v1(sign_params=data)
    headers = {
        "ApiKey": API_KEY,
        "Request-Time": str(_get_server_time()),
        "Signature": sign,
        "Content-Type": "application/json"
    }
    url = "%s%s%s" % (url, "?", data)
    response = requests.request(method, url, headers=headers).json()

    if response.get('success'):
        return response.get('data')
    else:
        return []


def get_positions_per_day(days) -> list:
    datetime_info = get_datetime_info(days)

    positions_in_report = []
    page_num = 1
    all_positions = get_history_positions(page_num=page_num, page_size=500)
    while all_positions:
        for position in all_positions:
            if position['updateTime'] >= datetime_info['timestamp_start_day'] and position['updateTime'] <= datetime_info['timestamp_end_day']:
                positions_in_report.append(position)
        page_num += 1
        all_positions = get_history_positions(page_num=page_num, page_size=500)

    return positions_in_report


def get_total_pnl(days=0) -> float:
    total_pnl = 0
    daily_positions = get_positions_per_day(days)

    for position in daily_positions:
        total_pnl += position['realised']

    return total_pnl.__round__(2)


def get_positions_count(days=0) -> int:
    return len(get_positions_per_day(days))
