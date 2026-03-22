from custom_requests.pages_request import PagesRequest

from settings.settings import Settings


def main():
    print("---=== START ===---")
    settings = Settings(save={"auto_create": True})

    pages_request = PagesRequest(settings)
    prod_count = pages_request.request_count_products()

    for _ in pages_request.request_products_pages(prod_count):
        pass

    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
