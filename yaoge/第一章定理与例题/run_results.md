# Chapter 1 Litex Run Results

- generated_at: `2026-06-09T14:29:26`
- litex_bin: `/opt/homebrew/bin/litex`
- litex_dir: `yaoge/第一章定理与例题`
- total_files: `86`
- success: `4`
- error: `82`
- timeout: `0`
- unparsed: `0`

| # | file | status | top error | deepest error | line | message |
|---:|---|---|---|---|---:|---|
| 1 | `001_ch1_theorem_01_basic_counting.lit` | `success` | `success` | `` | 41 |  |
| 2 | `002_ch1_theorem_02_generalized_counting.lit` | `success` | `success` | `` | 36 |  |
| 3 | `003_ch1_theorem_03_permutations.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 4 | `004_ch1_theorem_04_repeated_permutations.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(visible_orders) * internal_symmetry_count = count(labeled_orders)`\nUnknown: |
| 5 | `005_ch1_theorem_05_combination_formula.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 36 | set s is not a finite set |
| 6 | `006_ch1_theorem_06_pascal_identity.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 37 | set s is not a finite set |
| 7 | `007_ch1_theorem_07_binomial_theorem.lit` | `error` | `ExecStmtError` | `UnknownError` | 41 | forall: then-fact 1/1 could not be verified (unknown): `(x + y) ^ n = binomial_expansion_rhs(n, x, y)`\nUnknown: |
| 8 | `008_ch1_theorem_08_multinomial_coefficient.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 35 | set s is not a finite set |
| 9 | `009_ch1_theorem_09_multinomial_theorem.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `sum_value ^ n = multinomial_expansion_rhs(n, sum_value)`\nUnknown: |
| 10 | `010_ch1_theorem_10_positive_integer_solutions.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(solutions) = stars_and_bars_count(total, parts)`\nUnknown: |
| 11 | `011_ch1_theorem_11_nonnegative_integer_solutions.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(solutions) = stars_and_bars_count(total, parts)`\nUnknown: |
| 12 | `012_ch1_problems_01.lit` | `error` | `ExecStmtError` | `UnknownError` | 43 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(26, 2)`\nUnknown: |
| 13 | `013_ch1_problems_02.lit` | `success` | `success` | `` | 38 |  |
| 14 | `014_ch1_problems_03.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 15 | `015_ch1_problems_04.lit` | `error` | `ExecStmtError` | `UnknownError` | 41 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 16 | `016_ch1_problems_05.lit` | `success` | `success` | `` | 40 |  |
| 17 | `017_ch1_problems_06.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 18 | `018_ch1_problems_07.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 19 | `019_ch1_problems_08.lit` | `error` | `ExecStmtError` | `UnknownError` | 36 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 20 | `020_ch1_problems_09.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 21 | `021_ch1_problems_10.lit` | `error` | `ExecStmtError` | `UnknownError` | 41 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 22 | `022_ch1_problems_11.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 23 | `023_ch1_problems_12.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 24 | `024_ch1_problems_13.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 38 | set s is not a finite set |
| 25 | `025_ch1_problems_14.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 37 | set s is not a finite set |
| 26 | `026_ch1_problems_15.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 27 | `027_ch1_problems_16.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 28 | `028_ch1_problems_17.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 29 | `029_ch1_problems_18.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 39 | set s is not a finite set |
| 30 | `030_ch1_problems_19.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 41 | set s is not a finite set |
| 31 | `031_ch1_problems_20.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 32 | `032_ch1_problems_21.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 38 | set s is not a finite set |
| 33 | `033_ch1_problems_22.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 34 | set s is not a finite set |
| 34 | `034_ch1_problems_23.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 35 | `035_ch1_problems_24.lit` | `error` | `ExecStmtError` | `UnknownError` | 35 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 36 | `036_ch1_problems_25.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 37 | `037_ch1_problems_26.lit` | `error` | `ExecStmtError` | `UnknownError` | 35 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 38 | `038_ch1_problems_27.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 38 | set s is not a finite set |
| 39 | `039_ch1_problems_28.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 40 | `040_ch1_problems_29.lit` | `error` | `ExecStmtError` | `UnknownError` | 44 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 41 | `041_ch1_problems_30.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 42 | `042_ch1_problems_31.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 43 | `043_ch1_problems_32.lit` | `error` | `ExecStmtError` | `UnknownError` | 42 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 44 | `044_ch1_problems_33.lit` | `error` | `ExecStmtError` | `UnknownError` | 42 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 45 | `045_ch1_theoretical_exercises_01.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 46 | `046_ch1_theoretical_exercises_02.lit` | `error` | `ExecStmtError` | `UnknownError` | 41 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 47 | `047_ch1_theoretical_exercises_03.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 48 | `048_ch1_theoretical_exercises_04.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 49 | `049_ch1_theoretical_exercises_05.lit` | `error` | `ExecStmtError` | `UnknownError` | 36 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 50 | `050_ch1_theoretical_exercises_06.lit` | `error` | `ExecStmtError` | `UnknownError` | 36 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 51 | `051_ch1_theoretical_exercises_07.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 52 | `052_ch1_theoretical_exercises_08.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 53 | `053_ch1_theoretical_exercises_09.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 54 | `054_ch1_theoretical_exercises_10.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 49 | set s is not a finite set |
| 55 | `055_ch1_theoretical_exercises_11.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 41 | set s is not a finite set |
| 56 | `056_ch1_theoretical_exercises_12.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 56 | set s is not a finite set |
| 57 | `057_ch1_theoretical_exercises_13.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `(x + y) ^ n = binomial_expansion_rhs(n, x, y)`\nUnknown: |
| 58 | `058_ch1_theoretical_exercises_14.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 47 | set s is not a finite set |
| 59 | `059_ch1_theoretical_exercises_15.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 60 | `060_ch1_theoretical_exercises_16.lit` | `error` | `ExecStmtError` | `UnknownError` | 49 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 61 | `061_ch1_theoretical_exercises_17.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 62 | `062_ch1_theoretical_exercises_18.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 63 | `063_ch1_theoretical_exercises_19.lit` | `error` | `ExecStmtError` | `UnknownError` | 35 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 64 | `064_ch1_theoretical_exercises_20.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 65 | `065_ch1_theoretical_exercises_21.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 66 | `066_ch1_theoretical_exercises_22.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 67 | `067_ch1_theoretical_exercises_23.lit` | `error` | `ExecStmtError` | `UnknownError` | 36 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 68 | `068_ch1_self_test_01.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 69 | `069_ch1_self_test_02.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 70 | `070_ch1_self_test_03.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 42 | set s is not a finite set |
| 71 | `071_ch1_self_test_04.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 72 | `072_ch1_self_test_05.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 73 | `073_ch1_self_test_06.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 74 | `074_ch1_self_test_07.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 75 | `075_ch1_self_test_08.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 76 | `076_ch1_self_test_09.lit` | `error` | `ExecStmtError` | `UnknownError` | 45 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 77 | `077_ch1_self_test_10.lit` | `error` | `ExecStmtError` | `UnknownError` | 37 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 78 | `078_ch1_self_test_11.lit` | `error` | `ExecStmtError` | `UnknownError` | 40 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 79 | `079_ch1_self_test_12.lit` | `error` | `ExecStmtError` | `WellDefinedError` | 40 | set s is not a finite set |
| 80 | `080_ch1_self_test_13.lit` | `error` | `ExecStmtError` | `UnknownError` | 41 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 81 | `081_ch1_self_test_14.lit` | `error` | `ExecStmtError` | `UnknownError` | 36 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 82 | `082_ch1_self_test_15.lit` | `error` | `ExecStmtError` | `UnknownError` | 42 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |
| 83 | `083_ch1_self_test_16.lit` | `error` | `ExecStmtError` | `UnknownError` | 38 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 84 | `084_ch1_self_test_17.lit` | `error` | `ExecStmtError` | `UnknownError` | 39 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 85 | `085_ch1_self_test_18.lit` | `error` | `ExecStmtError` | `UnknownError` | 43 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = answer`\nUnknown: |
| 86 | `086_ch1_self_test_19.lit` | `error` | `ExecStmtError` | `UnknownError` | 43 | forall: then-fact 1/1 could not be verified (unknown): `count(outcomes) = falling_factorial(count(symbols), length)`\nUnknown: |

## Raw Output

Full stdout/stderr and parsed JSON are stored in `run_results.json`.
