import random
import time
from functools import wraps
from typing import Any, Callable

import requests

from settings.settings import Settings


class LimiterRequest:

    def __init__(self, settings: Settings):
        self.min_delay_sec = settings.limits.min_delay_sec
        self.max_delay_sec = settings.limits.max_delay_sec
        self._last_call_time: float = time.time()

    @staticmethod
    def rate_limit(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            elapsed = time.time() - self._last_call_time
            target_delay = random.uniform(self.min_delay_sec,
                                          self.max_delay_sec)
            sleep_time = target_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            self._last_call_time = time.time()
            return func(self, *args, **kwargs)

        return wrapper

    @rate_limit
    def fetch(self, url: str, params: dict, headers: dict) -> Any:
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            response_json_data = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
            print(f"Server response (first 200 simbols): {response.text[:200]}")
            raise f'Error {e}'

        except Exception as e:
            print(f"Error: Exception {e}")
            raise f'Error {e}'
        return response_json_data
