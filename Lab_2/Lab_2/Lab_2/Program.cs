using System;
using System.Collections.Generic;

namespace BiquadraticEquationSolver
{
    class Program
    {
        static void Main(string[] args)
        {
            double a = GetCoef(1, "Введите коэффициент А (не равный нулю):", false, args);
            double b = GetCoef(2, "Введите коэффициент B:", true, args);
            double c = GetCoef(3, "Введите коэффициент C:", true, args);

            List<double> roots = GetRoots(a, b, c);

            int count = roots.Count;
            if (count == 0)
            {
                Console.WriteLine("Нет корней");
            }
            else if (count == 1)
            {
                Console.WriteLine("Один корень: {0}", roots[0]);
            }
            else if (count == 2)
            {
                Console.WriteLine("Два корня: {0} и {1}", roots[0], roots[1]);
            }
            else if (count == 3)
            {
                Console.WriteLine("Три корня: {0}, {1} и {2}", roots[0], roots[1], roots[2]);
            }
            else if (count == 4)
            {
                Console.WriteLine("Четыре корня: {0}, {1}, {2} и {3}", roots[0], roots[1], roots[2], roots[3]);
            }
            Console.ReadKey();
        }

        static double GetCoef(int index, string prompt, bool allowZero, string[] args)
        {
            bool triedCommandLine = false;
            while (true)
            {
                string coefStr;
                if (!triedCommandLine && (index - 1) < args.Length)
                {
                    coefStr = args[index - 1];
                    triedCommandLine = true;
                    Console.WriteLine(prompt);
                    Console.WriteLine($"Попытка использовать значение из командной строки: {coefStr}");
                }
                else
                {
                    Console.WriteLine(prompt);
                    coefStr = Console.ReadLine();
                }

                try
                {
                    double coef = double.Parse(coefStr);
                    if (!allowZero && coef == 0.0)
                    {
                        Console.WriteLine("Ошибка: коэффициент не может быть равен нулю. Попробуйте снова.");
                        continue;
                    }
                    return coef;
                }
                catch (FormatException)
                {
                    Console.WriteLine("Ошибка: введите действительное число. Попробуйте снова.");
                }
            }
        }

        static List<double> GetRoots(double a, double b, double c)
        {
            List<double> result = new List<double>();
            double discriminant = b * b - 4 * a * c;

            if (discriminant == 0.0)
            {
                double y = -b / (2.0 * a);
                if (y > 0.0)
                {
                    result.Add(Math.Sqrt(y));
                    result.Add(-Math.Sqrt(y));
                }
                else if (y == 0.0)
                {
                    result.Add(0.0);
                }
            }
            else if (discriminant > 0.0)
            {
                double sqrtDiscriminant = Math.Sqrt(discriminant);
                double y1 = (-b + sqrtDiscriminant) / (2.0 * a);
                double y2 = (-b - sqrtDiscriminant) / (2.0 * a);

                if (y1 > 0.0)
                {
                    result.Add(Math.Sqrt(y1));
                    result.Add(-Math.Sqrt(y1));
                }
                else if (y1 == 0.0)
                {
                    result.Add(0.0);
                }

                if (y2 > 0.0)
                {
                    result.Add(Math.Sqrt(y2));
                    result.Add(-Math.Sqrt(y2));
                }
                else if (y2 == 0.0 && y1 != 0.0)
                {
                    result.Add(0.0);
                }
            }

            return result;
        }
    }
}