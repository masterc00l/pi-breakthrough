"""
Auto-Research Pi Optimization
Tweak → Test → Keep/Kill → Repeat
"""

import random
import time
from decimal import Decimal, getcontext
import json

getcontext().prec = 120

# Baseline: Gauss-Legendre (known: ~0.4ms for 101 digits)
def gauss_legendre(digits):
    a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
    for _ in range(30):
        a, b, t, p = (a + b) / 2, (a * b).sqrt(), t - p * (a - (a + b) / 2) ** 2, p * 2
    return ((a + b) ** 2) / (4 * t)

# Get baseline time
baseline_time = None
for _ in range(5):
    start = time.time()
    result = gauss_legendre(101)
    t = time.time() - start
    if baseline_time is None or t < baseline_time:
        baseline_time = t

print(f"Baseline (Gauss-Legendre): {baseline_time*1000:.4f}ms")

# Tweak mutations
def mutate_gauss_legendre(digits, mutation):
    """Apply mutations to Gauss-Legendre"""
    a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
    
    iterations = 30
    if 'iter_plus' in mutation:
        iterations += random.randint(-2, 5)
    if 'iter_mult' in mutation:
        iterations = int(iterations * random.uniform(0.8, 1.5))
    
    # Bound iterations
    iterations = max(5, min(100, iterations))
    
    for _ in range(iterations):
        a_new = (a + b) / 2
        
        # Mutation: vary the geometric mean calculation
        if 'geo_variant' in mutation:
            # Try different root approximations
            root_approx = (a * b).sqrt()
            if random.random() < 0.3:
                # Use different approximation
                root_approx = ((a + b) / 2) * Decimal('0.9999') if random.random() < 0.5 else (a * b).sqrt() * Decimal('1.0001')
            b_new = root_approx
        else:
            b_new = (a * b).sqrt()
        
        # Mutation: vary the correction term
        if 'correction' in mutation:
            correction_factor = Decimal('1.0')
            if random.random() < 0.2:
                correction_factor = Decimal(str(random.uniform(0.99, 1.01)))
            t_new = t - p * (a - a_new) ** 2 * correction_factor
        else:
            t_new = t - p * (a - a_new) ** 2
        
        p_new = p * 2
        
        a, b, t, p = a_new, b_new, t_new, p_new
    
    return ((a + b) ** 2) / (4 * t)

# Auto-research loop
print("\n🔬 Starting Auto-Research Optimization...\n")

mutations_tried = {}
best_time = baseline_time
best_mutation = None
best_result = gauss_legendre(101)

# Generate and test mutations
for attempt in range(50):
    # Randomly select mutations
    mutation = []
    if random.random() < 0.5:
        mutation.append('iter_plus')
    if random.random() < 0.5:
        mutation.append('iter_mult')
    if random.random() < 0.4:
        mutation.append('geo_variant')
    if random.random() < 0.3:
        mutation.append('correction')
    
    mutation_key = '+'.join(mutation) if mutation else 'baseline'
    
    # Test this mutation
    times = []
    for _ in range(3):
        start = time.time()
        result = mutate_gauss_legendre(101, mutation)
        times.append(time.time() - start)
    
    avg_time = sum(times) / len(times)
    
    # Check correctness
    expected = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480"
    result_str = str(result)[:102]
    correct = result_str == expected
    
    # Result
    if correct:
        status = "✅"
        if avg_time < best_time:
            best_time = avg_time
            best_mutation = mutation_key
            best_result = result
            status = "🚀 FASTER!"
    else:
        status = "❌"
    
    print(f"Attempt {attempt+1:2d}: {mutation_key:20s} | {avg_time*1000:7.4f}ms | {status}")
    
    # Record
    if mutation_key not in mutations_tried:
        mutations_tried[mutation_key] = {'time': avg_time, 'correct': correct}

print(f"\n{'='*60}")
print(f"RESULTS:")
print(f"  Baseline:   {baseline_time*1000:.4f}ms")
print(f"  Best:       {best_time*1000:.4f}ms | {best_mutation}")
print(f"  Speedup:    {(baseline_time/best_time - 1)*100:.2f}%")
print(f"\nBest result: {str(best_result)[:50]}...")
print(f"{'='*60}")