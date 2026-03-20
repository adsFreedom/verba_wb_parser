from find_products import find_products
from settings.settings import settings

def main():
    print("---=== START ===---")

    find_str = "пальто из натуральной шерсти"
    x_wbaas_token = ""

    res = find_products(find_string=find_str,
                        x_wbaas_token=x_wbaas_token)
    print(f"find_products: {res=}")

    print("---=== FINISH ===---")


if __name__ == "__main__":
    main()
