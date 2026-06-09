#!/usr/bin/env python3
"""
Generate Chapter 1 Litex scaffold files from extracted proof-route records.

The generated files intentionally preserve proof debt. They do not convert a
textbook counting theorem into a bare arithmetic check, because that would hide
the exact Litex boundary this project is trying to test.
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from dataclasses import asdict
from pathlib import Path
from typing import Any

from extract_probability_theorems import chapter1_litex_records, extract_lines


DEFAULT_RECORDS_PATH = Path("yaoge/chapter1_litex_routes.json")
DEFAULT_PDF_PATH = Path("A-First-Course-in-Probability (1).pdf")
DEFAULT_OUTPUT_DIR = Path("yaoge/第一章定理与例题")


def load_records(records_path: Path, pdf_path: Path) -> list[dict[str, Any]]:
    if records_path.exists():
        return json.loads(records_path.read_text(encoding="utf-8"))

    records = chapter1_litex_records(extract_lines(pdf_path))
    return [asdict(record) for record in records]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "record"


def infer_topic(record: dict[str, Any]) -> str:
    text = f"{record.get('source_section', '')} {record.get('content', '')}".lower()
    if "permutation" in text or "arrangement" in text or "order" in text:
        return "permutations"
    if "combination" in text or "committee" in text or "subset" in text or "choose" in text:
        return "combinations"
    if "multinomial" in text:
        return "multinomial coefficients"
    if "integer" in text or "solution" in text or "distribute" in text:
        return "integer solutions"
    if "binomial" in text or "expand" in text:
        return "binomial theorem"
    return "combinatorial analysis"


def infer_difficulty(record: dict[str, Any]) -> str:
    status = record.get("status", "")
    blocker = record.get("blocker", "")
    if status == "blocked" and blocker in {"blocked_by_stdlib", "blocked_by_infer_rule"}:
        return "medium"
    if status == "blocked":
        return "hard"
    return "easy"


def comment_wrapped(label: str, text: str, width: int = 92) -> list[str]:
    if not text:
        return [f"# {label}: "]
    prefix = f"# {label}: "
    wrapped = textwrap.wrap(
        text,
        width=width,
        initial_indent=prefix,
        subsequent_indent="# " + " " * (len(label) + 2),
        break_long_words=False,
        break_on_hyphens=False,
    )
    return wrapped or [prefix.rstrip()]


def comment_list(title: str, values: list[str]) -> list[str]:
    lines = [f"# {title}:"]
    if not values:
        lines.append("# - ")
        return lines
    for value in values:
        wrapped = textwrap.wrap(
            value,
            width=92,
            initial_indent="# - ",
            subsequent_indent="#   ",
            break_long_words=False,
            break_on_hyphens=False,
        )
        lines.extend(wrapped or ["# - "])
    return lines


def proof_attempt_summary(record: dict[str, Any]) -> str:
    chain = record.get("litex_proof_chain", [])
    if not chain:
        return "No proof route was extracted; manually classify the source statement first."
    return " ".join(chain)


def render_intended_litex_attempt(record: dict[str, Any]) -> list[str]:
    objects = record.get("litex_objects", [])
    blocker = record.get("blocker", "")
    lines = [
        "# intended_litex_attempt:",
        "# 1. Name the counted mathematical object before evaluating any numeric expression.",
    ]
    for index, obj in enumerate(objects, start=2):
        lines.append(f"# {index}. Introduce or reuse Litex object: {obj}.")
    lines.extend(
        [
            "# next_verifier_step:",
            "# - Replace these comments with the smallest object-level Litex statement.",
            "# - Run the verifier.",
            "# - Record the exact first error or unknown line before simplifying the target.",
        ]
    )
    if blocker:
        lines.append(f"# expected_primary_blocker: {blocker}")
    return lines


def render_record(record: dict[str, Any]) -> str:
    status = record.get("status", "translated")
    blocker = record.get("blocker", "")
    proof_attempt = proof_attempt_summary(record)
    notes = record.get("notes", "")
    if status == "checkable":
        notes = (
            f"{notes} This generated scaffold is not itself verified; rerun the concrete "
            ".lit file before keeping status checkable."
        ).strip()
        status = "translated"

    lines: list[str] = []
    lines.extend(comment_wrapped("id", record.get("id", "")))
    lines.extend(comment_wrapped("source", "A First Course in Probability, Chapter 1"))
    lines.extend(comment_wrapped("kind", record.get("kind", "")))
    lines.extend(comment_wrapped("source_section", record.get("source_section", "")))
    lines.extend(comment_wrapped("pages", f"{record.get('page_start')}-{record.get('page_end')}"))
    lines.extend(comment_wrapped("topic", infer_topic(record)))
    lines.extend(comment_wrapped("difficulty", infer_difficulty(record)))
    lines.extend(comment_wrapped("natural_language_idea", record.get("content", "")))
    lines.extend(comment_wrapped("litex_code", "this file"))
    lines.extend(comment_wrapped("proof_attempt", proof_attempt))
    lines.extend(comment_wrapped("status", status))
    lines.extend(comment_wrapped("blocker", blocker))
    lines.extend(comment_wrapped("notes", notes))
    lines.extend(
        comment_wrapped(
            "verification_boundary",
            (
                "This file is a proof-route scaffold generated from the Chapter 1 extraction. "
                "Commented proof_debt and intended_litex_attempt lines are not verified. "
                "Only uncommented Litex statements count as verifier evidence."
            ),
        )
    )
    lines.append("")
    lines.extend(comment_list("book_proof_chain", record.get("litex_proof_chain", [])))
    lines.append("")
    lines.extend(comment_list("litex_objects_or_predicates", record.get("litex_objects", [])))
    lines.append("")
    if status == "blocked" or blocker:
        lines.extend(
            comment_wrapped(
                "proof_debt",
                (
                    "Formalize the source proof route directly and keep the first failing "
                    "object-level Litex statement here or in the nearby todo.md."
                ),
            )
        )
    else:
        lines.extend(
            comment_wrapped(
                "proof_debt",
                (
                    "Generate and run the concrete object-level Litex statement before changing "
                    "this item from translated to checkable."
                ),
            )
        )
    lines.append("")
    lines.extend(render_intended_litex_attempt(record))
    lines.append("")
    return "\n".join(lines)


def clean_existing_lit_files(output_dir: Path) -> int:
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
        return 0

    removed = 0
    for path in output_dir.glob("*.lit"):
        path.unlink()
        removed += 1
    return removed


def write_records(records: list[dict[str, Any]], output_dir: Path, clean: bool) -> tuple[int, int]:
    removed = clean_existing_lit_files(output_dir) if clean else 0
    for index, record in enumerate(records, start=1):
        filename = f"{index:03d}_{slugify(record.get('id', 'record'))}.lit"
        (output_dir / filename).write_text(render_record(record), encoding="utf-8")
    return removed, len(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Chapter 1 .lit proof-route scaffold files."
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
        help="Directory where generated .lit files are written.",
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

    removed, written = write_records(records, args.output_dir, clean=not args.no_clean)
    print(f"removed={removed} written={written} output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
