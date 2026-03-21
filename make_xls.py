"""Debug script"""
import json

from tqdm import tqdm

from models import Product, Card, Goods
from settings.settings import Settings
from pydantic import ValidationError


def main():
    print("---=== START ===---")
    settings = Settings(save={"auto_create": False})

    pages_dir = settings.save.save_json_dir / "find_products"
    cards_dir = settings.save.save_json_dir / "product_cards"

    for page_file in tqdm(pages_dir.glob("*")):
        print(f"Process page: {page_file.name}...")

        with open(page_file, "r", encoding="utf-8") as f:
            page_json = json.load(f)

        if (page_products := page_json["products"]) is None:
            raise f'Error: no field `products` in {page_file}'

        for page_product in page_products:
            try:
                product = Product.model_validate(page_product)
            except ValidationError as e:
                print(e)
                raise f'Error: validate Product in {page_file=}'

            card_file = cards_dir / f"{product.id}.json"
            if not card_file.exists():
                print(f'Error: NOT found file {card_file}')
                continue

            with open(card_file, "r", encoding="utf-8") as f:
                card_json = json.load(f)
            try:
                card = Card.model_validate(card_json)
            except ValidationError as e:
                print(e)
                raise f'Error: validate Card in {card_file=}'

            goods = Goods(card=card, prod=product)
            # show all data
            print(f'INFO:')
            print(f'Ссылка на товар: {goods.product_url}')
            print(f'Aртикул: {goods.article}')
            print(f'Название: {goods.name}')
            print(f'Цены: {goods.prices}')
            print(f'Описание: {goods.description_short}')
            # print(f'Цена(база): {goods.price_base}')


            a = 2
        a = 2

    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
