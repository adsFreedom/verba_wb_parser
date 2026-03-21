from pydantic import BaseModel

from models.card import Card
from models.product import Product


class Goods(BaseModel):
    card: Card
    prod: Product

    @property
    def product_url(self) -> str:
        return f"https://www.wildberries.ru/catalog/{self.card.id}/detail.aspx"

    @property
    def article(self) -> str:
        return str(self.card.id)

    @property
    def name(self) -> str:
        return self.card.name

    @property
    def prices(self) -> list[str]:
        return [f"{p.price_prod // 100}.{p.price_prod % 100:02}"
                for p in self.prod.sizes]

    @property
    def description(self) -> str:
        return self.card.descr

    @property
    def description_short(self) -> str:
        return f"{self.card.descr[:50]} ... {self.card.descr[-50:]}"
