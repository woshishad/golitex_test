#!/usr/bin/env python3
"""
Turn Chapter 1 proof-route records into executable Litex attempts.

This script follows the theorem-to-litex boundary-testing workflow:

1. Preserve the textbook proof route in comments.
2. Add a real, uncommented Litex `prove:` block for each item.
3. Name the mathematical object being counted before evaluating arithmetic.
4. Keep blocked concepts as object-level attempts, not as assumed target facts.

The generated files are expected to be a mixed batch: some should verify, and
some should fail in useful ways. The failures are the point of this dataset.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from extract_probability_theorems import chapter1_litex_records, extract_lines
from generate_chapter1_litex_files import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PDF_PATH,
    DEFAULT_RECORDS_PATH,
    comment_list,
    comment_wrapped,
    infer_difficulty,
    infer_topic,
    slugify,
)


def load_records(records_path: Path, pdf_path: Path) -> list[dict[str, Any]]:
    if records_path.exists():
        return json.loads(records_path.read_text(encoding="utf-8"))
    records = chapter1_litex_records(extract_lines(pdf_path))
    return [asdict(record) for record in records]


def indent_block(code: str, spaces: int = 0) -> list[str]:
    prefix = " " * spaces
    return [prefix + line if line else "" for line in code.strip("\n").splitlines()]


def is_abstract_record(record: dict[str, Any]) -> bool:
    """Return whether a source item should be translated at a general level."""

    kind = record.get("kind", "")
    if kind in {"theorem", "proposition", "lemma", "corollary"}:
        return True

    content = record.get("content", "").lower()
    abstract_markers = (
        "show that",
        "prove that",
        "derive",
        "establish",
        "in terms of n",
        "in terms of r",
        "as a function of",
        "for arbitrary",
        "for any",
        "for all",
        "for each n",
        "if there are n",
        "if n ",
        "where n ",
        "n people",
        "n men",
        "n women",
        "n boys",
        "n girls",
        "n objects",
        "n distinct",
    )
    return any(marker in content for marker in abstract_markers)


def source_item_shape(record: dict[str, Any]) -> str:
    return "abstract" if is_abstract_record(record) else "concrete"


def metadata_lines(record: dict[str, Any]) -> list[str]:
    proof_attempt = " ".join(record.get("litex_proof_chain", []))
    lines: list[str] = []
    lines.extend(comment_wrapped("id", record.get("id", "")))
    lines.extend(comment_wrapped("source", "A First Course in Probability, Chapter 1"))
    lines.extend(comment_wrapped("kind", record.get("kind", "")))
    lines.extend(comment_wrapped("source_item_shape", source_item_shape(record)))
    lines.extend(comment_wrapped("source_section", record.get("source_section", "")))
    lines.extend(comment_wrapped("pages", f"{record.get('page_start')}-{record.get('page_end')}"))
    lines.extend(comment_wrapped("topic", infer_topic(record)))
    lines.extend(comment_wrapped("difficulty", infer_difficulty(record)))
    lines.extend(comment_wrapped("natural_language_idea", record.get("content", "")))
    lines.extend(comment_wrapped("litex_code", "this file"))
    lines.extend(comment_wrapped("proof_attempt", proof_attempt))
    lines.extend(comment_wrapped("status", record.get("status", "translated")))
    lines.extend(comment_wrapped("blocker", record.get("blocker", "")))
    lines.extend(comment_wrapped("notes", record.get("notes", "")))
    lines.extend(
        comment_wrapped(
            "verification_boundary",
            (
                "The executable block below is a first Litex attempt generated from the "
                "book proof route. If it fails, keep the exact verifier output and classify "
                "the blocker instead of replacing the object-level statement by arithmetic."
            ),
        )
    )
    lines.append("")
    lines.extend(comment_list("book_proof_chain", record.get("litex_proof_chain", [])))
    lines.append("")
    lines.extend(comment_list("litex_objects_or_predicates", record.get("litex_objects", [])))
    return lines


def independent_cart_attempt() -> str:
    return """
prove:
    forall A, B finite_set, m, n N:
        count(A) = m
        count(B) = n
        =>:
            count(cart(A, B)) = count(A) * count(B) = m * n
