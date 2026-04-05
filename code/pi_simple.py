"""
Simple Pi Benchmark for 101 digits
"""

import decimal
from decimal import Decimal, getcontext
import time

getcontext().prec = 120


def gauss_legendre(digits):
    """Gauss-Legendre (Brent-Salamin) - FAST for 101 digits"""
    getcontext().prec = digits + 20
    
    a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
    
    while abs(a - b) > Decimal(10) ** (-digits):
        a, b, t, p = (a + b) / 2, (a * b).sqrt(), t - p * (a - (a + b) / 2) ** 2, p * 2
    
    return ((a + b) ** 2) / (4 * t)


def chudnovsky(digits):
    """Chudnovsky Brothers - Very efficient"""
    getcontext().prec = digits + 20
    
    total = Decimal(0)
    for n in range(digits // 14 + 3):
        # Simplified Chudnovsky
        n_dec = Decimal(n)
        num = 1
        for k in range(1, n + 1):
            k = Decimal(k)
            num *= (6*k-5)*(6*k-4)*(6*k-3)*(6*k-2)*(6*k-1)*(6*k) / (k**3 * (3*k-2)*(3*k-1)*(3*k))
        
        total += num * (13591409 + 545140134*n_dec) / Decimal(640320) ** (3*n_dec + 1.5)
    
    return Decimal(12) * total * Decimal(640320) ** Decimal(0.5)


def main():
    print("Computing 101 digits of Pi...\n")
    
    # Test Gauss-Legendre
    start = time.time()
    pi1 = gauss_legendre(101)
    t1 = time.time() - start
    print(f"Gauss-Legendre: {t1:.6f}s")
    print(f"Result: {str(pi1)[:105]}...\n")
    
    # Test Chudnovsky  
    start = time.time()
    pi2 = chudnovsky(101)
    t2 = time.time() - start
    print(f"Chudnovsky: {t2:.6f}s")
    print(f"Result: {str(pi2)[:105]}...\n")
    
    # Compare results
    print("Results match:", str(pi1)[:50] == str(pi2)[:50])
    print(f"\n✅ Fastest: {'Gauss-Legendre' if t1 < t2 else 'Chudnovsky'}")
    print(f"Time: {min(t1, t2):.6f}s for 101 digits")


if __name__ == "__main__":
    main()