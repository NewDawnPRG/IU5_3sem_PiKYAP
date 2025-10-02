import sys
import math

def get_coef(index, prompt, allow_zero):
    while True:
        try:
            coef_str = sys.argv[index]
            print(prompt)
            print(f"Попытка использовать значение из командной строки: {coef_str}")
        except:
            print(prompt)
            coef_str = input()
        try:
            coef = float(coef_str)
            if not allow_zero and coef == 0.0:
                print("Ошибка: коэффициент не может быть равен нулю. Попробуйте снова.")
                continue
            return coef
        except ValueError:
            print("Ошибка: введите действительное число. Попробуйте снова.")


def get_roots(a, b, c):
    result = []
    D = b**2 - 4*a*c
    
    if D == 0.0:
        y = -b / (2.0*a)
        if y > 0.0:
            root1 = math.sqrt(y)
            root2 = -math.sqrt(y)
            result.append(root1)
            result.append(root2)
        elif y == 0.0:
            result.append(0.0)
    elif D > 0.0:
        sqD = math.sqrt(D)
        y1 = (-b + sqD) / (2.0*a)
        y2 = (-b - sqD) / (2.0*a)
        
        if y1 > 0.0:
            root1 = math.sqrt(y1)
            root2 = -math.sqrt(y1)
            result.append(root1)
            result.append(root2)
        elif y1 == 0.0:
            result.append(0.0)
            
        if y2 > 0.0:
            root3 = math.sqrt(y2)
            root4 = -math.sqrt(y2)
            result.append(root3)
            result.append(root4)
        elif y2 == 0.0 and y1 != 0.0:
            result.append(0.0)
    
    return result


def main():
    a = get_coef(1, 'Введите коэффициент А (не равный нулю):', allow_zero=False)
    b = get_coef(2, 'Введите коэффициент B:', allow_zero=True)
    c = get_coef(3, 'Введите коэффициент C:', allow_zero=True)

    roots = get_roots(a,b,c)

    len_roots = len(roots)
    if len_roots == 0:
        print('Нет корней')
    elif len_roots == 1:
        print('Один корень: {}'.format(roots[0]))
    elif len_roots == 2:
        print('Два корня: {} и {}'.format(roots[0], roots[1]))
    elif len_roots == 3:
        print('Три корня: {}, {} и {}'.format(roots[0], roots[1], roots[2]))
    elif len_roots == 4:
        print('Четыре корня: {}, {}, {} и {}'.format(roots[0], roots[1], roots[2], roots[3]))
    

if __name__ == "__main__":
    main()
