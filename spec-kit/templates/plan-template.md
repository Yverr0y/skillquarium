# Implementation Plan: [FEATURE]

**Feature Directory**: `specs/[###-feature-name]` | **Date**: [DATE] | **Spec**: [link to spec.md]

## Summary

[Primary requirement from the spec + the technical approach chosen, in a few sentences]

## Technical Context

<!-- Replace with real values. Anything genuinely unknown stays NEEDS CLARIFICATION — do not invent numbers. -->

**Language/Version**: [e.g. Python 3.11, Swift 5.9, Rust 1.75, or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g. FastAPI, UIKit, LLVM, or NEEDS CLARIFICATION]

**Storage**: [e.g. PostgreSQL, files, or N/A]

**Testing**: [e.g. pytest, XCTest, cargo test, or NEEDS CLARIFICATION]

**Target Platform**: [e.g. Linux server, iOS 15+, WASM, or NEEDS CLARIFICATION]

**Project Type**: [e.g. library / CLI / web service / mobile app / desktop app]

**Performance Goals**: [domain-specific, e.g. 1000 req/s, 10k lines/sec, 60 fps]

**Constraints**: [domain-specific, e.g. <200ms p95, <100MB memory, offline-capable]

**Scale/Scope**: [domain-specific, e.g. 10k users, 50 screens]

## Constitution Check

*GATE: must pass before research. Re-check after the design below is filled in.*

<!--
  Derive these gates from the project constitution at .specify/memory/constitution.md.
  The examples below are the common shapes — replace them with this project's principles.
-->

### Simplicity Gate

- [ ] Using ≤3 projects?
- [ ] No future-proofing?

### Anti-Abstraction Gate

- [ ] Using the framework directly rather than wrapping it?
- [ ] Single model representation?

### Integration-First Gate

- [ ] Contracts defined?
- [ ] Contract tests written?

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── spec.md              # WHAT and WHY
├── plan.md              # This file
├── research.md          # Option comparisons, benchmarks (optional)
├── data-model.md        # Entities and relationships (optional)
├── quickstart.md        # Key validation scenarios (optional)
├── contracts/           # API/event contracts (optional)
└── tasks.md             # Executable task list (written in the tasks phase)
```

### Source Code (repository root)

<!--
  Replace the placeholder tree with the concrete layout for this feature.
  Delete the unused options and expand the chosen one with real paths.
  The delivered plan must not contain "Option" labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application
backend/
├── src/{models,services,api}/
└── tests/

frontend/
├── src/{components,pages,services}/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API
api/
└── [same as backend above]

ios/ or android/
└── [feature modules, UI flows, platform tests]
```

**Structure Decision**: [Which structure was chosen and why, referencing the real directories above]

## Complexity Tracking

> Fill in **only** if the Constitution Check has violations that must be justified.
> An empty justification means the design should be simplified instead.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| [e.g. 4th project] | [current need] | [why 3 projects are insufficient] |
| [e.g. repository pattern] | [specific problem] | [why direct DB access is insufficient] |
