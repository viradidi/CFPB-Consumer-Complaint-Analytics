# CFPB Consumer Complaint Analytics — execution record

**Record prepared:** 22 November 2026  
**Current execution status:** OWNER-CONFIRMED SUCCESSFUL FABRIC ENVIRONMENT RUN — 22 NOVEMBER 2026; RUN-SPECIFIC EVIDENCE NOT YET ATTACHED

The project owner confirms that the CFPB solution ran successfully in their Microsoft Fabric environment on 22 November 2026. This closes the previous pending run status at the owner-reported level. The repository contains the Fabric notebook, Gold SQL assets, architecture and documentation; however, the run-specific workspace/item identifiers, pipeline and notebook run IDs, source snapshot hash, Bronze/Silver/Gold counts, semantic-model and report checks, and DEV-to-PROD promotion evidence have not yet been supplied for this record.

The execution is therefore recorded as **owner-confirmed successful**, while independent auditability and reconstruction remain pending until sanitized run artifacts are added. Historical dataset counts in the README are not being presented as measurements from this particular run.

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

## 2. Evidence required for independent verification and audit

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
| Repository commit SHA | Not captured with the owner-reported run |
| Execution date/time (UTC) | 22 November 2026; exact UTC time not supplied |
| Fabric workspace | Not supplied |
| Source dataset URL/version | Not captured for this run; historical Kaggle slug/version remains unresolved |
| Source file SHA-256 | Not supplied |
| Source rows / columns | Historical README value: 903,983 / 18; run-specific values not supplied |
| Bronze count | Not supplied |
| Silver valid count | Historical README value: 896,931; run-specific value not supplied |
| Quarantine count | Historical README value: 7,052; run-specific value not supplied |
| Gold fact and dimension counts | Not supplied |
| End-to-end pipeline run ID | Not supplied |
| Semantic model refresh evidence | Owner reports successful Fabric environment run; refresh artifact not attached |
| Power BI report verification | Not supplied |
| DEV-to-PROD promotion evidence | Not supplied |
| Final operator acceptance | Owner-confirmed successful Fabric environment run; independent evidence package pending |

## 4. Status rule

The project is now recorded as **owner-confirmed successfully run in Microsoft Fabric** on 22 November 2026. This status is based on the project owner's direct confirmation, not on GitHub Actions or static repository checks. Do not describe the run as independently audited or fully reproducible until the actual Fabric runtime evidence listed above is attached.

Add sanitized identifiers and aggregate outputs from the successful run when available. Keep raw complaint narratives and sensitive source content out of public evidence artifacts. If the original source snapshot cannot be identified, retain the existing provenance limitation and clearly label any future reproduction using a new source snapshot/version.
