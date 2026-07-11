"""Generate synthetic e-commerce data for the bronze data layer.

Default output:
    data/bronze/customers.csv  - 10,000 rows
    data/bronze/products.csv   - 1,000 rows
    data/bronze/orders.csv     - 100,000 rows
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

try:
    from faker import Faker
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "Missing dependency: faker. Install it with `pip install faker`."
    ) from exc


DEFAULT_CUSTOMERS = 10_000
DEFAULT_PRODUCTS = 1_000
DEFAULT_ORDERS = 100_000
DEFAULT_OUTPUT_DIR = Path("data/bronze")
DEFAULT_SEED = 42

CUSTOMER_SEGMENTS = ("new", "returning", "vip", "at_risk")
PRODUCT_CATEGORIES = (
    "electronics",
    "home",
    "fashion",
    "beauty",
    "sports",
    "toys",
    "books",
    "grocery",
)
ORDER_STATUSES = ("created", "paid", "shipped", "delivered", "cancelled", "refunded")
PAYMENT_METHODS = ("credit_card", "debit_card", "upi", "paypal", "gift_card")


def money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


def random_money(min_value: str, max_value: str) -> Decimal:
    cents = random.randint(int(Decimal(min_value) * 100), int(Decimal(max_value) * 100))
    return Decimal(cents) / Decimal(100)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_customers(fake: Faker, count: int) -> list[dict[str, object]]:
    customers = []

    for index in range(1, count + 1):
        created_at = fake.date_time_between(
            start_date="-3y",
            end_date="now",
            tzinfo=timezone.utc,
        )
        customers.append(
            {
                "customer_id": f"CUST{index:06d}",
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "phone_number": fake.phone_number(),
                "city": fake.city(),
                "state": fake.state(),
                "country": fake.country(),
                "customer_segment": random.choice(CUSTOMER_SEGMENTS),
                "created_at": created_at.isoformat(),
            }
        )

    return customers


def generate_products(fake: Faker, count: int) -> list[dict[str, object]]:
    products = []

    for index in range(1, count + 1):
        category = random.choice(PRODUCT_CATEGORIES)
        price = random_money("5.00", "1500.00")
        products.append(
            {
                "product_id": f"PROD{index:05d}",
                "product_name": f"{fake.word().title()} {category.title()} Item",
                "category": category,
                "brand": fake.company(),
                "unit_price": money(price),
                "is_active": random.choice((True, True, True, False)),
                "created_at": fake.date_time_between(
                    start_date="-4y",
                    end_date="now",
                    tzinfo=timezone.utc,
                ).isoformat(),
            }
        )

    return products


def generate_orders(
    customers: list[dict[str, object]],
    products: list[dict[str, object]],
    count: int,
) -> list[dict[str, object]]:
    orders = []
    start_date = datetime.now(timezone.utc) - timedelta(days=730)

    for index in range(1, count + 1):
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = Decimal(str(product["unit_price"]))
        discount_amount = random_money("0.00", "25.00")
        gross_amount = unit_price * quantity
        net_amount = max(gross_amount - discount_amount, Decimal("0.00"))
        order_date = start_date + timedelta(
            seconds=random.randint(0, 730 * 24 * 60 * 60)
        )

        orders.append(
            {
                "order_id": f"ORD{index:08d}",
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "order_date": order_date.isoformat(),
                "quantity": quantity,
                "unit_price": money(unit_price),
                "discount_amount": money(discount_amount),
                "order_amount": money(net_amount),
                "order_status": random.choice(ORDER_STATUSES),
                "payment_method": random.choice(PAYMENT_METHODS),
            }
        )

    return orders


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic customers, products, and orders CSV files."
    )
    parser.add_argument("--customers", type=int, default=DEFAULT_CUSTOMERS)
    parser.add_argument("--products", type=int, default=DEFAULT_PRODUCTS)
    parser.add_argument("--orders", type=int, default=DEFAULT_ORDERS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    random.seed(args.seed)
    Faker.seed(args.seed)
    fake = Faker()

    customers = generate_customers(fake, args.customers)
    products = generate_products(fake, args.products)
    orders = generate_orders(customers, products, args.orders)

    write_csv(
        args.output_dir / "customers.csv",
        list(customers[0].keys()),
        customers,
    )
    write_csv(
        args.output_dir / "products.csv",
        list(products[0].keys()),
        products,
    )
    write_csv(
        args.output_dir / "orders.csv",
        list(orders[0].keys()),
        orders,
    )

    print(f"Generated {len(customers):,} customers")
    print(f"Generated {len(products):,} products")
    print(f"Generated {len(orders):,} orders")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