"""


def concrete_cart_attempt(stage_counts: list[int]) -> str:
    if len(stage_counts) < 2:
        return concrete_unknown_count_attempt()

    lines = ["prove:"]
    set_names: list[str] = []
    for index, count in enumerate(stage_counts, start=1):
        set_name = f"S{index}"
        set_names.append(set_name)
        values = ", ".join(str(value) for value in range(1, count + 1))
        lines.append(f"    have {set_name} finite_set = {{{values}}}")

    lines.extend(
        [
            "    let outcomes finite_set:",
            f"        outcomes = cart({', '.join(set_names)})",
            "",
            f"    count(outcomes) = count(cart({', '.join(set_names)})) = "
            + " * ".join(f"count({set_name})" for set_name in set_names),
        ]
    )
    for set_name, count in zip(set_names, stage_counts):
        values = ", ".join(str(value) for value in range(1, count + 1))
        lines.append(f"    count({set_name}) = count({{{values}}}) = {count}")
    lines.append(
        "    count(outcomes) = "
        + " * ".join(str(count) for count in stage_counts)
        + f" = {product(stage_counts)}"
    )
    return "\n".join(lines) + "\n"


def four_stage_cart_attempt() -> str:
    return """
prove:
    forall A, B, C, D finite_set, a, b, c, d N:
        count(A) = a
        count(B) = b
        count(C) = c
        count(D) = d
        =>:
            count(cart(A, B, C, D)) = count(A) * count(B) * count(C) * count(D) = a * b * c * d
"""


def concrete_no_repeat_attempt(total_symbols: int, length: int) -> str:
    return f"""
prove:
    have falling_factorial fn(total, length N) N
    forall outcomes finite_set:
        count(outcomes) = falling_factorial({total_symbols}, {length})
"""


def no_repeat_tuple_attempt() -> str:
    return """
prove:
    have falling_factorial fn(total, length N) N
    forall symbols finite_set, length N, outcomes finite_set:
        count(outcomes) = falling_factorial(count(symbols), length)
"""


def concrete_fixed_subset_attempt(total: int, selected: int) -> str:
    values = ", ".join(str(value) for value in range(1, total + 1))
    return f"""
prove:
    have choose fn(n, r N) N
    have S finite_set = {{{values}}}
    let choices set:
        choices = {{s power_set(S): count(s) = {selected}}}

    count(S) = count({{{values}}}) = {total}
    count(choices) = choose({total}, {selected})
"""


def fixed_cardinality_subset_attempt() -> str:
    return """
prove:
    have choose fn(n, r N) N
    forall S finite_set, r N:
        count({s power_set(S): count(s) = r}) = choose(count(S), r)
"""


def concrete_unknown_count_attempt() -> str:
    return """
prove:
    forall outcomes finite_set, answer N:
        count(outcomes) = answer
"""


def quotient_count_attempt() -> str:
    return """
prove:
    forall labeled_orders, visible_orders finite_set, internal_symmetry_count N:
        count(visible_orders) * internal_symmetry_count = count(labeled_orders)
"""


def pascal_partition_attempt() -> str:
    return """
prove:
    have choose fn(n, r N) N
    forall S finite_set, distinguished S, r N:
        count({s power_set(S): count(s) = r}) = choose(count(S) - 1, r - 1) + choose(count(S) - 1, r)
"""


def binomial_attempt() -> str:
    return """
prove:
    have binomial_expansion_rhs fn(n N, x, y R) R
    forall n N, x, y R:
        (x + y)^n = binomial_expansion_rhs(n, x, y)
"""


def multinomial_attempt() -> str:
    return """
prove:
    have multinomial_expansion_rhs fn(n N, sum_value R) R
    forall n N, variables finite_set, sum_value R:
        sum_value^n = multinomial_expansion_rhs(n, sum_value)
"""


def integer_solution_attempt(positive: bool) -> str:
    return f"""
prove:
    have stars_and_bars_count fn(total, parts N) N
    forall total, parts N, solutions finite_set:
        count(solutions) = stars_and_bars_count(total, parts)
"""


def path_count_attempt() -> str:
    return """
prove:
    have choose fn(n, r N) N
    forall positions finite_set, right_moves N:
        count({s power_set(positions): count(s) = right_moves}) = choose(count(positions), right_moves)
"""


def fallback_attempt() -> str:
    return """
prove:
    forall parameters, outcomes finite_set, answer N:
        count(outcomes) = answer
