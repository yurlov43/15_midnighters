import requests
from datetime import datetime, date, time
import pytz


def load_attempts(pages):
    api_url = 'http://devman.org/api/challenges/solution_attempts/?page={}'
    for page in range(1, pages+1, 1):
        request_link = api_url.format(page)
        users = requests.get(request_link).json()
        for user in users['records']:
            yield {
                'username': user['username'],
                'timestamp': user['timestamp'],
                'timezone': user['timezone'],
            }


def get_midnighters(start_time, end_time, users):
    for user in users:
        server_time = datetime.fromtimestamp(user['timestamp'])
        user_timezone = pytz.timezone(user['timezone'])
        user_time = user_timezone.fromutc(server_time).time()
        if user_time >= start_time and user_time <= end_time:
            yield {
                'username': user['username'],
                'usertime': user_time,
            }


def print_to_console(midnighters_users):
    for number, midnighters_user in enumerate(midnighters_users, start=1):
        print('{}. {}'.format(number, midnighters_user['username']))


if __name__ == '__main__':
    pages = 1
    users = load_attempts(pages)
    start_time = time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    end_time = time(hour=6, minute=0, second=0, microsecond=0, tzinfo=None)
    midnighters_users = get_midnighters(start_time, end_time, users)
    print_to_console(midnighters_users)
