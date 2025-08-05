from typing import Union

class Product:
    """
    Представляє окремий продукт з типом, назвою та базовою ціною.
    """

    def __init__(self, type: str, name: str, price: float):
        """
        Ініціалізує новий продукт.

        Аргументи:
            type (str): Тип продукту (наприклад, 'Sport', 'Food').
            name (str): Назва продукту (наприклад, 'Football T-Shirt').
            price (float): Базова ціна продукту (до націнки магазину).
        """
        if not isinstance(type, str) or not type:
            raise ValueError("Тип продукту має бути непорожнім рядком.")
        if not isinstance(name, str) or not name:
            raise ValueError("Назва продукту має бути непорожнім рядком.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Ціна продукту має бути додатним числом.")

        self.type = type
        self.name = name
        self.price = price  # Базова ціна

    def __repr__(self):
        """Повертає строкове представлення об'єкта Product."""
        return f"Product(type='{self.type}', name='{self.name}', price={self.price})"


class ProductStore:
    """
    Магазин, який управляє продуктами, їх кількістю, знижками та доходом.
    """
    # Преміум націнка для всіх продуктів у магазині (30%)
    PRICE_PREMIUM_FACTOR = 1.30

    def __init__(self):
        """
        Ініціалізує ProductStore з порожнім асортиментом та нульовим доходом.
        self.products: словник, де ключ - назва продукту,
                       значення - словник з {'product_obj': Product, 'amount': int, 'discount_percent': float}
        """
        self.products = {}  # Агрегація/композиція: ProductStore містить об'єкти Product
        self.income = 0.0

    def add(self, product: Product, amount: int):
        """
        Додає вказану кількість продукту до магазину.
        Застосовує націнку магазину до ціни продукту.

        Аргументи:
            product (Product): Об'єкт продукту, який потрібно додати.
            amount (int): Кількість продукту.
        """
        if not isinstance(product, Product):
            raise ValueError("Додавати можна лише об'єкти класу Product.")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Кількість продукту має бути додатним цілим числом.")

        if product.name in self.products:
            # Якщо продукт вже є, просто оновлюємо кількість
            self.products[product.name]['amount'] += amount
            print(
                f"Додано {amount} одиниць '{product.name}'. Загальна кількість: {self.products[product.name]['amount']}")
        else:
            # Якщо продукт новий, додаємо його з початковою знижкою 0%
            self.products[product.name] = {
                'product_obj': product,
                'amount': amount,
                'discount_percent': 0.0
            }
            print(f"Додано новий продукт '{product.name}' ({amount} одиниць).")

    def set_discount(self, identifier: Union[str, int], percent: Union[int, float], identifier_type: str = 'name'):
        """
        Встановлює знижку для продуктів за назвою або типом.

        Аргументи:
            identifier (str | int): Назва продукту (якщо identifier_type='name')
                                    або тип продукту (якщо identifier_type='type').
            percent (int | float): Розмір знижки у відсотках (від 0 до 100).
            identifier_type (str): Тип ідентифікатора ('name' або 'type').
        """
        if not (0 <= percent <= 100):
            raise ValueError("Відсоток знижки має бути від 0 до 100.")
        if identifier_type not in ['name', 'type']:
            raise ValueError("identifier_type має бути 'name' або 'type'.")

        found_match = False
        for product_data in self.products.values():
            product_obj = product_data['product_obj']

            if identifier_type == 'name' and product_obj.name == identifier:
                product_data['discount_percent'] = percent
                found_match = True
                print(f"Встановлено знижку {percent}% для продукту '{identifier}'.")
            elif identifier_type == 'type' and product_obj.type == identifier:
                product_data['discount_percent'] = percent
                found_match = True
                print(f"Встановлено знижку {percent}% для продуктів типу '{identifier}'.")

        if not found_match:
            raise ValueError(
                f"Продукт(и) з ідентифікатором '{identifier}' (тип: {identifier_type}) не знайдено для встановлення знижки.")

    def sell_product(self, product_name: str, amount: int):
        """
        Продає вказану кількість продукту зі складу.
        Збільшує дохід магазину.

        Аргументи:
            product_name (str): Назва продукту для продажу.
            amount (int): Кількість одиниць для продажу.
        """
        if not isinstance(product_name, str) or not product_name:
            raise ValueError("Назва продукту має бути непорожнім рядком.")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Кількість для продажу має бути додатним цілим числом.")

        if product_name not in self.products:
            raise ValueError(f"Продукту '{product_name}' немає в наявності.")

        product_data = self.products[product_name]
        current_amount = product_data['amount']
        product_obj = product_data['product_obj']
        discount_percent = product_data['discount_percent']

        if current_amount < amount:
            raise ValueError(f"Недостатньо '{product_name}' на складі. Доступно: {current_amount}, запитано: {amount}.")

        # Обчислення ціни продажу за одиницю
        # Базова ціна -> Ціна з націнкою -> Ціна зі знижкою
        price_after_premium = product_obj.price * self.PRICE_PREMIUM_FACTOR
        final_unit_price = price_after_premium * (1 - discount_percent / 100)

        # Оновлення кількості та доходу
        product_data['amount'] -= amount
        self.income += final_unit_price * amount
        print(f"Продано {amount} одиниць '{product_name}' за {final_unit_price:.2f} за одиницю. Дохід збільшено.")

    def get_income(self) -> float:
        """
        Повертає загальний дохід магазину.
        """
        return self.income

    def get_all_products(self) -> list:
        """
        Повертає інформацію про всі доступні продукти в магазині.

        Повертає:
            list: Список словників, кожен з яких містить інформацію
                  про продукт (назва, тип, кількість, ціна з націнкою та знижкою).
        """
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
        """
        Повертає кортеж з назвою продукту та його кількістю на складі.

        Аргументи:
            product_name (str): Назва продукту.

        Повертає:
            tuple: Кортеж (назва продукту, кількість).

        Викликає:
            ValueError: Якщо продукт не знайдено.
        """
        if product_name not in self.products:
            raise ValueError(f"Продукту '{product_name}' немає в наявності.")

        product_data = self.products[product_name]
        return (product_name, product_data['amount'])


