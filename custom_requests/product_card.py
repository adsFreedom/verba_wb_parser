import json
from typing import Generator

from tqdm import tqdm

from custom_requests.limiter_request import LimiterRequest
from custom_requests.utils import str2wb_quote
from settings.settings import Settings


class ProductCard(LimiterRequest):
    def __init__(self, settings: Settings):
        self.find_string = settings.find_string
        self.find_quote_str = str2wb_quote(self.find_string)
        self.x_wbaas_token = settings.x_wbaas_token

        self.prod_cards_dir = settings.save.save_json_dir / "product_cards"
        self.prod_cards_dir.mkdir(parents=True, exist_ok=True)

        self.find_products_dir = settings.save.save_json_dir / "find_products"
        if not self.find_products_dir.exists():
            raise (f"Not exists directory {self.find_products_dir}"
                   f"Need first run script `find_all_products`")

        super().__init__(settings)

    def request_product_info(self) -> Generator:
        """Get info about every product card for additional information"""
        print(f'Start get product cards...')

        # get all prod_id
        all_prod_id_list = []
        for page_file in self.find_products_dir.glob("*"):
            with open(page_file, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            if (products_list := json_data.get('products')) is None:
                raise f"Error get field `products` in {page_file}"
            for product in products_list:
                if (prod_id := product.get("id")) is None:
                    raise f"Error get field `products.id` in {page_file}"
                all_prod_id_list.append(prod_id)

        # get ready prod_id
        ready_prod_id_list = []
        for prod_id in self.prod_cards_dir.glob("*"):
            ready_prod_id_list.append(int(prod_id.stem))

        # remove ready from need process
        prod_id_list = [prod_id for prod_id in all_prod_id_list
                        if prod_id not in ready_prod_id_list]

        print(f'  All      : {len(all_prod_id_list)}')
        print(f'  Ready    : {len(ready_prod_id_list)}')
        print(f'  Need load: {len(prod_id_list)}')
        print()

        for prod_id in tqdm(prod_id_list):
            sid = str(prod_id)

            url = (f"https://rst-basket-cdn-01bl.geobasket.ru/"
                   f"vol{sid[:4]}/part{sid[:6]}/{prod_id}/info/ru/card.json")

            params = {}
            headers = {
                "accept": "*/*",
                "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "referer": f"https://www.wildberries.ru/"
                           f"catalog/{prod_id}/detail.aspx",
                "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", '
                             '"Google Chrome";v="146"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/146.0.0.0 Safari/537.36"
            }
            if (json_data := self.fetch(url=url, params=params,
                                        headers=headers)) is None:
                continue

            save_file = self.prod_cards_dir / f"{prod_id}.json"
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            yield save_file
