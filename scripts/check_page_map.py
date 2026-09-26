#!/usr/bin/env python3
"""Check that a scanned book's source pages are accounted for before delivery.

This checks coverage and declared review status, not whether OCR text is correct.
"""

import argparse
import csv
import sys
import zipfile
from pathlib import Path, PurePosixPath


FIELDS = {
    "source_page", "kind", "rendering", "epub_target", "review_status",
    "open_issues", "omission_reason",
}
KINDS = {"text", "cover", "contents", "illustration", "notes", "blank", "other"}
RENDERINGS = {"text", "image", "omitted"}
STATUSES = {"verified", "pending", "not_applicable"}


def check(manifest, expected_pages, epub=None):
    errors = []
    with manifest.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing_fields = FIELDS - set(reader.fieldnames or [])
        if missing_fields:
            return [f"Missing columns: {', '.join(sorted(missing_fields))}"], 0
        rows = list(reader)

    targets = None
    if epub is not None:
        with zipfile.ZipFile(epub) as archive:
            targets = set(archive.namelist())

    seen = set()
    for line_number, row in enumerate(rows, 2):
        if None in row or any(row[field] is None for field in FIELDS):
            errors.append(f"Line {line_number}: malformed CSV row")
            continue
        value = row["source_page"].strip()
        try:
            page = int(value)
            if page < 1:
                raise ValueError
        except ValueError:
            errors.append(f"Line {line_number}: invalid source_page {value!r}")
            continue
        if page in seen:
            errors.append(f"Page {page}: duplicate source_page")
        seen.add(page)

        kind = row["kind"].strip()
        rendering = row["rendering"].strip()
        status = row["review_status"].strip()
        target = row["epub_target"].strip()
        issues = row["open_issues"].strip()
        reason = row["omission_reason"].strip()

        if kind not in KINDS:
            errors.append(f"Page {page}: unknown kind {kind!r}")
        if rendering not in RENDERINGS:
            errors.append(f"Page {page}: unknown rendering {rendering!r}")
        if status not in STATUSES:
            errors.append(f"Page {page}: unknown review_status {status!r}")
        if issues:
            errors.append(f"Page {page}: unresolved issue: {issues}")

        if rendering == "omitted":
            if target:
                errors.append(f"Page {page}: omitted page has an epub_target")
            if not reason:
                errors.append(f"Page {page}: omission_reason is required")
            if status == "pending":
                errors.append(f"Page {page}: omission is not verified")
        elif rendering in {"text", "image"}:
            if not target:
                errors.append(f"Page {page}: included page has no epub_target")
            elif target.startswith("/") or "\\" in target or ".." in PurePosixPath(target).parts:
                errors.append(f"Page {page}: unsafe epub_target {target!r}")
            elif targets is not None and target not in targets:
                errors.append(f"Page {page}: epub_target is missing from EPUB: {target}")
            if status != "verified":
                errors.append(f"Page {page}: included page is not verified")

    expected = set(range(1, expected_pages + 1))
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    if missing:
        errors.append(f"Missing source pages: {missing}")
    if extra:
        errors.append(f"Pages beyond expected range: {extra}")
    return errors, len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="CSV page map")
    parser.add_argument("--expected-pages", type=int, required=True)
    parser.add_argument("--epub", type=Path, help="check target paths inside this EPUB")
    args = parser.parse_args()
    if args.expected_pages < 1:
        parser.error("--expected-pages must be positive")
    try:
        errors, row_count = check(args.manifest, args.expected_pages, args.epub)
    except (OSError, csv.Error, zipfile.BadZipFile) as exc:
        parser.exit(2, f"Could not check page map: {exc}\n")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} issue(s) across {row_count} row(s)", file=sys.stderr)
        return 1
    print(f"PASS: all {args.expected_pages} source pages accounted for")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
