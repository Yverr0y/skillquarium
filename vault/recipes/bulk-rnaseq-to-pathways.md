---
title: Bulk RNA-seq → pathways
tags:
  - recipe
  - domain/single-cell-rnaseq
created: 2026-06-09
---

# Bulk RNA-seq → pathways

> [!abstract] Goal
> Take raw bulk RNA-seq reads through QC and quantification to differentially expressed genes, enriched pathways, and a publication-ready figure.

[Back to Recipes](index.md)  ·  [Skill Index](../index.md)

## Pipeline

```mermaid
flowchart LR
  A[FASTQ reads] --> B[QC + align + quantify] --> C[Counts matrix] --> D[Differential expression] --> E[Pathway enrichment] --> F[Figure]
```

## Steps

1. **[bulk-rnaseq](../notes/single-cell-rnaseq/bulk-rnaseq.md)** — orchestrate FASTQ → counts (QC, trimming, alignment, quantification). Alternative: **[nfcore-rnaseq-wrapper](../notes/single-cell-rnaseq/nfcore-rnaseq-wrapper.md)**.
2. **[pydeseq2](../notes/single-cell-rnaseq/pydeseq2.md)** — differential expression on the counts matrix. Alternative: **[rnaseq-de](../notes/single-cell-rnaseq/rnaseq-de.md)**.
3. **[pathway-enrichment](../notes/single-cell-rnaseq/pathway-enrichment.md)** — GSEA / over-representation on the DE gene list. Alternative: **[pathway-enricher](../notes/single-cell-rnaseq/pathway-enricher.md)**.
4. **[scientific-visualization](../notes/research-writing/scientific-visualization.md)** — volcano / heatmap / enrichment figures. Alternative: **[diff-visualizer](../notes/single-cell-rnaseq/diff-visualizer.md)**.

## Add-ons

- **[multiqc-reporter](../notes/sequence-phylogenetics/multiqc-reporter.md)** — aggregate QC across samples.
- **[de-summary](../notes/single-cell-rnaseq/de-summary.md)** — narrative summary of the DE results.
