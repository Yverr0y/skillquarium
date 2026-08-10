---
title: Germline variant interpretation
tags:
  - recipe
  - domain/genomics-variants
created: 2026-06-09
---

# Germline variant interpretation

> [!abstract] Goal
> Take a VCF to an annotated, ACMG/AMP-classified, ranked clinical report.

[Back to Recipes](index.md)  ·  [Skill Index](../index.md)

## Pipeline

```mermaid
flowchart LR
  A[VCF] --> B[Sample QC] --> C[Annotate: VEP / ClinVar / gnomAD] --> D[ACMG/AMP classify] --> E[Clinical report]
```

## Steps

1. **[sample-qc-triage](../notes/genomics-variants/sample-qc-triage.md)** — identity, sex, contamination, batch-shift checks (optional but recommended).
2. **[vcf-annotator](../notes/genomics-variants/vcf-annotator.md)** — Ensembl VEP + ClinVar + gnomAD annotation and impact ranking. Alternative: **[variant-annotation](../notes/genomics-variants/variant-annotation.md)**.
3. **[clinical-variant-reporter](../notes/genomics-variants/clinical-variant-reporter.md)** — ACMG/AMP 2015 classification with per-variant evidence.
4. **[wes-clinical-report-en](../notes/clinical-medical/wes-clinical-report-en.md)** — clinical PDF report. Spanish: **[wes-clinical-report-es](../notes/clinical-medical/wes-clinical-report-es.md)**.

## Add-ons

- **[pharmgx-reporter](../notes/clinical-medical/pharmgx-reporter.md)** — pharmacogenomic findings.
- **[clinical-trial-finder](../notes/clinical-medical/clinical-trial-finder.md)** — matching trials for a gene/variant/condition.
- Low-level VCF/BAM handling: **[pysam](../notes/genomics-variants/pysam.md)**.
