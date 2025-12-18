from behave import given, when, then, step
import math
from equation_solver import EquationSolver

@given('биквадратное уравнение с коэффициентами a={a}, b={b}, c={c}')
def step_given_equation_with_coefficients(context, a, b, c):
    """Задает коэффициенты уравнения"""
    context.a = float(a)
    context.b = float(b)
    context.c = float(c)

@when('я решаю уравнение')
def step_when_solve_equation(context):
    """Решает уравнение и сохраняет результат"""
    try:
        context.roots = EquationSolver.solve_biquadratic(
            context.a, context.b, context.c
        )
        context.error = None
    except Exception as e:
        context.error = str(e)
        context.roots = []

@when('я пытаюсь решить уравнение')
def step_when_try_solve_equation(context):
    """Пытается решить уравнение (ожидается возможная ошибка)"""
    step_when_solve_equation(context)

@then('я получаю {expected_count} действительных корней')
def step_then_get_roots_count(context, expected_count):
    """Проверяет количество корней"""
    expected = int(expected_count)
    actual = len(context.roots)
    assert actual == expected, (
        f"Ожидалось {expected} корней, но получено {actual}. "
        f"Корни: {context.roots}"
    )

@then('я получаю ошибку "{expected_error}"')
def step_then_get_error(context, expected_error):
    """Проверяет, что получена ожидаемая ошибка"""
    assert context.error is not None, "Ошибка не была вызвана"
    assert expected_error in context.error, (
        f"Ожидалась ошибка содержащая '{expected_error}', "
        f"но получено: '{context.error}'"
    )

@then('корни равны {expected_roots} с точностью {tolerance}')
def step_then_roots_equal(context, expected_roots, tolerance):
    """Проверяет значения корней с заданной точностью"""
    # Преобразуем строку с корнями в список чисел
    import ast
    expected = ast.literal_eval(expected_roots)
    tol = float(tolerance)
    
    assert len(context.roots) == len(expected), (
        f"Количество корней не совпадает: "
        f"ожидалось {len(expected)}, получено {len(context.roots)}"
    )
    
    # Сортируем корни для сравнения
    actual_sorted = sorted(context.roots)
    expected_sorted = sorted(expected)
    
    for i, (actual, expected_val) in enumerate(zip(actual_sorted, expected_sorted)):
        assert math.isclose(actual, expected_val, abs_tol=tol), (
            f"Корень #{i+1}: ожидалось {expected_val}, "
            f"получено {actual}, разница {abs(actual - expected_val)}"
        )

@then('корень равен {expected_value} с точностью {tolerance}')
def step_then_root_equals(context, expected_value, tolerance):
    """Проверяет значение единственного корня"""
    expected = float(expected_value)
    tol = float(tolerance)
    
    assert len(context.roots) == 1, f"Ожидался 1 корень, получено {len(context.roots)}"
    assert math.isclose(context.roots[0], expected, abs_tol=tol), (
        f"Корень: ожидался {expected}, "
        f"получен {context.roots[0]}"
    )