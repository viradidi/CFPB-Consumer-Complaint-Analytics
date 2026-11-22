"""Repository-level contracts for the CFPB Fabric project.

These tests validate committed artifacts and documented contracts. They do not
execute Microsoft Fabric, Spark, Warehouse SQL, semantic models or Power BI.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "nb_bronze_to_silver_cfpb_complaints (1).ipynb"
README = ROOT / "README.md"
GOLD_DDL = ROOT / "01_create_gold_tables.sql"
GOLD_LOAD = ROOT / "02_Create_SP_Load_Gold.sql"
ARCHITECTURE = ROOT / "architecture" / "cfpb-consumer-complaint-analytics.webp"


class RepositoryContractTests(unittest.TestCase):
    def test_bronze_to_silver_notebook_is_valid_json_with_code_cells(self):
        self.assertTrue(NOTEBOOK.is_file(), "Expected Fabric notebook is missing.")
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        self.assertIsInstance(notebook.get("cells"), list)
        code_cells = [
            cell for cell in notebook["cells"]
            if cell.get("cell_type") == "code"
        ]
        self.assertGreater(len(code_cells), 0, "Notebook has no code cells.")
        for index, cell in enumerate(code_cells):
            source = cell.get("source", [])
            source_text = "".join(source) if isinstance(source, list) else str(source)
            self.assertTrue(
                source_text.strip(),
                f"Notebook code cell {index} is empty.",
            )

    def test_original_architecture_asset_is_present(self):
        self.assertTrue(ARCHITECTURE.is_file())
        self.assertGreater(ARCHITECTURE.stat().st_size, 1000)
        readme = README.read_text(encoding="utf-8")
        self.assertIn("architecture/cfpb-consumer-complaint-analytics.webp", readme)

    def test_gold_schema_contains_fact_and_dimensions(self):
        sql = GOLD_DDL.read_text(encoding="utf-8").upper()
        required_tables = (
            "GOLD.DIM_DATE",
            "GOLD.DIM_PRODUCT",
            "GOLD.DIM_ISSUE",
            "GOLD.DIM_COMPANY",
            "GOLD.DIM_LOCATION",
            "GOLD.DIM_CHANNEL",
            "GOLD.DIM_RESPONSE",
            "GOLD.FACT_COMPLAINT",
        )
        for table in required_tables:
            with self.subTest(table=table):
                self.assertIn(table, sql)

    def test_gold_loader_has_expected_procedure_and_fact_load(self):
        sql = GOLD_LOAD.read_text(encoding="utf-8").upper()
        self.assertIn("CREATE OR ALTER PROCEDURE GOLD.SP_LOAD_GOLD", sql)
        self.assertIn("INSERT INTO GOLD.FACT_COMPLAINT", sql)
        self.assertIn("FROM LH_CFPB_COMPLAINTS.SILVER.CONSUMER_COMPLAINTS", sql)
        self.assertIn("TRUNCATE TABLE GOLD.FACT_COMPLAINT", sql)

    def test_documented_historical_reconciliation_is_arithmetic(self):
        readme = README.read_text(encoding="utf-8")
        self.assertRegex(readme, r"896,931\s*\+\s*7,052\s*=\s*903,983")
        self.assertEqual(896_931 + 7_052, 903_983)

    def test_source_provenance_disclosure_is_present_and_no_placeholder_remains(self):
        readme = README.read_text(encoding="utf-8")
        provenance = (ROOT / "docs" / "DATA_PROVENANCE.md").read_text(encoding="utf-8")
        self.assertIn("https://www.consumerfinance.gov/data-research/consumer-complaints/", provenance)
        self.assertIn("exact Kaggle dataset", provenance.lower())
        self.assertNotIn("Add the exact dataset URL", readme)
        self.assertIn("docs/DATA_PROVENANCE.md", readme)

    def test_execution_record_does_not_claim_unrecorded_runtime_success(self):
        execution = (ROOT / "docs" / "EXECUTION_RECORD.md").read_text(encoding="utf-8")
        self.assertIn("NOT YET ESTABLISHED BY A DATED EXECUTION RECORD", execution)
        self.assertIn("Do not mark this record PASS", execution)


if __name__ == "__main__":
    unittest.main()