"""


def product(values: list[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def concrete_stage_counts_from_content(content: str) -> list[int] | None:
    text = content.lower()
    if "die is rolled four times" in text or "die is rolled 4 times" in text:
        return [6, 6, 6, 6]
    if "area codes" in text or "area code" in text:
        if "first digit was an integer between 2 and 9" in text:
            return [8, 2, 9]
    if "first 2 places are for letters" in text and "other 5 for numbers" in text:
        return [26, 26, 10, 10, 10, 10, 10]
    return None


def concrete_attempt_for_record(record: dict[str, Any]) -> str:
    content = record.get("content", "").lower()
    objects = " ".join(record.get("litex_objects", [])).lower()

    stage_counts = concrete_stage_counts_from_content(content)
    if stage_counts and "no-repeat" not in objects:
        return concrete_cart_attempt(stage_counts)
    if "no-repeat" in objects:
        if "first 2 places are for letters" in content and "other 5 for numbers" in content:
            return concrete_no_repeat_attempt(26, 2)
        return no_repeat_tuple_attempt()
    if "fixed-cardinality" in objects or "power_set" in objects or "choose" in objects:
        return concrete_fixed_subset_attempt(5, 3)
    if "cart" in objects or "finite sets for positions" in objects:
        if stage_counts:
            return concrete_cart_attempt(stage_counts)
        return concrete_unknown_count_attempt()
    return concrete_unknown_count_attempt()


def abstract_attempt_for_record(record: dict[str, Any]) -> str:
    content = record.get("content", "").lower()
    objects = " ".join(record.get("litex_objects", [])).lower()
    record_id = record.get("id", "")

    if "theorem_01" in record_id:
        return independent_cart_attempt()
    if "theorem_02" in record_id:
        return four_stage_cart_attempt()
    if "pascal_identity" in record_id:
        return pascal_partition_attempt()
    if "binomial_theorem" in record_id:
        return binomial_attempt()
    if "multinomial_theorem" in record_id:
        return multinomial_attempt()
    if "binomial" in objects or "binomial" in content:
        return binomial_attempt()
    if "multinomial theorem" in content or "multi-index" in objects:
        return multinomial_attempt()
    if "multinomial coefficient" in objects or "labeled group" in objects:
        return fixed_cardinality_subset_attempt()
    if "positive solution" in objects:
        return integer_solution_attempt(positive=True)
    if "nonnegative solution" in objects or "integer solution" in objects or "stars-and-bars" in objects:
        return integer_solution_attempt(positive=False)
    if "fixed-cardinality" in objects or "power_set" in objects or "choose" in objects:
        return fixed_cardinality_subset_attempt()
    if "no-repeat" in objects or "permutation" in objects or "permutation" in content:
        return no_repeat_tuple_attempt()
    if "quotient" in objects or "repeated classes" in content or "indistinguishable" in content:
        return quotient_count_attempt()
    if "path" in content or "grid" in content or "lattice" in content:
        return path_count_attempt()
    if "cart" in objects or "finite sets for positions" in objects:
        return independent_cart_attempt()
    return fallback_attempt()


def attempt_for_record(record: dict[str, Any]) -> str:
    if is_abstract_record(record):
        return abstract_attempt_for_record(record)
    return concrete_attempt_for_record(record)


def render_file(record: dict[str, Any]) -> str:
    lines = metadata_lines(record)
    lines.append("")
    lines.append("# executable_litex_attempt:")
    lines.extend(indent_block(attempt_for_record(record)))
    lines.append("")
    return "\n".join(lines)


def clean_existing_lit_files(output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    removed = 0
    for path in output_dir.glob("*.lit"):
        path.unlink()
        removed += 1
    return removed


def write_attempts(records: list[dict[str, Any]], output_dir: Path, clean: bool) -> tuple[int, int]:
    removed = clean_existing_lit_files(output_dir) if clean else 0
    for index, record in enumerate(records, start=1):
        filename = f"{index:03d}_{slugify(record.get('id', 'record'))}.lit"
        (output_dir / filename).write_text(render_file(record), encoding="utf-8")
    return removed, len(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materialize Chapter 1 scaffold records into executable .lit attempts."
    )
    parser.add_argument(
        "--records",
        type=Path,
        default=DEFAULT_RECORDS_PATH,
        help="JSON records generated by extract_probability_theorems.py --chapter1-litex.",
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=DEFAULT_PDF_PATH,
        help="Fallback PDF path used when --records does not exist.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where .lit attempt files are written.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not delete existing .lit files before writing generated files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print how many files would be written without touching the output directory.",
    )
    args = parser.parse_args()

    records = load_records(args.records, args.pdf)
    if args.dry_run:
        print(f"would_write={len(records)} output_dir={args.output_dir}")
        return 0

    removed, written = write_attempts(records, args.output_dir, clean=not args.no_clean)
    print(f"removed={removed} written={written} output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
