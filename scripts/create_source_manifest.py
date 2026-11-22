#!/usr/bin/env python3
"""Create a reproducibility manifest for a CFPB complaint CSV snapshot.

The script records the file hash, byte size, parsed row/column counts, ordered
column names, source URL/version supplied by the operator, and capture time.
It uses Python's CSV parser so quoted fields containing commas or line breaks
are counted as records rather than physical lines.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def profile_csv(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Source CSV does not exist: {path}")
    if path.stat().st_size == 0:
        raise ValueError("Source CSV is empty.")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        try:
            columns = next(reader)
        except StopIteration as exc:
            raise ValueError("Source CSV contains no header row.") from exc

        if not columns or not any(name.strip() for name in columns):
            raise ValueError("Source CSV header is empty.")
        if len(columns) != len(set(columns)):
            raise ValueError("Source CSV contains duplicate column names.")

        row_count = 0
        for row in reader:
            if len(row) != len(columns):
                raise ValueError(
                    f"CSV record {row_count + 1} has {len(row)} fields; "
                    f"expected {len(columns)}. Parser reached physical line {reader.line_num}."
                )
            row_count += 1

    return {
        "file_name": path.name,
        "file_size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "row_count": row_count,
        "column_count": len(columns),
        "columns": columns,
    }


def build_manifest(
    source_path: Path,
    source_url: str | None = None,
    source_version: str | None = None,
    downloaded_at_utc: str | None = None,
) -> dict[str, Any]:
    metadata = profile_csv(source_path)
    metadata.update({
        "manifest_schema_version": 1,
        "source_name": "CFPB Consumer Complaint Database",
        "source_url": source_url,
        "source_version": source_version,
        "downloaded_at_utc": downloaded_at_utc,
        "manifest_created_at_utc": datetime.now(timezone.utc).isoformat(),
    })
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="Downloaded source CSV path")
    parser.add_argument("--source-url", help="Exact source download/page URL")
    parser.add_argument("--source-version", help="Dataset version, snapshot date or release identifier")
    parser.add_argument("--downloaded-at-utc", help="Original download timestamp in ISO-8601 UTC")
    parser.add_argument("--output", type=Path, default=Path("source-snapshot-manifest.json"))
    args = parser.parse_args()

    try:
        manifest = build_manifest(
            args.csv_path,
            source_url=args.source_url,
            source_version=args.source_version,
            downloaded_at_utc=args.downloaded_at_utc,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            f"Manifest written to {args.output}: "
            f"{manifest['row_count']:,} rows, {manifest['column_count']} columns, "
            f"SHA-256 {manifest['sha256']}"
        )
        return 0
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