# --- Демонстрація та перевірки ---
from typing import Union

print("--- Демонстрація класів Product та ProductStore ---")

# Створення продуктів
p = Product('Sport', 'Football T-Shirt', 100)
p2 = Product('Food', 'Ramen', 1.5)
p3 = Product('Sport', 'Basketball', 50)
p4 = Product('Electronics', 'Headphones', 200)

# Створення магазину
s = ProductStore()
print("\nМагазин створено.")

# Додавання продуктів
print("\n--- Додавання продуктів ---")
s.add(p, 10)  # Football T-Shirt: 100 * 1.3 = 130 за шт.
s.add(p2, 300)  # Ramen: 1.5 * 1.3 = 1.95 за шт.
s.add(p3, 5)  # Basketball: 50 * 1.3 = 65 за шт.
s.add(p4, 20)  # Headphones: 200 * 1.3 = 260 за шт.

# Перевірка get_product_info перед продажем
print("\n--- Перевірка get_product_info перед продажем ---")
assert s.get_product_info('Ramen') == ('Ramen', 300)
print(f"Інформація про Ramen: {s.get_product_info('Ramen')}")

# Продаж продукту
print("\n--- Продаж продуктів ---")
s.sell_product('Ramen', 10)  # Продаємо 10 Ramen
assert s.get_product_info('Ramen') == ('Ramen', 290)
print(f"Інформація про Ramen після продажу: {s.get_product_info('Ramen')}")
print(f"Поточний дохід магазину: {s.get_income():.2f}")  # Очікується: 1.95 * 10 = 19.50

# Спроба продати більше, ніж є
try:
    s.sell_product('Football T-Shirt', 100)
except ValueError as e:
    print(f"Успішно перехоплено помилку: {e}")  # Очікується: Недостатньо 'Football T-Shirt' на складі.

# Спроба продати неіснуючий продукт
try:
    s.sell_product('NonExistentProduct', 1)
except ValueError as e:
    print(f"Успішно перехоплено помилку: {e}")  # Очікується: Продукту 'NonExistentProduct' немає в наявності.

# Встановлення знижок
print("\n--- Встановлення знижок ---")
s.set_discount('Football T-Shirt', 10)  # Знижка 10% на Football T-Shirt
s.set_discount('Sport', 20, identifier_type='type')  # Знижка 20% на всі продукти типу 'Sport'
# Це перезапише 10% для Football T-Shirt

# Продаж продукту зі знижкою
print("\n--- Продаж продуктів зі знижкою ---")
# Football T-Shirt: 100 (базова) * 1.3 (націнка) * (1 - 0.20) (знижка) = 130 * 0.8 = 104 за шт.
s.sell_product('Football T-Shirt', 5)
print(f"Поточний дохід магазину: {s.get_income():.2f}")  # Очікується: 19.50 + 104 * 5 = 19.50 + 520 = 539.50

# Basketball: 50 (базова) * 1.3 (націнка) * (1 - 0.20) (знижка) = 65 * 0.8 = 52 за шт.
s.sell_product('Basketball', 2)
print(f"Поточний дохід магазину: {s.get_income():.2f}")  # Очікується: 539.50 + 52 * 2 = 539.50 + 104 = 643.50

# Спроба встановити знижку на неіснуючий ідентифікатор
try:
    s.set_discount('InvalidType', 5, identifier_type='type')
except ValueError as e:
    print(f"Успішно перехоплено помилку: {e}")

# Отримання інформації про всі продукти
print("\n--- Інформація про всі продукти ---")
all_products = s.get_all_products()
for prod in all_products:
    print(prod)

# Перевірка кінцевого доходу
print(f"\nКінцевий дохід магазину: {s.get_income():.2f}")

print("\nВсі тести пройшли успішно!")
