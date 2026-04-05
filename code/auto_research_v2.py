"""
Auto-Research Pi Optimization v2
More aggressive mutations + proper accuracy check
"""

import random
import time
from decimal import Decimal, getcontext

getcontext().prec = 120

# Known correct 101 digits of Pi
CORRECT_PI = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480"

def check_correct(result, target_digits=101):
    """Check if result matches correct digits"""
    result_str = str(result).replace('.', '')[:target_digits]
    return result_str == CORRECT_PI[:target_digits]

def gauss_legendre(digits):
    """Baseline Gauss-Legendre"""
    a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
    for _ in range(30):
        a, b, t, p = (a + b) / 2, (a * b).sqrt(), t - p * (a - (a + b) / 2) ** 2, p * 2
    return ((a + b) ** 2) / (4 * t)

# Get baseline
times = [time.time() for _ in range(10)]
for _ in range(10):
    result = gauss_legendre(101)
baseline_time = min(times)
print(f"Baseline: {baseline_time*1000:.4f}ms, Correct: {check_correct(result)}")

# Try many algorithmic variants
def test_variant(variant_name, func, runs=5):
    """Test a variant multiple times"""
    valid_times = []
    for _ in range(runs):
        start = time.time()
        try:
            result = func(101)
            elapsed = time.time() - start
            if check_correct(result):
                valid_times.append(elapsed)
        except:
            pass
    return min(valid_times) if valid_times else None

# Define variants - different ways to compute the same thing
variants = {
    "baseline_gl": lambda d: gauss_legendre(d),
    
    # Different iteration counts
    "gl_20it": lambda d: (lambda a,b,t,p: ((a+b)**2)/(4*t))(
        *[Decimal(1), Decimal(1)/Decimal(2).sqrt(), Decimal(1)/Decimal(4), Decimal(1)] +
        [((a+b)/2, (a*b).sqrt(), t-p*(a-(a+b)/2)**2, p*2) for _ in range(20)]
    ),
    
    # Different order of operations
    "gl_sqrt_first": lambda d: (
        lambda a,b,t,p: ((a+b)**2)/(4*t))(
            Decimal(1), 
            (Decimal(1) * Decimal(1)/Decimal(2).sqrt()).sqrt(),  # nested sqrt
            Decimal(1)/Decimal(4), 
            Decimal(1)
        )
    ),
    
    # Use high precision from start
    "gl_high_prec": lambda d: (
        getcontext().prec = 150;
        a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
        for _ in range(25):
            a, b, t, p = (a + b) / 2, (a * b).sqrt(), t - p * (a - (a + b) / 2) ** 2, p * 2
        return ((a + b) ** 2) / (4 * t)
    ),
    
    # Brent-Salamin original (slightly different)
    "brent_salamin": lambda d: (
        a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
        for _ in range(25):
            a, b, t, p = (a+b)/2, (a*b).sqrt(), t - p*(a-a)**2, p*2
        ((a+b)**2)/(4*t)
    ),
    
    # Machin-like formula  
    "machin": lambda d: (
        getcontext().prec = 120
        def arctan(x, n=100):
            r = t = x
            for i in range(1, n):
                t *= -x*x
                r += t/(2*i+1)
            return r
        4*(4*arctan(Decimal(1)/5, 80) - arctan(Decimal(1)/239, 80))
    ),
}

print("\n🔬 Auto-Research: Testing algorithmic variants...\n")

results = []
for name, func in variants.items():
    t = test_variant(name, func)
    if t is not None:
        speedup = (baseline_time / t - 1) * 100
        status = "🚀 FASTER" if speedup > 0 else "="
        results.append((name, t, speedup, status))
        print(f"{name:20s} | {t*1000:7.4f}ms | {speedup:+6.2f}% | {status}")

# Sort by speed
results.sort(key=lambda x: x[2], reverse=True)
print(f"\n{'='*60}")
print(f"🏆 BEST: {results[0][0]} at {results[0][1]*1000:.4f}ms ({results[0][2]:+.2f}%)")
print(f"{'='*60}")