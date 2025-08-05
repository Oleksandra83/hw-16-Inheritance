import os
from typing import Union

# --- Користувацький виняток, що логгує помилки ---
class CustomException(Exception):
    """
    Користувацький виняток, що логгує кожне повідомлення про помилку у файл 'logs.txt'.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self._log_error(message)

    def _log_error(self, message: str):
        log_file = 'logs.txt'
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"ERROR: {message}\n")
        except Exception:
            pass


# --- Клас Product ---
class Product:
    """
    Представляє окремий продукт з типом, назвою та базовою ціною.
    """
    def __init__(self, type: str, name: str, price: float):
        if not isinstance(type, str) or not type:
            raise CustomException("Тип продукту має бути непорожнім рядком.")
        if not isinstance(name, str) or not name:
            raise CustomException("Назва продукту має бути непорожнім рядком.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise CustomException("Ціна продукту має бути додатним числом.")

        self.type = type
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(type='{self.type}', name='{self.name}', price={self.price})"


# --- Клас ProductStore ---
class ProductStore:
    PRICE_PREMIUM_FACTOR = 1.30

    def __init__(self):
        self.products = {}
        self.income = 0.0

    def add(self, product: Product, amount: int):
        if not isinstance(product, Product):
            raise CustomException("Додавати можна лише об'єкти класу Product.")
        if not isinstance(amount, int) or amount <= 0:
            raise CustomException("Кількість продукту має бути додатним цілим числом.")

        if product.name in self.products:
            self.products[product.name]['amount'] += amount
        else:
            self.products[product.name] = {
                'product_obj': product,
                'amount': amount,
                'discount_percent': 0.0
            }

    def set_discount(self, identifier: Union[str, int], percent: Union[int, float], identifier_type: str = 'name'):
        if not (0 <= percent <= 100):
            raise CustomException("Відсоток знижки має бути від 0 до 100.")
        if identifier_type not in ['name', 'type']:
            raise CustomException("identifier_type має бути 'name' або 'type'.")

        found_match = False
        for product_data in self.products.values():
            product_obj = product_data['product_obj']

            if identifier_type == 'name' and product_obj.name == identifier:
                product_data['discount_percent'] = percent
                found_match = True
            elif identifier_type == 'type' and product_obj.type == identifier:
                product_data['discount_percent'] = percent
                found_match = True

        if not found_match:
            raise CustomException(f"Продукт(и) з ідентифікатором '{identifier}' (тип: {identifier_type}) не знайдено.")

    def sell_product(self, product_name: str, amount: int):
        if not isinstance(product_name, str) or not product_name:
            raise CustomException("Назва продукту має бути непорожнім рядком.")
        if not isinstance(amount, int) or amount <= 0:
            raise CustomException("Кількість для продажу має бути додатним цілим числом.")
        if product_name not in self.products:
            raise CustomException(f"Продукту '{product_name}' немає в наявності.")

        product_data = self.products[product_name]
        current_amount = product_data['amount']
        product_obj = product_data['product_obj']
        discount_percent = product_data['discount_percent']

        if current_amount < amount:
            raise CustomException(f"Недостатньо '{product_name}' на складі. Доступно: {current_amount}, запитано: {amount}.")

        price_after_premium = product_obj.price * self.PRICE_PREMIUM_FACTOR
        final_unit_price = price_after_premium * (1 - discount_percent / 100)

        product_data['amount'] -= amount
        self.income += final_unit_price * amount

    def get_income(self) -> float:
        return self.income

    def get_all_products(self) -> list:
        all_products_info = []
        for product_name, product_data in self.products.items():
            product_obj = product_data['product_obj']
            amount = product_data['amount']
            discount_percent = product_data['discount_percent']

            price_after_premium = product_obj.price * self.PRICE_PREMIUM_FACTOR
            final_unit_price = price_after_premium * (1 - discount_percent / 100)

            all_products_info.append({
                'name': product_name,
                'type': product_obj.type,
                'amount': amount,
                'unit_price_with_premium_and_discount': round(final_unit_price, 2)
            })
        return all_products_info

    def get_product_info(self, product_name: str) -> tuple:
        if product_name not in self.products:
            raise CustomException(f"Продукту '{product_name}' немає в наявності.")
        product_data = self.products[product_name]
        return (product_name, product_data['amount'])

# --- ТЕСТУВАННЯ: має бути поза класами ---
if __name__ == "__main__":
    print("\n--- Тестування ProductStore ---")

    p = Product('Sport', 'Football T-Shirt', 100)
    p2 = Product('Food', 'Ramen', 1.5)

    s = ProductStore()
    s.add(p, 10)
    s.add(p2, 300)

    s.sell_product('Ramen', 10)
    assert s.get_product_info('Ramen') == ('Ramen', 290)
    print("✅ Продаж успішний. Дані актуальні.")

    # Інші перевірки та демонстрації...
    print("\nВсі тести пройшли успішно!")