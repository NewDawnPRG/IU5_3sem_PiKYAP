import math
from typing import List, Tuple

class EquationSolver:
    @staticmethod
    def solve_biquadratic(a: float, b: float, c: float) -> List[float]:
        if abs(a) < 1e-10:
            raise ValueError("Коэффициент 'a' не может быть равен нулю")

        discriminant = b**2 - 4*a*c
        
        roots = []
        
        if discriminant < -1e-10:
            return []
        
        if abs(discriminant) < 1e-10:
            y = -b / (2*a)
            roots.extend(EquationSolver._get_roots_from_y(y))
        
        else:
            sqrt_d = math.sqrt(discriminant)
            y1 = (-b + sqrt_d) / (2*a)
            y2 = (-b - sqrt_d) / (2*a)
            
            roots.extend(EquationSolver._get_roots_from_y(y1))
            roots.extend(EquationSolver._get_roots_from_y(y2))
        
        unique_roots = EquationSolver._remove_duplicates(sorted(roots))
        
        return unique_roots
    
    @staticmethod
    def _get_roots_from_y(y: float) -> List[float]:
        roots = []
        
        if abs(y) < 1e-10:
            roots.append(0.0)
        elif y > 0: 
            sqrt_y = math.sqrt(y)
            roots.append(sqrt_y)
            roots.append(-sqrt_y)
        
        return roots
    
    @staticmethod
    def _remove_duplicates(numbers: List[float], tolerance: float = 1e-10) -> List[float]:
        if not numbers:
            return []
        
        unique = [numbers[0]]
        for num in numbers[1:]:
            if abs(num - unique[-1]) > tolerance:
                unique.append(num)
        
        return unique
    
    @staticmethod
    def validate_coefficients(a: float, b: float, c: float) -> Tuple[bool, str]:
        if math.isnan(a) or math.isnan(b) or math.isnan(c):
            return False, "Коэффициенты не могут быть NaN"
        
        if math.isinf(a) or math.isinf(b) or math.isinf(c):
            return False, "Коэффициенты не могут быть бесконечными"
        
        if abs(a) < 1e-10:
            return False, "Коэффициент 'a' не может быть равен нулю"
        
        return True, ""