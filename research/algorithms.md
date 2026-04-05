# Pi Computation Research - Discovered Algorithms

## Recent Findings (2023-2026)

### 1. Catalan Numbers Approach (2024)
- **Source**: GitHub - Abhrankan-Chakrabarti/pi-calculation-with-catalan-numbers
- **Method**: Uses Catalan numbers and fixed-point arithmetic
- **Novelty**: Unique approach leveraging Catalan number properties

### 2. Stride-6 Engine (Feb 2026) ⭐ NEWEST
- **Source**: GitHub - NachoPeinador/Arquitectura-de-Hibridacion-Algoritmica-en-Z-6Z
- **Method**: Unifies Chudnovsky's series with DSP polyphase decomposition in Z/6Z
- **Performance**: Validated at 100M digits with 95% parallel efficiency
- **Features**: Shared-Nothing architecture, bypasses memory wall

### 3. Monte Carlo GPU (2024)
- **Source**: GitHub - Nikolay1998/cuda-pi-calculation
- **Method**: CUDA-based Monte Carlo

### 4. Rust Big Number (2025)
- **Source**: GitHub - BreezeWhite/BigBench
- **Method**: Benchmarks of Rust big number crates

## Physical Experiment Methods

### Classic Approaches
1. **Buffon's Needle** - Drop needles on parallel lines
2. **Random Walk** - 2D random walk distance estimation
3. **Monte Carlo** - Random point in square/circle
4. **Galton Board** - Falling balls through pegs

### Novel Physical Ideas
- Quantum random number generators
- Thermal noise-based randomness
- Optics/photonics approaches

## Algorithm Comparison for 101 Digits

| Method | Complexity | Suitable for 101 digits |
|--------|------------|------------------------|
| Chudnovsky | O(n log³ n) | ✅ Excellent |
| Gauss-Legendre | O(n log² n) | ✅ Excellent |
| BBP (Digit Extraction) | O(n) | ✅ Good |
| Catalan Numbers | Unknown | 🔬 Need to test |
| Monte Carlo | O(n) | ❌ Slow for precision |

## Implementation Priority

1. ✅ Chudnovsky (baseline, known fast)
2. ✅ Gauss-Legendre 
3. 🔬 Catalan Numbers (novel)
4. 🔬 Stride-6 (newest, most promising)
5. 🔬 Physical experiment variant

## Research Notes

- "Saha-Sinha Pi Formula (2024)" mentioned in search - uses string theory scattering amplitudes
- No significant 2024-2026 arXiv papers specifically on NEW Pi algorithms
- Most recent work focuses on optimization/parallelization, not new formulas

---
Updated: 2026-04-05