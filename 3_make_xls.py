"""Debug script"""
import json

from pydantic import ValidationError
from tqdm import tqdm

from models import Product, Card, Goods
from settings.settings import Settings
from utils.xls_writer import XlsWriter


def main():
    print("---=== START ===---")
    is_debug = True

    settings = Settings(save={"auto_create": False})

    pages_dir = settings.save.pages_dir
    cards_dir = settings.save.cards_dir

    with XlsWriter("res.xlsx") as ws:
        for page_file in tqdm(pages_dir.glob("*")):
            print(f"Process page: {page_file.name}...")

            with open(page_file, "r", encoding="utf-8") as f:
                page_json = json.load(f)

            if (page_products := page_json["products"]) is None:
                raise f'Error: no field `products` in {page_file}'

            for i, page_product in enumerate(page_products):
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
                ws.write_good(goods)
                if is_debug:
                    print(f'-----------================INFO:')
                    print(f'Ссылка на товар: {goods.product_url}')
                    print(f'Aртикул: {goods.article}')
                    print(f'Название: {goods.name}')
                    print(f'Цена: {goods.price}')
                    print(f'Описание: {goods.description_short}')
                    print(f'Ссылки на изображения: {goods.img_urls}')
                    print(f'Характеристики: {goods.characteristics}')
                    print(f'Название селлера: {goods.seller_name}')
                    print(f'Ссылка на селлера: {goods.seller_url}')
                    print(f'Размеры(через запятую): {goods.sizes}')
                    print(f'Остатки по товару: {goods.quantity}')
                    print(f'Рейтинг товара: {goods.rating}')
                    print(f'Количество отзывов: {goods.feedbacks}')

                    if i >= 25:
                        break
            else:
                continue
            if is_debug:
                break
    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
