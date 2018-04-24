import requests
from datetime import datetime, date, time
import pytz


def load_attempts():
    page = 0
    api_url = 'http://devman.org/api/challenges/solution_attempts/'
    while True:
        page = page + 1
        response = requests.get(api_url, params={'page': page})
        if not response:
            break
        for attempt in response.json()['records']:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }


def get_midnighters(attempts):
    for attempt in attempts:
        user_timezone = pytz.timezone(attempt['timezone'])
        user_time = datetime.fromtimestamp(
            attempt['timestamp'],
            tz=user_timezone).time()
        if user_time.hour >= 0 and user_time.hour < 6:
            yield {
                'username': attempt['username'],
                'usertime': user_time,
            }


def print_to_console(midnighters_attempts):
    for number, midnighters_attempt in enumerate(
            midnighters_attempts, start=1):
        print('{}. {} ({})'.format(
            number,
            midnighters_attempt['username'],
            midnighters_attempt['usertime']))


if __name__ == '__main__':
    attempts = load_attempts()
    midnighters_attempts = get_midnighters(attempts)
    print_to_console(midnighters_attempts)
