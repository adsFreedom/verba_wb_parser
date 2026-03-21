from find_products import FindProducts
from settings.settings import Settings


def main():
    print("---=== START ===---")
    settings = Settings(save={"auto_create": True})

    find_products = FindProducts(settings)
    total_products = find_products.request_count_products()
    print(f'Find products: {total_products}')

    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
