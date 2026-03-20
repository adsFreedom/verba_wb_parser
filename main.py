from find_products import FindProducts
from settings.settings import settings


def main():
    print("---=== START ===---")

    find_products = FindProducts(
        find_string=settings.find_string,
        x_wbaas_token=settings.x_wbaas_token,
    )
    find_products.request()

    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
