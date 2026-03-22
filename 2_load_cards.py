"""
Load info about every card from `find_all_products`
"""
from custom_requests.cards_request import CardsRequest

from settings.settings import Settings


def main():
    print("---=== START ===---")
    settings = Settings(save={"auto_create": False})

    cards_request = CardsRequest(settings)
    for _ in cards_request.request_product_info():
        pass
    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
