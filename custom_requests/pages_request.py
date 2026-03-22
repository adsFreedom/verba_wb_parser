import json
import math
from typing import Generator

from tqdm import tqdm

from custom_requests.limiter_request import LimiterRequest
from custom_requests.utils import str2wb_quote
from settings.settings import Settings


class PagesRequest(LimiterRequest):
    def __init__(self, settings: Settings):
        self.find_string = settings.find_string
        self.find_quote_str = str2wb_quote(self.find_string)
        self.x_wbaas_token = settings.x_wbaas_token

        self.find_products_dir = settings.save.pages_dir
        self.count_products_dir = settings.save.count_products_dir

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
        return total

    def request_products_pages(
            self, cnt_products: int = 0) -> Generator | None:
        """
        Find list products pages, 100 products per page.
        """
        print(f"Start find products {cnt_products} (100 per query)...")

        cnt_pages = math.ceil(cnt_products / 100)
        for page in tqdm(range(1, cnt_pages + 1)):
            url = (
                "https://www.wildberries.ru/__internal/"
                "u-search/exactmatch/ru/common/v18/search"
            )

            params = {
                "ab_testing": "false",
                "appType": "1",
                "curr": "rub",
                "dest": "-2228364",
                "hide_vflags": "4294967296",
                "inheritFilters": "false",
                "lang": "ru",
                "page": f"{page}",
                "query": f"{self.find_string}",
                "resultset": "catalog",
                "sort": "newly",
                "spp": "30",
                "suppressSpellcheck": "false",
            }

            headers = {
                "authority": "www.wildberries.ru",
                "accept": "*/*",
                "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "priority": "u=1, i",
                "referer": f"https://www.wildberries.ru/catalog/0/search.aspx?"
                           f"page={page}&sort=newly&"
                           f"search={self.find_quote_str}&meta_charcs=false",
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
                "x-spa-version": "14.2.3",
                "x-userid": "0",
                "cookie": f"x_wbaas_token={self.x_wbaas_token}"
            }

            save_file = self.find_products_dir / f"{page}_page.json"

            if (json_data := self.fetch(url=url, params=params,
                                        headers=headers)) is None:
                return None
            # with open(save_file, "r", encoding="utf-8") as f:
            #     json_data = json.load(f)
            # a = 2

            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            yield save_file
