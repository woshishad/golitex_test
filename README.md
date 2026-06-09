# Litex Contribution Work Report

This repository records my contribution work around Litex. The main goal is to
use real textbook translation as a pressure test for Litex: translate natural
mathematical statements into Litex attempts, run the verifier, and turn failures
into concrete language, standard-library, inference-rule, and diagnostic
blockers.

The current vertical slice is Chapter 1 of *A First Course in Probability*.
This chapter is useful because it contains basic counting principles,
permutations, combinations, binomial and multinomial formulas, quotient-counting
ideas, and stars-and-bars arguments.

## Contribution Summary

My work builds an end-to-end feedback loop:

1. Extract theorem, proposition, exercise, and self-test items from the textbook.
2. Preserve each item's mathematical proof route before writing Litex code.
3. Generate `.lit` proof attempts from the structured records.
4. Distinguish abstract theorems from concrete problems when generating code.
5. Run Litex on every generated file and record exact verifier output.
6. Classify failures into formulation, inference-rule, standard-library,
   syntax, kernel, or diagnostic blockers.

This is not intended as a line-by-line port of a textbook. It is a structured
pressure test for what Litex can already express and verify, and what support is
still missing.

## Main Artifacts

- `docs/skills/contribute-to-litex/SKILL.md`: contribution workflow skill for
  Litex documentation feedback, dataset/textbook translation work, blocker
  reporting, and contribution PR preparation.
- `docs/skills/theorem-to-litex/SKILL.md`: theorem/problem-to-Litex translation
  skill. I updated it to enforce proof-route preservation, boundary probing,
  no circular proof debt, and correct handling of abstract versus concrete
  source items.
- `yaoge/extract_probability_theorems.py`: extracts theorem/problem records and
  proof routes from the probability textbook PDF.
- `yaoge/generate_chapter1_litex_files.py`: creates initial scaffold `.lit`
  files from extracted Chapter 1 proof-route records.
- `yaoge/materialize_chapter1_litex_attempts.py`: turns scaffold records into
  executable `.lit` attempts while applying the abstract/concrete translation
  rule.
- `yaoge/run_chapter1_litex_attempts.py`: runs all generated Chapter 1 `.lit`
  files and writes structured logs.
- `yaoge/第一章定理与例题/`: generated Chapter 1 `.lit` files, run logs, and
  blocker notes.

## Skill Improvements

I created and revised project-local skills to make the contribution workflow
repeatable.

### `contribute-to-litex`

This skill defines how to contribute through:

- documentation feedback;
- dataset and textbook translation;
- understanding/demo improvements;
- blocker records;
- contribution PR preparation.

It also sets the rule that new contributors should usually focus first on
textbook/data/documentation work rather than verifier, parser, builtin-rule, or
soundness-critical kernel changes.

### `theorem-to-litex`

This skill defines the theorem translation discipline used in this work:

- understand the ordinary mathematics before writing Litex;
- preserve the source proof route;
- write object-level Litex attempts instead of replacing the theorem with easier
  arithmetic;
- run the verifier and record exact failures;
- classify each item as `translated`, `checkable`, or `blocked`;
- never mark an item `checkable` without actually running the relevant `.lit`
  file.

A key correction I added is the abstract/concrete distinction:

- For an abstract theorem, do not prove only a hand-picked concrete instance.
  For example, a theorem about arbitrary finite sets `A` and `B` should be
  translated using a general `forall A, B ...` formulation.
- For a concrete textbook problem, it is valid to use the concrete objects and
  numbers from that problem, as long as the proof follows the problem's
  mathematical chain.
- Concrete witnesses are appropriate for existence proofs.
- Concrete objects are appropriate for counterexamples.

This rule was added after finding that a generated proof for the basic counting
principle incorrectly used a single concrete example instead of the general
statement.

## Chapter 1 Translation Work

The Chapter 1 pipeline generated `86` `.lit` files covering:

- textbook theorem/proposition records;
- ordinary problems;
- theoretical exercises;
- self-test problems.

Each generated file records:

```yaml
id:
source:
kind:
source_item_shape: abstract/concrete
source_section:
pages:
topic:
difficulty:
natural_language_idea:
proof_attempt:
status:
blocker:
notes:
book_proof_chain:
litex_objects_or_predicates:
executable_litex_attempt:
```

