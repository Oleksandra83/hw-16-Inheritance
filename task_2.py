class Person:
    """
    Базовий клас, що представляє будь-яку особу у школі.
    Містить спільні атрибути та методи.
    """
    def __init__(self, name: str, age: int, gender: str):
        """
        Ініціалізує об'єкт Person.

        Аргументи:
            name (str): Повне ім'я особи.
            age (int): Вік особи.
            gender (str): Стать особи.
        """
        self.name = name
        self.age = age
        self.gender = gender

    def introduce(self) -> str:
        """
        Повертає рядок із представленням особи.
        """
        return f"Привіт, мене звати {self.name}, мені {self.age} років."

    def get_details(self) -> dict:
        """
        Повертає словник з основними деталями особи.
        """
        return {"Name": self.name, "Age": self.age, "Gender": self.gender}

class Student(Person):
    """
    Клас, що представляє учня у школі.
    Успадковує від класу Person та додає специфічні атрибути та методи.
    """
    def __init__(self, name: str, age: int, gender: str, student_id: str, grade_level: int):
        """
        Ініціалізує об'єкт Student.

        Аргументи:
            name (str): Повне ім'я учня.
            age (int): Вік учня.
            gender (str): Стать учня.
            student_id (str): Унікальний ідентифікатор учня.
            grade_level (int): Клас, у якому навчається учень.
        """
        # Викликаємо конструктор батьківського класу (Person)
        super().__init__(name, age, gender)
        self.student_id = student_id
        self.grade_level = grade_level
        self.courses = [] # Список курсів, на які записаний студент
        self.grades = {}  # Додано: словник для зберігання оцінок (курс -> оцінка)

    def enroll_course(self, course_name: str):
        """
        Записує студента на курс.
        """
        if course_name not in self.courses:
            self.courses.append(course_name)
            print(f"{self.name} записано на курс '{course_name}'.")
        else:
            print(f"{self.name} вже записаний на курс '{course_name}'.")

    def list_courses(self) -> list:
        """
        Повертає список курсів, на які записаний студент.
        """
        return self.courses

    def introduce(self) -> str:
        """
        Перевизначає метод introduce для додавання специфічної інформації про студента.
        """
        return f"{super().introduce()} Я учень {self.grade_level}-го класу, мій ID: {self.student_id}."

class Teacher(Person):
    """
    Клас, що представляє вчителя у школі.
    Успадковує від класу Person та додає специфічні атрибути та методи.
    """
    def __init__(self, name: str, age: int, gender: str, employee_id: str, subject: str, salary: float):
        """
        Ініціалізує об'єкт Teacher.

        Аргументи:
            name (str): Повне ім'я вчителя.
            age (int): Вік вчителя.
            gender (str): Стать вчителя.
            employee_id (str): Унікальний ідентифікатор працівника.
            subject (str): Предмет, який викладає вчитель.
            salary (float): Зарплата вчителя.
        """
        # Викликаємо конструктор батьківського класу (Person)
        super().__init__(name, age, gender)
        self.employee_id = employee_id
        self.subject = subject
        self.salary = salary
        self.classes_taught = [] # Список класів, які викладає вчитель

    def assign_grade(self, student: Student, course: str, grade: str):
        """
        Призначає оцінку студенту за певний курс.
        Оцінка зберігається у словнику grades студента.
        """
        if course in student.courses:
            student.grades[course] = grade # Зберігаємо оцінку у словнику grades студента
            print(f"{self.name} поставив оцінку '{grade}' студенту {student.name} за курс '{course}'.")
        else:
            print(f"Помилка: Студент {student.name} не записаний на курс '{course}'.")

    def add_class_taught(self, class_name: str):
        """
        Додає клас до списку класів, які викладає вчитель.
        """
        if class_name not in self.classes_taught:
            self.classes_taught.append(class_name)
            print(f"{self.name} тепер викладає у класі '{class_name}'.")
        else:
            print(f"{self.name} вже викладає у класі '{class_name}'.")

    def introduce(self) -> str:
        """
        Перевизначає метод introduce для додавання специфічної інформації про вчителя.
        """
        return f"{super().introduce()} Я викладач {self.subject}, мій ID: {self.employee_id}."

# --- Додано новий клас Mathematician ---
class Mathematician:
    """
    Допоміжний клас для виконання математичних операцій зі списками чисел.
    """
    def square_nums(self, nums: list) -> list:
        """
        Приймає список цілих чисел і повертає список їхніх квадратів.
        """
        return list(map(lambda x: x ** 2, nums))

    def remove_positives(self, nums: list) -> list:
        """
        Приймає список цілих чисел і повертає його без додатних чисел.
        """
        return [num for num in nums if num <= 0] # Включає нуль, якщо він є

    def filter_leaps(self, dates: list) -> list:
        """
        Приймає список років (цілих чисел) і повертає лише ті, що є високосними.
        Рік є високосним, якщо:
        - ділиться на 4, АЛЕ
        - не ділиться на 100, АБО
        - ділиться на 400.
        """
        leap_years = []
        for year in dates:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                leap_years.append(year)
        return leap_years


# --- Демонстрація використання класів ---
print("--- Демонстрація класів: Person, Student, Teacher ---")

# Створення об'єкта Person
print("\n--- Об'єкт Person ---")
person1 = Person("Олена Коваль", 35, "Жінка")
print(person1.introduce())
print(f"Деталі: {person1.get_details()}")

# Створення об'єкта Student
print("\n--- Об'єкт Student ---")
student1 = Student("Іван Сидоренко", 16, "Чоловік", "S001", 10)
print(student1.introduce())
student1.enroll_course("Математика")
student1.enroll_course("Історія України")
student1.enroll_course("Математика") # Спроба записатися на той самий курс
print(f"Курси {student1.name}: {student1.list_courses()}")
print(f"Вік {student1.name}: {student1.age}") # Доступ до успадкованого атрибута

# Створення об'єкта Teacher
print("\n--- Об'єкт Teacher ---")
teacher1 = Teacher("Марія Іванова", 40, "Жінка", "T005", "Фізика", 2500.00)
print(teacher1.introduce())
print(f"Зарплата {teacher1.name}: {teacher1.salary}") # Доступ до специфічного атрибута
teacher1.add_class_taught("10-А")
teacher1.add_class_taught("11-Б")

# Призначаємо оцінку студенту
teacher1.assign_grade(student1, "Математика", "Відмінно")
teacher1.assign_grade(student1, "Хімія", "Добре") # Студент не записаний на цей курс

# Перевіряємо оцінки студента
print(f"Оцінки {student1.name}: {student1.grades}") # {'Математика': 'Відмінно'}

# --- Демонстрація класу Mathematician ---
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
