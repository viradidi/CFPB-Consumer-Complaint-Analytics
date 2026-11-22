# CFPB project — data provenance and reproducibility

## Snapshot used by the implementation

The project README records the historical input snapshot as:

| Measure | Recorded value |
|---|---:|
| Source rows | 903,983 |
| Source columns | 18 |
| Valid Silver rows | 896,931 |
| Quarantined rows | 7,052 |

The project reconciliation is:

`896,931 + 7,052 = 903,983`

These figures describe the snapshot used when the project was built. They are not a claim about the size of the live CFPB database today.

## Source authority

The underlying complaint data originates from the U.S. Consumer Financial Protection Bureau (CFPB):

- [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
- [Current CFPB bulk CSV export](https://files.consumerfinance.gov/ccdb/complaints.csv.zip)
- [CFPB database API release notes](https://cfpb.github.io/api/ccdb/release-notes.html)
- [CFPB field reference](https://cfpb.github.io/api/ccdb/fields.html)

The project README records that the historical snapshot was retrieved through Kaggle. However, the exact Kaggle dataset slug, version identifier, download date and source-file checksum were not retained in the committed repository. The exact Kaggle page therefore cannot be established from the current repository contents, and this document deliberately does not guess one.

The official CFPB bulk export is provided as the authoritative source for a fresh reproduction. It is a changing source, not a byte-for-byte replacement for the original historical snapshot. The CFPB release notes document schema changes over time, including removal of fields that existed in older complaint exports. A current download may therefore differ from the historical 18-column input in both row count and available columns.

## What is and is not reproducible from Git

**Available in the repository**

- The Fabric Bronze-to-Silver notebook.
- Gold table definitions and the Gold loading stored procedure.
- The original architecture graphic and mapping/reference files.
- The documented historical row counts and Silver/quarantine reconciliation.

**Not retained in the repository**

- The exact Kaggle dataset page and version.
- The downloaded source CSV or immutable archive.
- Download timestamp and source-file SHA-256 checksum.
- Original Fabric workspace item IDs and complete execution exports.

Consequently, the transformation and modelling implementation can be inspected, but the exact original source snapshot cannot currently be fetched deterministically from the repository alone.

## Recommended provenance completion

Before describing the original input as fully reproducible, recover and record:

1. The original Kaggle URL and dataset slug.
2. The Kaggle dataset version or version date.
3. The downloaded source filename and byte size.
4. The source file SHA-256 checksum.
5. The download date and the observed source row/column counts.

If the original Kaggle version cannot be recovered, retain that fact and use a newly downloaded CFPB snapshot as a separately versioned reproduction. Do not compare its row counts directly with the historical 903,983-row snapshot without documenting the source-version difference.
