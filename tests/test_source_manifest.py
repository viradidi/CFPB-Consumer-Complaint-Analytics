from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.create_source_manifest import build_manifest, profile_csv


class SourceManifestTests(unittest.TestCase):
    def test_counts_csv_records_with_embedded_newlines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "complaints.csv"
            with path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["complaint_id", "narrative"])
                writer.writerow(["1", "first line\nsecond line"])
                writer.writerow(["2", "text, with comma"])
            result = profile_csv(path)
            self.assertEqual(result["row_count"], 2)
            self.assertEqual(result["column_count"], 2)
            self.assertEqual(result["columns"], ["complaint_id", "narrative"])
            self.assertEqual(len(result["sha256"]), 64)

    def test_manifest_records_source_identity_and_snapshot_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "complaints.csv"
            path.write_text("id,value\n1,a\n2,b\n", encoding="utf-8")
            manifest = build_manifest(
                path,
                source_url="https://example.test/complaints.csv",
                source_version="test-snapshot-1",
                downloaded_at_utc="2026-11-22T00:00:00Z",
            )
            self.assertEqual(manifest["source_url"], "https://example.test/complaints.csv")
            self.assertEqual(manifest["source_version"], "test-snapshot-1")
            self.assertEqual(manifest["downloaded_at_utc"], "2026-11-22T00:00:00Z")
            self.assertEqual(manifest["row_count"], 2)

    def test_rejects_inconsistent_row_width(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("id,value\n1,a\n2,b,c\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "expected 2"):
                profile_csv(path)


if __name__ == "__main__":
    unittest.main()
