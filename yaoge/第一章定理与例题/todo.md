# Chapter 1 Litex Boundary Notes

This folder is a pressure test for Chapter 1 of *A First Course in
Probability*. The goal is not to make every file green by weakening the
mathematics. The goal is to follow the book's proof route, run Litex, and use
the exact failures to identify missing language, standard-library, builtin-rule,
kernel, or diagnostic support.

## Working rule

- Keep a runnable fragment when it is useful, but do not treat it as the full
  proof unless it proves the source-route mathematical object.
- If the book proof uses subsets, permutations, quotient counts, bijections, or
  stars-and-bars, first try to express that object directly.
- When that attempt fails, record the smallest failing snippet and exact output.
- Use `checkable` only for files whose executable Litex proves the intended
  mathematical statement, not merely a later arithmetic calculation.

## Current blocker map

### fixed-cardinality subset counting

Used by:

- `05_theorem_combination_formula.lit`
- `06_theorem_pascal_identity.lit`
- `23_example_4a_three_person_committees.lit`
- `24_example_4b_mixed_committee_with_restriction.lit`
- `29_example_5b_children_into_labeled_teams.lit`

Small failing attempt:

```litex
have people finite_set = {1, 2, 3, 4, 5}
have committees set = {s power_set(people): count(s) = 3}
count(committees) = 10
```

Exact verifier failure:

```text
line 2: have committees set = {s power_set(people): count(s) = 3}
WellDefinedError: failed to verify well-defined of set builder {s power_set(people): count(s) = 3}
previous: count(s) = 3
message: set s is not a finite set
```

Primary blocker: `blocked_by_infer_rule`

Needed support:

- infer `s` is finite from `s $in power_set(people)` and `$is_finite_set(people)`;
- or provide a standard fixed-cardinality subset constructor/count theorem.

### finite integer-solution set counting

Used by:

- `10_proposition_positive_integer_solutions.lit`
- `11_proposition_nonnegative_integer_solutions.lit`
- `33_example_6a_nonnegative_solutions_two_variables.lit`
- `34_example_6b_investment_allocations.lit`
- `35_example_6c_number_of_multinomial_terms.lit`

Small failing attempt:

```litex
have solutions set = {p cart(N, N): p[1] + p[2] = 3}
count(solutions) = 4
```

Exact verifier failure:

```text
line 2: count(solutions) = 4
WellDefinedError: set solutions is not a finite set
```

Primary blocker: `blocked_by_stdlib`

Needed support:

- bounded finite solution-set construction for equations over `N`;
- stars-and-bars theorem for positive and nonnegative integer solutions;
- diagnostics suggesting a bound such as `p[1] <= 3` and `p[2] <= 3`.

### permutation and no-repeat sequence objects

Used by:

- `03_theorem_permutation_of_distinct_objects.lit`
- `16_example_2e_license_plates_without_repetition.lit`
- `17_example_3a_batting_orders.lit`
- `18_example_3b_rankings_by_sex.lit`
- `31_example_5d_knockout_tournament.lit`

Small failing attempt:

```litex
have players finite_set = {1, 2, 3}
have orders set = {p cart(players, players, players): p[1] != p[2], p[1] != p[3], p[2] != p[3]}
count(orders) = 6
```

Exact verifier failure:

```text
line 2: have orders set = {p cart(players, players, players): p[1] != p[2], p[1] != p[3], p[2] != p[3]}
ParseError: Expected operator or $prop in fact
```

Primary blocker: `blocked_by_syntax`

Needed support:

- documented syntax for multiple set-builder filters, or better parse error;
- no-repeat tuple/permutation object for finite sets;
- theorem `count(permutations(S)) = factorial(count(S))`.

### quotient counting for indistinguishable objects

Used by:

- `04_theorem_permutation_with_repeated_objects.lit`
- `20_example_3d_pepper_arrangements.lit`
- `21_example_3e_tournament_nationalities.lit`
- `22_example_3f_colored_flags.lit`
- `30_example_5c_children_into_unlabeled_teams.lit`

Current status:

- no direct Litex object has been tested yet for quotienting labeled
  arrangements by internal symmetries;
- existing files only verify the arithmetic quotient after the mathematical
  quotient count is assumed externally.

Primary blocker: `blocked_by_stdlib`

Needed support:

- finite quotient count theorem;
- equivalence relation/class count interface;
- or specialized repeated-permutation/multinomial coefficient theorem.

### multinomial and finite-sum theorem interfaces

Used by:

- `07_theorem_binomial_theorem.lit`
- `09_theorem_multinomial_theorem.lit`
- `32_example_5e_expand_trinomial_square.lit`

Current status:

- concrete polynomial identities such as `(x+y)^3` and `(x1+x2+x3)^2` are
  checkable;
- the general finite-sum theorem statements are not represented.

Primary blocker: `blocked_by_stdlib`

Needed support:

- finite indexed sums over `k`;
- binomial and multinomial coefficient interfaces;
- theorem statements tying coefficients to combinatorial counts.
