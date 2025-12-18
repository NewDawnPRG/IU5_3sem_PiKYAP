#!/usr/bin/env python3
"""
Утилита для запуска всех тестов
"""

import subprocess
import sys
import os

def run_unittests():
    """Запуск TDD тестов (unittest)"""
    print("=" * 60)
    print("Запуск TDD тестов (unittest)")
    print("=" * 60)
    
    import unittest
    from test_equation_tdd import TestEquationSolverTDD
    
    # Создаем test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEquationSolverTDD)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_behave_tests():
    """Запуск BDD тестов (behave)"""
    print("\n" + "=" * 60)
    print("Запуск BDD тестов (behave)")
    print("=" * 60)
    
    try:
        # Запускаем behave через subprocess
        result = subprocess.run(
            ['behave', 'features/equation.feature', '--no-capture'],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("Ошибка: behave не установлен. Установите: pip install behave")
        return False

def main():
    """Основная функция запуска тестов"""
    print("Тестирование решения биквадратного уравнения")
    print("=" * 60)
    
    # Проверяем наличие необходимых модулей
    try:
        import behave
    except ImportError:
        print("Внимание: behave не установлен. BDD тесты пропущены.")
        print("Установите: pip install behave")
        behave_available = False
    else:
        behave_available = True
    
    # Запускаем TDD тесты
    tdd_success = run_unittests()
    
    # Запускаем BDD тесты если установлен behave
    bdd_success = True
    if behave_available:
        bdd_success = run_behave_tests()
    
    # Итоговый результат
    print("\n" + "=" * 60)
    print("ИТОГИ:")
    print("=" * 60)
    print(f"TDD тесты: {'ПРОЙДЕНЫ' if tdd_success else 'НЕ ПРОЙДЕНЫ'}")
    if behave_available:
        print(f"BDD тесты: {'ПРОЙДЕНЫ' if bdd_success else 'НЕ ПРОЙДЕНЫ'}")
    
    overall_success = tdd_success and (not behave_available or bdd_success)
    print(f"\nОбщий результат: {'ВСЕ ТЕСТЫ ПРОЙДЕНЫ' if overall_success else 'ТЕСТЫ НЕ ПРОЙДЕНЫ'}")
    
    sys.exit(0 if overall_success else 1)

if __name__ == '__main__':
    main()