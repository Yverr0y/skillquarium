---
title: bulk-rnaseq
aliases:
  - bulk rnaseq
  - FastQC
  - STAR
  - Salmon
  - featureCounts
tags:
  - skill
  - domain/single-cell-rnaseq
domain: single-cell-rnaseq
status: untried
source: skills/bulk-rnaseq/SKILL.md
created: 2026-06-09
---

# bulk-rnaseq

> [!info] What it does
> End-to-end bulk RNA-seq orchestrator — takes raw FASTQ reads through QC and trimming (FastQC, fastp/Trim Galore), alignment and quantification (STAR, Salmon, featureCounts), assembles a gene-level counts matrix, then hands off to differential expression (pydeseq2), pathway/GSEA enrichment (pathway-enrichment), and publication figures (scientific-visualization). Use whenever the user has bulk RNA-seq reads or quant output and wants a complete, reproducible differential-expression workflow — e.g. "analyze my RNA-seq", "FASTQ to DESeq2", "run nf-core/rnaseq", "STAR/Salmon quantification", "build a counts matrix for DESeq2", or "go from reads to differentially expressed genes and enriched pathways". Routes between an nf-core/rnaseq (Nextflow) path and a standalone STAR/Salmon path, and covers experimental design, strandedness, and QC gates. For single-cell RNA-seq use the scanpy skill instead.

**Source:** [skills/bulk-rnaseq/SKILL.md](../../../skills/bulk-rnaseq/SKILL.md)  ·  **Domain:** [Single-Cell, RNA-seq & Functional Genomics](../../maps/single-cell-rnaseq.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [differential-expression](../../notes/single-cell-rnaseq/differential-expression.md) — Bulk transcriptomics differential expression with count-aware modeling, design validation, contrast handling, thresholded exports, and publication-ready DE figures
- [nextflow](../../notes/cloud-devops/nextflow.md) — Build, run, and debug Nextflow data pipelines and nf-core workflows end to end
- [pathway-enrichment](../../notes/single-cell-rnaseq/pathway-enrichment.md) — Run pathway and gene-set enrichment analysis on gene lists or ranked gene data, then interpret the results
- [pydeseq2](../../notes/single-cell-rnaseq/pydeseq2.md) — Differential gene expression analysis for bulk RNA-seq with PyDESeq2, including formulaic designs, Wald tests, FDR correction, LFC shrinkage, and result visualization
- [scanpy](../../notes/single-cell-rnaseq/scanpy.md) — Standard single-cell RNA-seq analysis pipeline
- [scientific-visualization](../../notes/research-writing/scientific-visualization.md) — Meta-skill for publication-ready figures
- [workflow](../../notes/software-dev/workflow.md) — Vercel Workflow DevKit (WDK) expert guidance

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
