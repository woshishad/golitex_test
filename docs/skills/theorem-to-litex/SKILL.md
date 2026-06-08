---
name: theorem-to-litex
description: Use when translating a natural-language theorem, textbook result, dataset problem, proof sketch, or mathematical statement into runnable Litex .lit code, including choosing a Litex-native formulation, writing proof attempts, running the verifier, and classifying translated/checkable/blocked status.
---

# Theorem to Litex

Use this skill to turn a mathematical theorem or problem into Litex code. Follow
the Manual's central model: users write facts, and Litex grows a verified
context. The output should be a small, runnable `.lit` development whenever the
user asks for verifiable code.

## Core workflow

1. Understand the theorem in ordinary mathematics before writing Litex.
2. Identify objects, domains, assumptions, conclusions, and any witnesses or cases.
3. Choose the most Litex-native formulation, not a line-by-line translation from another prover.
4. Write facts in mathematical order so each accepted line becomes context for later lines.
5. Run the smallest relevant verifier command, read the exact result, and make the next smallest correction.
6. Classify the item as `translated`, `checkable`, or `blocked`.

If the task is for this repository and the user asks for code that makes Litex
code verifiable, write the attempt in `examples/tmp.lit` and test it directly.

## Formulating the statement

- Use builtin predicates and objects when they express the idea: `=`, `!=`, `<`, `<=`, `$in`, `$subset`, `$is_set`, `R`, `Z`, `N`, finite sets, tuples, functions, ranges, and standard set operations.
- Use `forall` block form for ordinary theorem statements. Without assumptions, put conclusions directly under `forall`; with assumptions, put hypotheses first, then `=>:`, then conclusions.
- Use `<=>:` only when both directions are intended. Otherwise use ordinary implication with `=>:`.
- Use `exist ... st { ... }` for existence statements and `witness` when proving one by explicit construction.
- Use `prop` for a reusable mathematical predicate with a definition. Use `abstract_prop` only for an intentionally uninterpreted concept, axiom interface, or clearly recorded proof debt.
- Use `claim` for short helper facts and local reusable `forall` patterns that should be available by shape matching.
- Use `thm name:` for named, classic, long, standard-library-facing, or parameter-sensitive theorems that should be cited explicitly with `by thm name(args...)`.

## Proof style

- Prefer explicit intermediate facts over large jumps.
- Use equality and inequality chains when they expose the ordinary calculation path.
- When a line becomes `unknown`, add a smaller equality, membership fact, domain condition, nonzero denominator fact, witness, case split, or helper `claim`.
- When a line becomes `error`, fix syntax or well-definedness first: undeclared names, missing type facts, function arguments outside the domain, invalid local witness scope, or division by zero.
- Keep goal shapes close to known facts and known `forall` conclusions so Litex can match them structurally.
- For existential goals, give a concrete `witness`; to use a known existential fact, use `have by exist` to name the witness and import its body facts.
- For disjunctions, prove one branch directly or use `by cases` when a known split should prove a shared goal branch-by-branch.
- For finite enumerated domains, use `by enumerate finite_set`, `by enumerate range`, or `by enumerate closed_range` when the proof is naturally case exhaustion.
- For induction over integer-like parameters, use `by induc` or `by strong_induc` only after identifying the base and step facts clearly.

## Proof debt and blockers

`know` is an assumption or proof-debt marker, similar in role to `sorry`. Use it
only when the task intentionally introduces background facts, axiom interfaces,
or a precise blocked step. Do not hide a gap by weakening the theorem.

When a proof is unfinished, record:

```yaml
id:
source:
topic:
difficulty:
natural_language_idea:
litex_code:
proof_attempt:
status: translated/checkable/blocked
blocker:
notes:
```

Use `checkable` only after running the relevant `.lit` code and seeing it
verify. Use `translated` when the statement is natural in Litex but the proof is
unfinished. Use `blocked` when the failure reason is understood. Prefer blocker
labels such as `blocked_by_language`, `blocked_by_stdlib`,
`blocked_by_infer_rule`, `blocked_by_kernel`, `blocked_by_syntax`,
`blocked_by_diagnostics`, or `blocked_by_formulation`.

## Running and interpreting Litex

- For a single file, run `litex -f path/to/file.lit` when the installed CLI is available.
- In this repository, use the smallest relevant test first; for example snippets, use `cargo test run_examples -- --nocapture` when appropriate.
- Treat verifier outcomes exactly:
  - `true`: keep the fact and continue.
  - `unknown`: the proof needs a smaller intermediate fact or better-shaped lemma.
  - `error`: syntax or well-definedness must be fixed before proof search matters.
- Read `verified_by` and `infer_facts` output when available. It shows whether a fact closed by builtin rules, known facts, known `forall` facts, theorem citation, or inferred context.
- After a proof works, remove unnecessary broad `know` facts and keep only explicit trusted assumptions with a reason.

## Output format for users

When reporting the result, include:

- The natural-language proof idea.
- The `.lit` file path or code snippet.
- The verifier command used.
- The status: `checkable`, `translated`, or `blocked`.
- Any remaining `know` facts or blocker labels.
- The next smallest step if the proof is not checkable yet.
