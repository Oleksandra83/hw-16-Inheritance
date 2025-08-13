class Mathematician:

    def square_nums(self, nums: list) -> list:

        return list(map(lambda x: x ** 2, nums))

    def remove_positives(self, nums: list) -> list:

        return [num for num in nums if num <= 0] # Включає нуль, якщо він є

    def filter_leaps(self, dates: list) -> list:

        leap_years = []
        for year in dates:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                leap_years.append(year)
        return leap_years


print("\n--- Демонстрація класу Mathematician ---")
m = Mathematician()

# Перевірка square_nums
nums_to_square = [7, 11, 5, 4]
squared_result = m.square_nums(nums_to_square)
print(f"Квадрати чисел {nums_to_square}: {squared_result}")
assert squared_result == [49, 121, 25, 16]

# Перевірка remove_positives
nums_to_filter = [26, -11, -8, 13, -90]
filtered_result = m.remove_positives(nums_to_filter)
print(f"Числа без додатних {nums_to_filter}: {filtered_result}")
assert filtered_result == [-11, -8, -90]

# Перевірка filter_leaps
years_to_check = [2001, 1884, 1995, 2003, 2020]
leap_years_result = m.filter_leaps(years_to_check)
print(f"Високосні роки з {years_to_check}: {leap_years_result}")
assert leap_years_result == [1884, 2020]

print("\nВсі демонстрації класів пройшли успішно!")
