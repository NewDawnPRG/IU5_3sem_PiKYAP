import unittest
from main import (
    build_one_to_many,
    build_many_to_many,
    get_drivers_with_surname_ending_ow,
    get_garages_with_avg_salary,
    get_garages_starting_with_a,
    Garage,
    Driver,
    DriverGarage
)

class TestControlWork(unittest.TestCase):
    """Тесты для рубежного контроля №1"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.garages = [
            Garage(1, "Альфа-парк"),
            Garage(2, "Бета-парк"),
            Garage(3, "Альтернативный автопарк")
        ]
        self.drivers = [
            Driver(1, "Иванов", 30000, 1),
            Driver(2, "Петров", 40000, 1),
            Driver(3, "Смирнов", 50000, 2),
            Driver(4, "Медведев", 35000, 3),
            Driver(5, "Овчинников", 45000, 3)
        ]
        self.drivers_garages = [
            DriverGarage(1, 1),
            DriverGarage(2, 1),
            DriverGarage(3, 2),
            DriverGarage(4, 3),
            DriverGarage(5, 3),
            DriverGarage(1, 3)  # Иванов работает в двух парках
        ]

    def test_drivers_surname_ending_ow(self):
        """Тест Д1: Фамилии, оканчивающиеся на 'ов'"""
        one_to_many = build_one_to_many(self.garages, self.drivers)
        result = get_drivers_with_surname_ending_ow(one_to_many)
        
        # Все водители, чьи фамилии заканчиваются на "ов":
        # Иванов, Петров, Смирнов, Овчинников
        expected = [
            ("Иванов", "Альфа-парк"),
            ("Овчинников", "Альтернативный автопарк"),
            ("Петров", "Альфа-парк"),
            ("Смирнов", "Бета-парк")
        ]
        
        # Сортировка по фамилии, затем по названию автопарка
        self.assertEqual(result, expected)

    def test_garages_avg_salary(self):
        """Тест Д2: Средняя зарплата по автопаркам"""
        one_to_many = build_one_to_many(self.garages, self.drivers)
        result = get_garages_with_avg_salary(self.garages, one_to_many)
        
        # Расчет:
        # Альфа-парк: (30000 + 40000) / 2 = 35000.0
        # Альтернативный автопарк: (35000 + 45000) / 2 = 40000.0
        # Бета-парк: 50000.0
        expected = [
            ("Альфа-парк", 35000.0),
            ("Альтернативный автопарк", 40000.0),
            ("Бета-парк", 50000.0)
        ]
        
        self.assertEqual(result, expected)

    def test_garages_starting_with_a(self):
        """Тест Д3: Автопарки, начинающиеся на 'А'"""
        many_to_many = build_many_to_many(
            self.garages, 
            self.drivers, 
            self.drivers_garages
        )
        result = get_garages_starting_with_a(self.garages, many_to_many)
        
        # Для Альфа-парка: Иванов, Петров (отсортированы по алфавиту)
        # Для Альтернативного автопарка: Иванов, Медведев, Овчинников (отсортированы)
        expected = {
            "Альфа-парк": ["Иванов", "Петров"],
            "Альтернативный автопарк": ["Иванов", "Медведев", "Овчинников"]
        }
        
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()