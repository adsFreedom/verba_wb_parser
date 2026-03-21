import json
import urllib.parse
from typing import Generator

from limiter_request import LimiterRequest
from settings.settings import Settings


def str2wb_quote(src: str) -> str:
    """Make quote string as in WB"""
    return "+".join([urllib.parse.quote(s) for s in src.split(" ")])


class FindProducts(LimiterRequest):
    def __init__(self, settings: Settings):
        self.find_string = settings.find_string
        self.find_quote_str = str2wb_quote(self.find_string)
        self.x_wbaas_token = settings.x_wbaas_token

        self.find_products_dir = settings.save.save_json_dir / "find_products"
        self.find_products_dir.mkdir(parents=True, exist_ok=True)

        self.count_products_dir = settings.save.save_json_dir / "count_products"
        self.count_products_dir.mkdir(parents=True, exist_ok=True)

        self.products_count = 0
        super().__init__(settings)

    def request_count_products(self):
        """
        Request for get count products in search
        """
        print("Start get count products...")
        url = (
            "https://www.wildberries.ru/__internal/"
            "u-search/exactmatch/ru/common/v18/search"
        )

        params = {
            "ab_testing": "false",
            "appType": "1",
            "autoselectFilters": "false",
            "curr": "rub",
            "dest": "-2228364",
            "hide_vflags": "4294967296",
            "inheritFilters": "false",
            "lang": "ru",
            "query": f"{self.find_string}",
            "resultset": "filters",
            "scale": "4",
            "spp": "30",
            "suppressSpellcheck": "false",
        }

        headers = {
            "authority": "www.wildberries.ru",
            "method": "GET",
            "scheme": "https",
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": f"https://www.wildberries.ru/catalog/0/search.aspx?"
                       f"search={self.find_quote_str}",
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

        save_file = self.count_products_dir / "count_products.json"

        if (json_data := self.fetch(url=url, params=params,
                                    headers=headers)) is None:
            raise 'Error get count products'

        # with open(save_file, "r", encoding="utf-8") as f:
        #     json_data = json.load(f)

        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        if (json_data_data := json_data.get("data")) is None:
            raise (f'Error find field `data` in request count products '
                   f'(view {save_file.resolve()} file)')
        if (total := json_data_data.get("total")) is None:
            raise (f'Error find field `data.total` in request count products '
                   f'(view {save_file.resolve()} file)')
        print(f"Finish get count products {total}")
        self.products_count = total

    def request_products_pages(self, start_page: int = 1) -> Generator | None:
        print("Start find products (100 per query)...")




        # if self.products_count is None:

        page: int = 1
        while True:
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
                "query": f"{self.find_quote_str}",
                "resultset": "catalog",
                "sort": "newly",
                "spp": "30",
                "suppressSpellcheck": "false",
                "page": f"{page}",
                "autoselectFilters": "false",
            }

            headers = {
                "authority": "www.wildberries.ru",
                "method": "GET",
                "scheme": "https",
                "accept": "*/*",
                "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "referer": f"https://www.wildberries.ru/catalog/0/search.aspx?"
                           f"search={self.find_quote_str}",
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

            save_file = self.find_products_dir / f"{page}_find_products.json"

            if (json_data := self.fetch(url=url, params=params,
                                        headers=headers)) is None:
                return None
            # with open(save_file, "r", encoding="utf-8") as f:
            #     json_data = json.load(f)
            # a = 2

            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            yield save_file

            if (total := json_data.get("total", None)) is None:
                raise f"Error find field 'total' in request 'find_products'"
            if total <= page * 100:
                break

            page += 1
