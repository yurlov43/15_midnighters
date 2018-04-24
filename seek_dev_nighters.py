import requests
from datetime import datetime, date, time
import pytz


def load_attempts():
    page = 0
    api_url = 'http://devman.org/api/challenges/solution_attempts/'
    while True:
        page = page + 1
        attempt = requests.get(api_url, params={'page': page})
        if attempt.status_code != requests.codes.ok:
            break
        for user in attempt.json()['records']:
            yield {
                'username': user['username'],
                'timestamp': user['timestamp'],
                'timezone': user['timezone'],
            }


def get_midnighters(start_time, end_time, users):
    for user in users:
        user_timezone = pytz.timezone(user['timezone'])
        user_time = datetime.fromtimestamp(
            user['timestamp'],
            tz=user_timezone).time()
        if (user_time.hour >= start_time.hour and
                user_time.hour < end_time.hour):
            yield {
                'username': user['username'],
                'usertime': user_time,
            }


def print_to_console(midnighters_users):
    for number, midnighters_user in enumerate(midnighters_users, start=1):
        print('{}. {} ({})'.format(
            number,
            midnighters_user['username'],
            midnighters_user['usertime']))


if __name__ == '__main__':
    users = load_attempts()
    start_time = time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    end_time = time(hour=6, minute=0, second=0, microsecond=0, tzinfo=None)
    midnighters_users = get_midnighters(start_time, end_time, users)
    print_to_console(midnighters_users)
