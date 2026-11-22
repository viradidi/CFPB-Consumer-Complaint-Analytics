# CFPB Consumer Complaint Analytics — execution record

**Record prepared:** 22 November 2026  
**Current evidence status:** NOT YET ESTABLISHED BY A DATED EXECUTION RECORD

This record is intentionally a truthful evidence register, not a retrospective claim that a run occurred. The repository contains the Fabric notebook, Gold SQL assets, architecture and documentation. The README documents a 903,983-row historical source snapshot and a reconciled Silver/quarantine split. The repository does not currently retain a dated Fabric run record with workspace item IDs, pipeline run IDs, notebook outputs, table counts or DEV-to-PROD promotion evidence.

This does not prove that the project was never executed. It means that the execution history is not independently reconstructable from the committed artifacts currently available.

## 1. Implementation scope to validate

| Stage | Implementation artifact | Acceptance evidence |
|---|---|---|
| Source acquisition | Kaggle historical snapshot / CFPB source | Dataset identity, version, download date, file hash and row/column count |
| Bronze ingestion | Fabric ingestion pipeline and Lakehouse raw file | Pipeline run ID, source path, file size/hash and raw row count |
| Silver transformation | `nb_bronze_to_silver_cfpb_complaints (1).ipynb` | Notebook run ID, valid count, quarantine count and validation outputs |
| Reconciliation | Silver and quarantine outputs | `896,931 + 7,052 = 903,983` for the historical snapshot |
| Gold model | `01_create_gold_tables.sql` | Gold table creation and schema verification |
| Gold load | `02_Create_SP_Load_Gold.sql` / `gold.sp_load_gold` | Stored procedure execution ID/status and fact/dimension row counts |
| Semantic model | Fabric semantic model and DAX | Model refresh/validation evidence and measure spot checks |
| Power BI | Three-page report | Report item identity and screenshots or export showing all three pages render against the expected model |
| Orchestration | End-to-end Fabric Data Pipeline | Pipeline run ID, activity statuses and execution timestamp |
| DEV-to-PROD | Fabric Deployment Pipeline | Promotion operation, target item bindings, target pipeline run and report access verification |

## 2. Required evidence before marking end-to-end execution verified

Record the following for one coherent execution, using the same source snapshot and Fabric environment:

- Repository commit SHA and execution date/time (UTC).
- Fabric tenant/workspace identifiers (redact tenant-specific values if the record is public).
- Source file identity, row/column count and SHA-256 checksum.
- Ingestion pipeline run ID and activity statuses.
- Bronze row count and source-to-Bronze reconciliation.
- Silver notebook run ID, valid-row count, quarantine count and reason counts.
- Gold stored-procedure run status and counts for every dimension and the complaint fact.
- Referential-integrity checks for all fact-to-dimension keys.
- Semantic model refresh status and DAX measure spot checks.
- Power BI report screenshots showing the three documented pages.
- DEV-to-PROD promotion record and post-promotion target binding/report checks.

Keep raw complaint narratives and any sensitive material out of public workflow artifacts. Screenshots and SQL outputs should contain aggregate counts only.

## 3. Execution fields

| Field | Value |
|---|---|
| Repository commit SHA | Not yet recorded |
| Execution date/time (UTC) | Not yet recorded |
| Fabric workspace | Not yet recorded |
| Source dataset URL/version | Not yet recorded |
| Source file SHA-256 | Not yet recorded |
| Source rows / columns | Historical README value: 903,983 / 18; run-specific value not recorded |
| Bronze count | Not yet recorded |
| Silver valid count | Historical README value: 896,931; run-specific value not recorded |
| Quarantine count | Historical README value: 7,052; run-specific value not recorded |
| Gold fact and dimension counts | Not yet recorded |
| End-to-end pipeline run ID | Not yet recorded |
| Semantic model refresh evidence | Not yet recorded |
| Power BI report verification | Not yet recorded |
| DEV-to-PROD promotion evidence | Not yet recorded |
| Final operator acceptance | Pending evidence collection |

## 4. Status rule

Do not mark this record PASS based only on valid notebook JSON, SQL file presence, a passing GitHub Actions workflow, or the documented historical row-count arithmetic. Those checks validate repository consistency and documented expectations. End-to-end acceptance requires the actual Fabric runtime evidence listed above.

Update this record with the original run date and sanitized evidence if the historical execution artifacts can be recovered. Otherwise, complete it during a fresh, reproducible run and clearly label that run as a new snapshot/version.
