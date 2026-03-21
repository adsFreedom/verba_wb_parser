from custom_requests.find_products import FindProducts
from settings.settings import Settings


def main():
    print("---=== START ===---")
    settings = Settings(save={"auto_create": True})

    find_products = FindProducts(settings)
    prod_count = find_products.request_count_products()

    for page_json_file in find_products.request_products_pages(prod_count):
        pass

    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