The generated files are intentionally evidence-oriented. If a proof cannot be
completed, the file keeps the attempted Litex formulation and the run log records
why it failed.

## Running Attempts

The batch runner is:

```bash
/Users/yaoge/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 yaoge/run_chapter1_litex_attempts.py
```

It writes:

- `yaoge/第一章定理与例题/run_results.md`: human-readable run summary;
- `yaoge/第一章定理与例题/run_results.json`: full raw verifier output.

Current run summary:

- total files: `86`
- success: `4`
- error: `82`
- timeout: `0`
- unparsed: `0`

Successful files in the latest run:

- `001_ch1_theorem_01_basic_counting.lit`
- `002_ch1_theorem_02_generalized_counting.lit`
- `013_ch1_problems_02.lit`
- `016_ch1_problems_05.lit`

These successes show that Litex can already verify finite Cartesian-product
counting patterns, including both an abstract basic counting theorem and
concrete multi-stage counting problems.

## Failure Analysis

The current failures are useful because they identify where Litex needs more
support.

Major failure clusters from the run log:

1. `blocked_by_formulation`
   - Many generated files still fall back to a generic statement such as
     `count(outcomes) = answer`.
   - This means the generator has not yet classified the problem into a precise
     mathematical object.
   - Next step: improve problem-type recognition and generate sharper Litex
     formulations.

2. `blocked_by_infer_rule`
   - Fixed-cardinality subset expressions such as
     `{s power_set(S): count(s) = r}` fail because Litex does not infer that
     `s` is finite from `s power_set(S)` and `S finite_set`.
   - Next step: add or propose an inference rule for finite subsets of finite
     sets, or introduce a standard fixed-cardinality subset object.

3. `blocked_by_stdlib`
   - Missing standard objects/theorems include:
     - no-repeat sequences and permutation counts;
     - falling factorial count theorem;
     - quotient counting for repeated or indistinguishable objects;
     - stars-and-bars for integer solution counts;
     - binomial and multinomial finite-sum interfaces.

4. `blocked_by_diagnostics`
   - Some verifier outputs are technically correct but still indirect for a
     translation workflow.
   - A useful future improvement is to make errors suggest the missing object or
     theorem more directly, for example fixed-cardinality subset support.

## Concrete Examples of the Feedback Loop

### Basic counting principle

The abstract theorem is now generated as a general Litex statement:

```litex
prove:
    forall A, B finite_set, m, n N:
        count(A) = m
        count(B) = n
        =>:
            count(cart(A, B)) = count(A) * count(B) = m * n
```

This verifies successfully and uses Litex's Cartesian-product count support.

### Four die rolls

A concrete textbook problem is generated using the concrete objects from the
problem:

```litex
prove:
    have S1 finite_set = {1, 2, 3, 4, 5, 6}
    have S2 finite_set = {1, 2, 3, 4, 5, 6}
    have S3 finite_set = {1, 2, 3, 4, 5, 6}
    have S4 finite_set = {1, 2, 3, 4, 5, 6}
    let outcomes finite_set:
        outcomes = cart(S1, S2, S3, S4)

    count(outcomes) = count(cart(S1, S2, S3, S4)) = count(S1) * count(S2) * count(S3) * count(S4)
    count(S1) = count({1, 2, 3, 4, 5, 6}) = 6
    count(S2) = count({1, 2, 3, 4, 5, 6}) = 6
    count(S3) = count({1, 2, 3, 4, 5, 6}) = 6
    count(S4) = count({1, 2, 3, 4, 5, 6}) = 6
    count(outcomes) = 6 * 6 * 6 * 6 = 1296
```

This also verifies successfully.

### Combination formula blocker

The natural object-level Litex attempt is:

```litex
prove:
    have choose fn(n, r N) N
    forall S finite_set, r N:
        count({s power_set(S): count(s) = r}) = choose(count(S), r)
```

The current blocker is that Litex cannot prove the set-builder is well-defined,
because it cannot infer that `s` is finite inside `count(s)`.

## Next Steps

The most useful next work is:

1. Improve generated formulation quality to reduce fallback records.
2. Add or propose inference support for finite subsets of finite sets.
3. Design standard objects for fixed-cardinality subsets, permutations,
   no-repeat sequences, quotient counts, and integer solution sets.
4. Convert successful attempts into clean examples or benchmark items.
5. Keep failed attempts as minimal reproductions for Litex standard-library and
   diagnostic improvements.
