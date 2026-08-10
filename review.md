---
title: review
tags:
  - skill
  - domain/software-dev
domain: software-dev
status: untried
source: skills/review/SKILL.md
created: 2026-06-20
---

# review

> [!info] What it does
> Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".

**Source:** [skills/review/SKILL.md](skills/review/SKILL.md)  ·  **Domain:** [Software Development & Engineering](maps/software-dev.md)  ·  **Table:** [skills.base](skills.base)  ·  **Index:** [Skills Index](index.md)

## Related skills

- [academic-paper-reviewer](academic-paper-reviewer.md) — Multi-perspective academic paper review with dynamic reviewer personas
- [academic-pipeline](academic-pipeline.md) — Orchestrator for the full academic research pipeline: research -> write -> integrity check -> review -> revise -> re-review -> re-revise -> final integrity check -> finalize
- [accessibility-and-inclusive-visualization](accessibility-and-inclusive-visualization.md) — Make data visualizations accessible and inclusive
- [audit-context-building](audit-context-building.md) — Understand a codebase before looking for bugs in it - what each function assumes, what it guarantees, and what it depends on elsewhere
- [audit-prep-assistant](audit-prep-assistant.md) — Prepares codebases for security review using Trail of Bits' checklist
- [author-component](author-component.md) — Create or review Blazor components (.razor files) with correct architecture
- [authoring-github-workflows](authoring-github-workflows.md) — Author and review GitHub Actions workflow YAML safely so syntactically-valid YAML can't ship a workflow that GitHub Actions refuses to run
- [bio-human-feedback](bio-human-feedback.md) — Phase 2.6 of the bio-manuscript pipeline: human review checkpoint
- [bio-manuscript-refine](bio-manuscript-refine.md) — Refinement loop for the bio-manuscript pipeline: three-reviewer iterative optimization (editor, computational, biological)
- [c-review](c-review.md) — Performs comprehensive C/C++ security review for memory corruption, integer overflows, race conditions, and platform-specific vulnerabilities
- [cavecrew](cavecrew.md) — Decision guide for delegating to caveman-style subagents
- [caveman-review](caveman-review.md) — Ultra-compressed code review comments. Cuts noise from PR feedback while preserving the actionable signal
- [cell-annotation](cell-annotation.md) — Automated and marker-guided single-cell cell type annotation using CellTypist, marker review, reference transfer, and confidence-aware label curation
- [chatgpt-app-submission](chatgpt-app-submission.md) — Inspect a ChatGPT Apps MCP server codebase and generate chatgpt-app-submission.json with app info suggestions, tool hint justifications, test cases, and negative test cases, then...
- [check-pr](check-pr.md) — Checks a GitHub, GitLab, or Perforce (p4) pull request (or merge request, or shelved changelist) for unresolved review comments, failing status checks, and incomplete PR descriptions
- [chip-seq](chip-seq.md) — ChIP-seq peak calling and downstream interpretation with MACS3, signal track export, annotation, motif analysis, and differential binding review
- [chronograph-gp-meeting-prep](chronograph-gp-meeting-prep.md) — Prepare an LP to meet with their fund manager (GP): review the fund's latest reporting, surface what changed since last period, and draft the questions worth raising
- [code-review](code-review.md) — Reviews code changes using CodeRabbit AI
- [code-review-and-quality](code-review-and-quality.md) — Conducts multi-axis code review. Use before merging any change
- [crewai](crewai.md) — Role-based multi-agent orchestration framework for building "Crews" of collaborating LLM agents (each with a role, goal, backstory, and optional tools) that execute sequential or...
- [deep-research](deep-research.md) — Universal deep research agent team. 13-agent pipeline for rigorous academic research on any topic
- [detect-static-dependencies](detect-static-dependencies.md) — Scan C# source files for hard-to-test static dependencies — DateTime.Now/UtcNow, File.*, Directory.*, Environment.*, HttpClient, Console.*, Process.*, and other untestable statics
- [differential-review](differential-review.md) — Performs security-focused differential review of code changes (PRs, commits, diffs)
- [document-quality-check](document-quality-check.md) — Document Quality Check skill for Datasite deal rooms
- [dogfood](dogfood.md) — Systematically explore and test a web application to find bugs, UX issues, and other problems
- [doubt-driven-development](doubt-driven-development.md) — Subjects every non-trivial decision to a fresh-context adversarial review before it stands
- [durable-objects](durable-objects.md) — Create and review Cloudflare Durable Objects
- [eod-wrapup](eod-wrapup.md) — Generates an end-of-day wrap-up using the Superhuman Mail MCP server — identifies open loops, unanswered emails, and action items from your day so you can leave work with a clear head
- [executing-plans](executing-plans.md) — Use when you have a written implementation plan to execute in a separate session with review checkpoints
- [exp-mock-usage-analysis](exp-mock-usage-analysis.md) — Audits .NET test mock usage by tracing each mock setup through the production code's execution path to find dead, unreachable, redundant, or replaceable mocks
- [figma-create-new-file](figma-create-new-file.md) — **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `create_new_file` tool call
- [game-playtest](game-playtest.md) — Run browser-game playtests and frontend QA
- [gh-address-comments](gh-address-comments.md) — Address actionable GitHub pull request review feedback
- [google-calendar](google-calendar.md) — Manage scheduling and conflicts in connected Google Calendar data
- [google-drive-comments](google-drive-comments.md) — Write, reply to, and resolve Google Drive comments on Docs, Sheets, Slides, and Drive files with evidence-backed location context
- [greploop](greploop.md) — Iteratively improves a PR (GitHub), MR (GitLab), or shelved changelist (Perforce) until Greptile gives it a 5/5 confidence score with zero unresolved comments
- [guidelines-advisor](guidelines-advisor.md) — Smart contract development advisor based on Trail of Bits' best practices
- [hunk-review](hunk-review.md) — Interacts with live Hunk diff review sessions via CLI
- [improve-ui](improve-ui.md) — Audit an existing product surface against its own design evidence, identify verified UI problems, and write self-contained implementation plans for another agent
- [infographics](infographics.md) — Create professional infographics using Nano Banana Pro AI with smart iterative refinement
- [launch-readiness-orchestrator](launch-readiness-orchestrator.md) — Launch Readiness Orchestrator skill for Datasite deal rooms
- [liquid-glass](liquid-glass.md) — Implement and review macOS SwiftUI Liquid Glass UI
- [matlab-review-code](matlab-review-code.md) — Review MATLAB code for quality, performance, maintainability, and adherence to MathWorks coding standards
- [morph-ppt](morph-ppt.md) — Use this skill when the user wants a .pptx with smooth cross-slide animation — PowerPoint Morph transitions, Keynote-style continuous motion, shapes that grow / move / rotate as the...
- [msbuild-antipatterns](msbuild-antipatterns.md) — Detect and fix MSBuild anti-patterns in project and build files
- [nature-figure](nature-figure.md) — Create, revise, audit, and export submission-grade scientific figures for Nature-family and other high-impact venues in Python (matplotlib/seaborn) or R...
- [nature-reviewer](nature-reviewer.md) — Simulate a Nature-style reviewer assessment from the referee perspective rather than an author rebuttal
- [neuropixels-analysis](neuropixels-analysis.md) — Analyze Neuropixels extracellular recordings end-to-end with SpikeInterface
- [ngs-bcl-to-fastq](ngs-bcl-to-fastq.md) — Validate Illumina BCL run folders and sample sheets, plan demultiplexing, review index/UMI/lane choices, run BCL-to-FASTQ conversion, and interpret demux metrics while surfacing...
- [officecli-pitch-deck](officecli-pitch-deck.md) — Use this skill when the user is building a fundraising / investor pitch deck — seed, Series A / B / C, convertible note, SAFE round, strategic raise
- [openai-ads-conversions-setup](openai-ads-conversions-setup.md) — Guide Codex through instrumenting or extending repositories with OpenAI Ads Measurement Pixel and optional Conversions API (CAPI)
- [peer-review](peer-review.md) — Systematic peer review toolkit. Evaluate methodology, statistics, design, reproducibility, ethics, figure integrity, reporting standards, for manuscript and grant review across...
- [phoenix-cli](phoenix-cli.md) — Debug LLM applications using the Phoenix CLI
- [pre-submission-reviewer](pre-submission-reviewer.md) — Runs a pre-submission review of a technical paper across five dimensions: macro logic, writing details, English grammar, LaTeX formatting, and figure quality
- [receiving-code-review](receiving-code-review.md) — Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification...
- [research-grants](research-grants.md) — Write competitive research proposals for NSF, NIH, DOE, and DARPA
- [risk-analysis-audit](risk-analysis-audit.md) — Risk Analysis Audit skill for Datasite deal rooms
- [scientific-schematics](scientific-schematics.md) — Create publication-quality scientific diagrams using Nano Banana 2 AI with smart iterative refinement
- [scrna-seq-qc](scrna-seq-qc.md) — Process, quality-control, annotate, and visualize single-cell or single-nucleus RNA-seq datasets across tissues and species
- [sds-gel-review](sds-gel-review.md) — Review SDS-PAGE or protein purification gel images using DNA sequence, protein sequence, base-pair length, expected protein size, and lane labels
- [security-diff-scan](security-diff-scan.md) — Use when the user asks for a security review of a pull request, commit, branch diff, working-tree patch, or other Git-backed change set
- [security-scan](security-scan.md) — Use for a standard, single-pass security audit of an entire repository or a scoped path, package folder, or submodule with no diff to review
- [sharepoint](sharepoint.md) — Inspect Microsoft SharePoint context, discover the right site or library, and prepare safe changes
- [sharepoint-powerpoint](sharepoint-powerpoint.md) — Create, edit, restyle, and review PowerPoint `.pptx` files fetched from SharePoint, with emphasis on style preservation, slide cloning, theme-aware updates, and rendered visual QA
- [shopify-app-store-review](shopify-app-store-review.md) — Run a pre-submission compliance check against your Shopify app's codebase
- [swiftui-liquid-glass](swiftui-liquid-glass.md) — Implement and review iOS 26+ SwiftUI Liquid Glass UI
- [teams-planner-task-management](teams-planner-task-management.md) — Review and manage Microsoft Planner tasks from Teams workflows
- [test-anti-patterns](test-anti-patterns.md) — Audits an existing test file or suite in any language for anti-patterns and quality issues — produces a severity-ranked report (Critical/Warning/Info)
- [use-js-interop](use-js-interop.md) — Add, review, or fix JavaScript interop in Blazor components
- [vdr-index-setup](vdr-index-setup.md) — VDR Index Setup skill for Datasite deal rooms
- [vercel-agent](vercel-agent.md) — Vercel Agent guidance — AI-powered code review, incident investigation, and SDK installation
- [web-design-guidelines](web-design-guidelines.md) — Review UI code for Web Interface Guidelines compliance
- [wix-app](wix-app.md) — Build and review Wix CLI app extensions — dashboard pages, modals, plugins, menu plugins, custom element widgets, Editor React components, site plugins, embedded scripts, backend APIs...
- [writing-mstest-tests](writing-mstest-tests.md) — Write, create, modernize, or fix comprehensive MSTest unit tests with MSTest 3.x/4.x APIs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
