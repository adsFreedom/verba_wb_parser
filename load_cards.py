"""
Load info about every card from `find_all_products`
"""
from custom_requests.product_card import ProductCard
from settings.settings import Settings


def main():
    print("---=== START ===---")
    settings = Settings(save={"auto_create": False})

    product_card = ProductCard(settings)
    for _ in product_card.request_product_info():
        pass
    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
