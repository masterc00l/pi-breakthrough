"""
Pi Computation - Fixed Implementation
Benchmarking algorithms for 101 digits with focus on computational efficiency
"""

import decimal
from decimal import Decimal, getcontext
import time

# Use high precision
getcontext().prec = 120


def gauss_legendre(digits: int) -> Decimal:
    """
    Gauss-Legendre (Brent-Salamin) algorithm.
    O(n log² n) complexity - historically fastest for moderate digits.
    """
    getcontext().prec = digits + 20
    
    a = Decimal(1)
    b = Decimal(1) / Decimal(2).sqrt()
    t = Decimal(1) / Decimal(4)
    p = Decimal(1)
    
    while True:
        a_new = (a + b) / 2
        b_new = (a * b).sqrt()
        t_new = t - p * (a - a_new) * (a - a_new)
        
        if abs(a - b) < Decimal(10) ** (-digits):
            break
            
        a = a_new
        b = b_new
        t = t_new
        p = p * 2
    
    pi = (a + b) * (a + b) / (4 * t)
    return pi


def chudnovsky(digits: int) -> Decimal:
    """
    Chudnovsky Brothers' algorithm - FASTEST known for high precision.
    ~14 digits per term, O(n log³ n).
    """
    getcontext().prec = digits + 20
    
    total = Decimal(0)
    a = Decimal(13591409)
    b = Decimal(545140134)
    c = Decimal(640320)
    
    n_max = digits // 14 + 2
    
    for n in range(n_max):
        # Compute (6n)! / (n!^3 * (3n)!)
        # Using the product formula for efficiency
        term = Decimal(1)
        for k in range(1, n + 1):
            k = Decimal(k)
            numerator = (6*k-5)*(6*k-4)*(6*k-3)*(6*k-2)*(6*k-1)*(6*k)
            denominator = k*k*k * (3*k-2)*(3*k-1)*(3*k)
            term *= Decimal(numerator) / Decimal(denominator)
        
        # Add the term with coefficient
        coeff = a + b * Decimal(n)
        total += term * coeff / c ** (Decimal(3*n + 1.5))
        
        # Alternate sign
        if n % 2 == 1:
            total = -total
    
    pi = Decimal(12) * total
    return pi


def machin_like(digits: int) -> Decimal:
    """
    Machin-like formulas - very efficient for moderate digits.
    Uses arctan series.
    
    Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    """
    getcontext().prec = digits + 20
    
    def arctan(x: Decimal, digits: int) -> Decimal:
        """Compute arctan using Taylor series."""
        result = Decimal(0)
        term = x
        n = 0
        while abs(term) > Decimal(10) ** (-digits):
            result += term / Decimal(2*n + 1)
            term *= -x * x
            n += 1
        return result
    
    # Machin's formula
    pi_4 = 4 * arctan(Decimal(1)/Decimal(5), digits) - arctan(Decimal(1)/Decimal(239), digits)
    return pi_4 * 4


def BBP_formula(digits: int) -> Decimal:
    """
    BBP (Bailey-Borwein-Plouffe) formula.
    Can extract any digit without computing all preceding digits!
    HEXADECIMAL digits only.
    """
    getcontext().prec = digits + 20
    
    def sum_term(k: int) -> Decimal:
        # BBP formula: Σ 1/(16^k) * (4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6))
        k = Decimal(k)
        term = (
            Decimal(4) / (8*k + 1) -
            Decimal(2) / (8*k + 4) -
            Decimal(1) / (8*k + 5) -
            Decimal(1) / (8*k + 6)
        ) / (Decimal(16) ** k)
        return term
    
    total = Decimal(0)
    for k in range(digits // 2 + 5):
        total += sum_term(k)
    
    return total


def benchmark(func, digits: int, name: str) -> tuple:
    """Benchmark a Pi computation function."""
    start = time.time()
    result = func(digits)
    elapsed = time.time() - start
    
    result_str = str(result).replace('.', '')[:digits]
    expected = "1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480"
    
    # Count matching digits
    matches = 0
    for i in range(min(len(result_str), len(expected))):
        if result_str[i] == expected[i]:
            matches += 1
        else:
            break
    
    print(f"\n{name}:")
    print(f"  Time: {elapsed:.6f}s")
    print(f"  Correct digits: {matches}/101")
    print(f"  Result: {str(result)[:60]}...")
    
    return result, elapsed, matches


def main():
    print("="*60)
    print("Pi Computation Benchmark - Computing 101 Digits")
    print("="*60)
    
    methods = [
        (gauss_legendre, "Gauss-Legendre"),
        (chudnovsky, "Chudnovsky"),
        (machin_like, "Machin-like"),
    ]
    
    results = []
    for method, name in methods:
        try:
            result, elapsed, matches = benchmark(method, 101, name)
            results.append((name, elapsed, result, matches))
        except Exception as e:
            print(f"\n{name}: FAILED - {e}")
    
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    
    if results:
        # Sort by correctness then speed
        results.sort(key=lambda x: (-x[3], x[1]))
        
        print(f"\n🏆 FASTEST CORRECT:")
        best = results[0]
        print(f"  {best[0]}: {best[1]:.6f}s ({best[3]}/101 digits correct)")
        
        print(f"\nFull result ({best[0]}):")
        print(f"  {best[2]}")
        
        print(f"\n📊 Rankings (by correctness, then speed):")
        for i, (name, elapsed, _, matches) in enumerate(results, 1):
            print(f"  {i}. {name}: {elapsed:.6f}s ({matches}/101)")


if __name__ == "__main__":
    main()