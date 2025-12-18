import unittest
import math
from equation_solver import EquationSolver

class TestEquationSolverTDD(unittest.TestCase):
    """TDD тесты для решения биквадратного уравнения"""
    
    def test_no_real_roots(self):
        """Тест: уравнение не имеет действительных корней"""
        # Уравнение: x^4 + 2x^2 + 5 = 0
        roots = EquationSolver.solve_biquadratic(1, 2, 5)
        self.assertEqual(len(roots), 0)
    
    def test_four_real_roots(self):
        """Тест: уравнение имеет 4 действительных корня"""
        # Уравнение: x^4 - 5x^2 + 4 = 0
        # Корни: -2, -1, 1, 2
        roots = EquationSolver.solve_biquadratic(1, -5, 4)
        self.assertEqual(len(roots), 4)
        
        expected_roots = [-2, -1, 1, 2]
        for expected, actual in zip(expected_roots, roots):
            self.assertAlmostEqual(expected, actual, places=10)
    
    def test_one_root_zero(self):
        """Тест: уравнение имеет один корень x=0"""
        # Уравнение: x^4 + 2x^2 = 0
        roots = EquationSolver.solve_biquadratic(1, 2, 0)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], 0.0, places=10)
    
    def test_two_real_roots(self):
        """Тест: уравнение имеет 2 действительных корня"""
        # Уравнение: x^4 - 4x^2 = 0
        # Корни: -2, 2
        roots = EquationSolver.solve_biquadratic(1, -4, 0)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], -2.0, places=10)
        self.assertAlmostEqual(roots[1], 2.0, places=10)
    
    def test_three_real_roots(self):
        """Тест: уравнение имеет 3 действительных корня"""
        # Уравнение: x^4 - x^2 = 0
        # Корни: -1, 0, 1
        roots = EquationSolver.solve_biquadratic(1, -1, 0)
        self.assertEqual(len(roots), 3)
        expected_roots = [-1, 0, 1]
        for expected, actual in zip(expected_roots, roots):
            self.assertAlmostEqual(expected, actual, places=10)
    
    def test_coefficient_a_zero_raises_error(self):
        """Тест: коэффициент a=0 вызывает исключение"""
        with self.assertRaises(ValueError) as context:
            EquationSolver.solve_biquadratic(0, 2, 3)
        self.assertIn("не может быть равен нулю", str(context.exception))
    
    def test_double_root(self):
        """Тест: уравнение с кратными корнями"""
        # Уравнение: x^4 - 2x^2 + 1 = 0
        # Корни: -1, 1 (каждый корень кратности 2)
        roots = EquationSolver.solve_biquadratic(1, -2, 1)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], -1.0, places=10)
        self.assertAlmostEqual(roots[1], 1.0, places=10)
    
    def test_validation_valid_coefficients(self):
        """Тест: валидация корректных коэффициентов"""
        valid, message = EquationSolver.validate_coefficients(1, 2, 3)
        self.assertTrue(valid)
        self.assertEqual(message, "")
    
    def test_validation_invalid_coefficients(self):
        """Тест: валидация некорректных коэффициентов"""
        # a = 0
        valid, message = EquationSolver.validate_coefficients(0, 2, 3)
        self.assertFalse(valid)
        self.assertIn("не может быть равен нулю", message)
        
        # NaN
        valid, message = EquationSolver.validate_coefficients(float('nan'), 2, 3)
        self.assertFalse(valid)
        self.assertIn("NaN", message)


if __name__ == '__main__':
    unittest.main()