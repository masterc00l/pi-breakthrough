"""
Auto-Research Pi Optimization v3
Tweak → Test (101 digits) → Keep Faster / Kill Slower → Repeat
"""

import random
import time
from decimal import Decimal, getcontext
import copy

# Setup high precision
getcontext().prec = 200
CORRECT = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480"

def check_correct(result):
    """Check if result matches 101 correct digits of Pi"""
    return str(result).replace('.','')[:101] == CORRECT[:101]

def run_gauss_legendre(iterations=30):
    """Gauss-Legendre with variable iterations"""
    a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
    for _ in range(iterations):
        a_new = (a + b) / 2
        b_new = (a * b).sqrt()
        t_new = t - p * (a - a_new) ** 2
        p_new = p * 2
        a, b, t, p = a_new, b_new, t_new, p_new
    return ((a + b) ** 2) / (4 * t)

# Get baseline
times = []
for _ in range(10):
    start = time.time()
    result = run_gauss_legendre(30)
    times.append(time.time() - start)
baseline = min(times)
print(f"Baseline: {baseline*1000:.4f}ms | Correct: {check_correct(result)}")

# Auto-research loop
print("\n🔬 Auto-Research: Mutate → Test → Keep Faster → Repeat\n")

best_time = baseline
best_config = {"iterations": 30}
history = []

# Test different iteration counts
for iters in [20, 25, 28, 29, 30, 31, 32, 35, 40]:
    times = []
    for _ in range(5):
        start = time.time()
        result = run_gauss_legendre(iters)
        elapsed = time.time() - start
        if check_correct(result):
            times.append(elapsed)
    
    if times:
        avg_time = min(times)
        diff = (best_time - avg_time) / best_time * 100
        status = "🚀" if avg_time < best_time else "="
        if avg_time < best_time:
            best_time = avg_time
            best_config = {"iterations": iters}
        print(f"iterations={iters:2d} | {avg_time*1000:7.4f}ms | Best: {best_time*1000:.4f}ms | {status}")

# Now try mutations on the best iteration count
print(f"\n--- Tuning best iteration count ({best_config['iterations']}) ---\n")

for trial in range(50):
    # Generate mutation
    mutation = {
        "iterations": best_config["iterations"] + random.randint(-3, 3),
        "early_exit": random.random() < 0.3,
        "sqrt_approx": random.choice([None, "newton", "halley", "simple"]),
        "parallel_approx": random.random() < 0.2,
    }
    
    # Clamp iterations
    mutation["iterations"] = max(10, min(60, mutation["iterations"]))
    
    # Run with mutation
    times = []
    for _ in range(3):
        start = time.time()
        
        a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / Decimal(4), Decimal(1)
        
        for i in range(mutation["iterations"]):
            a_new = (a + b) / 2
            
            # Mutation: different sqrt approximation
            if mutation["sqrt_approx"] == "newton":
                # Newton iteration for sqrt
                b_new = b * (Decimal(3) + (a*a + b*b) / (b*b)) / Decimal(4)
            elif mutation["sqrt_approx"] == "halley":
                b_new = b * (b*b + 3*a*a) / (3*b*b + a*a)
            elif mutation["sqrt_approx"] == "simple":
                b_new = (a + b) / Decimal(2)  # simpler approx
            else:
                b_new = (a * b).sqrt()
            
            # Mutation: parallel approximation
            if mutation["parallel_approx"] and i % 2 == 0:
                b_new = b_new * Decimal('0.9999')
            
            t_new = t - p * (a - a_new) ** 2
            p_new = p * 2
            a, b, t, p = a_new, b_new, t_new, p_new
            
            # Mutation: early exit
            if mutation["early_exit"] and i > 5:
                if abs(a - b) < Decimal(10) ** (-102):
                    break
        
        result = ((a + b) ** 2) / (4 * t)
        elapsed = time.time() - start
        
        if check_correct(result):
            times.append(elapsed)
    
    if times:
        avg_time = min(times)
        speedup = (best_time - avg_time) / best_time * 100
        
        if avg_time < best_time:
            best_time = avg_time
            best_config = mutation.copy()
            print(f"Trial {trial+1:2d}: MUTATION KEPT! {avg_time*1000:.4f}ms | {speedup:+.2f}% faster")
        else:
            status = "="
            if trial % 10 == 0:
                print(f"Trial {trial+1:2d}: {avg_time*1000:.4f}ms | {status}")

print(f"\n{'='*60}")
print(f"🏆 FINAL RESULT:")
print(f"  Time: {best_time*1000:.4f}ms for 101 digits")
print(f"  Config: {best_config}")
print(f"  Speedup from baseline: {(baseline/best_time - 1)*100:.2f}%")
print(f"{'='*60}")