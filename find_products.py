import json
from pathlib import Path
import urllib.parse

import requests


def find_products(find_string: str, x_wbaas_token: str) -> Path | None:
    """
    Generator for get product list and save to JSON file.

    Response from WB return only 100 items. Save to JSON by 100 items and
    add to name file `1_100`, `101_200`.
    """

    url = "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search"

    params = {
        "ab_testid": "model_size_dot",
        "appType": "1",
        "curr": "rub",
        "dest": "-2228364",
        "hide_vflags": "4294967296",
        "inheritFilters": "false",
        "lang": "ru",
        "query": f"{find_string}",
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
        "referer": f"https://www.wildberries.ru/catalog/0/search.aspx?search={urllib.parse.quote(find_string)}",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "x-spa-version": "14.2.2",
        "x-userid": "0",
        "cookie": f"x_wbaas_token={x_wbaas_token}"
    }
    return None
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        script_dir = Path(__file__).parent
        script_dir.mkdir(exist_ok=True)
        output_file = script_dir / "wb_search_result.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return output_file

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        print(f"Server response (first 200 simbols): {response.text[:200]}")

    except Exception as e:
        print(f"Error: Exception {e}")

    return None
