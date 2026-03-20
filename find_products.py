import json
import urllib.parse
from pathlib import Path

from limiter_request import LimiterRequest
from settings.settings import Settings


class FindProducts(LimiterRequest):
    def __init__(self, settings: Settings,
                 saved_json_dir: Path = Path("saved_json_data")):
        self.find_string = settings.find_string
        self.x_wbaas_token = settings.x_wbaas_token

        self.saved_products_dir = saved_json_dir / "find_products"
        self.saved_products_dir.mkdir(parents=True, exist_ok=True)

        super().__init__(settings)

    def request(self) -> Path | None:
        url = (
            "https://www.wildberries.ru/__internal/"
            "u-search/exactmatch/ru/common/v18/search"
        )

        params = {
            "ab_testid": "model_size_dot",
            "appType": "1",
            "curr": "rub",
            "dest": "-2228364",
            "hide_vflags": "4294967296",
            "inheritFilters": "false",
            "lang": "ru",
            "query": f"{self.find_string}",
            "resultset": "catalog",
            "sort": "popular",
            "spp": "30",
            "suppressSpellcheck": "false"
        }

        headers = {
            "authority": "www.wildberries.ru",
            "method": "GET",
            "scheme": "https",
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": f"https://www.wildberries.ru/catalog/0/search.aspx?"
                       f"search={urllib.parse.quote(self.find_string)}",
            "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", '
                         '"Google Chrome";v="146"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/146.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
            "x-spa-version": "14.2.2",
            "x-userid": "0",
            "cookie": f"x_wbaas_token={self.x_wbaas_token}"
        }
        if (json_data := self.fetch(url=url, params=params,
                                    headers=headers)) is None:
            return None

        save_file = self.saved_products_dir / "find_products.json"
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
