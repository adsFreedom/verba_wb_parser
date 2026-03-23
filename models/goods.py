from typing import ClassVar

from pydantic import BaseModel

from models.card import Card
from models.product import Product


class Goods(BaseModel):
    card: Card
    prod: Product

    EXPORT_FIELDS: ClassVar = [
        ("product_url", "Ссылка на товар"),
        ("article", "Артикул"),
        ("name", "Название"),
        ("price", "Цена (руб.)"),
        ("description", "Описание"),
        ("img_urls", "Ссылки на изображения"),
        ("characteristics", "Характеристики"),
        ("seller_name", "Название селлера"),
        ("seller_url", "Ссылка на селлера"),
        ("sizes", "Размеры товара"),
        ("quantity", "Остатки по товару"),
        ("rating", "Рейтинг"),
        ("feedbacks", "Количество отзывов"),
    ]

    @classmethod
    def export_headers(cls):
        return [title for _, title in cls.EXPORT_FIELDS]

    def export_row(self):
        row = []
        for attr, _ in self.EXPORT_FIELDS:
            value = getattr(self, attr)
            if isinstance(value, list):
                value = ", ".join(map(str, value))
            row.append(value)
        return row

    @property
    def product_url(self) -> str:
        return f"https://www.wildberries.ru/catalog/{self.prod.id}/detail.aspx"

    @property
    def article(self) -> str:
        return str(self.prod.id)

    @property
    def name(self) -> str:
        return self.card.name if self.card.name != "" else self.prod.name

    @property
    def price(self) -> float:
        p = max([p.price_prod for p in self.prod.sizes])
        return p / 100

    @property
    def description(self) -> str:
        return self.card.descr

    @property
    def description_short(self) -> str:
        return f"{self.card.descr[:50]} ... {self.card.descr[-50:]}"

    @property
    def img_urls(self) -> str:
        sid = str(self.prod.id)
        pic_url_list = []
        for p in range(1, self.prod.pics + 1):
            url = (f"https://rst-basket-cdn-03bl.geobasket.ru/"
                   f"vol{sid[:-5]}/part{sid[:-3]}/{sid}/images/big/{p}.webp")
            pic_url_list.append(url)
        return " ,\n".join(pic_url_list)

    @property
    def characteristics(self) -> str:
        res = ""
        for opt in self.card.options:
            res += f"{opt.name}:{opt.value},\n"

        for gopt in self.card.group_options:
            for opt in gopt.options:
                res += f"{opt.name}:{opt.value},\n"
        return res

    @property
    def seller_name(self) -> str:
        return self.prod.supplier

    @property
    def seller_url(self) -> str:
        return f"https://www.wildberries.ru/seller/{self.prod.supplier_id}"

    @property
    def sizes(self) -> str:
        return ",".join([s.name for s in self.prod.sizes])

    @property
    def quantity(self) -> int:
        return self.prod.total_quantity

    @property
    def rating(self) -> float:
        return self.prod.rating

    @property
    def feedbacks(self) -> int:
        return self.prod.feedbacks
