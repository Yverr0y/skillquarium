# Spec-Driven Development: the reasoning

Distilled from `spec-driven.md` in [github/spec-kit](https://github.com/github/spec-kit).
Read this when you need to justify the method, adapt the templates, or decide whether a
deviation is safe.

## The power inversion

For decades code was the source of truth and specs were scaffolding — written to guide
implementation, then discarded. Because the asset and the implementation were the same
artifact, specs never kept pace, and the gap between intent and code was accepted as
inevitable. Better documentation and stricter process narrowed that gap; nothing closed it.

SDD inverts the relationship. Specifications don't serve code — code serves specifications.
The spec is the primary artifact; code is its expression in a particular language and
framework. The gap disappears not because the spec is more detailed but because the spec
generates the implementation: there is no gap, only transformation.

The consequences follow directly:

- **Maintaining software means evolving specifications**, not patching code and updating docs afterward.
- **Debugging** often means fixing a specification that produced incorrect code.
- **Refactoring** means restructuring the spec for clarity.
- **A pivot** is a regeneration, not a manual rewrite propagated by hand through docs, design, and code.

This is only possible now because models can implement complex specifications reliably. But
raw generation without structure produces chaos — which is what the templates exist to prevent.

## Core principles

**Specifications as the lingua franca.** The spec is the artifact teams review, version,
branch, and merge. Intent is expressed in natural language, design assets, and principles;
code is the last mile.

**Executable specifications.** Precise, complete, and unambiguous enough to generate a
working system. Ambiguity in the spec is a defect, not a detail to sort out later.

**Continuous refinement.** Consistency validation is ongoing, not a one-time gate before
implementation. Analyze the artifacts for ambiguity, contradiction, and gaps repeatedly.

**Research-driven context.** Gather real context during specification — library
compatibility, benchmarks, security implications, organizational constraints — rather than
asserting technical choices from memory.

**Bidirectional feedback.** Production reality feeds back into the spec. A performance
incident becomes a non-functional requirement; a vulnerability becomes a constraint on all
future work.

**Branching for exploration.** The same spec can generate several implementations optimized
for different targets — performance, maintainability, cost — because the spec, not the code,
is the thing being preserved.

## Why the templates constrain the model productively

The templates are not forms. They are prompts engineered to block the specific ways an LLM
degrades a specification.

**1. Preventing premature implementation detail.** The spec template states plainly: focus
on WHAT users need and WHY; avoid HOW. Where a model would jump to "implement using React
with Redux," the template holds it at "users need real-time updates of their data." The
spec then survives changes in technology.

**2. Forcing explicit uncertainty markers.** `[NEEDS CLARIFICATION: specific question]` is
mandatory where no reasonable default exists. This attacks the most damaging LLM failure
mode — the plausible guess. Instead of silently deciding a login system uses email/password,
the model must surface the question. The cap (3 in the spec, 5 in clarification) matters
too: unlimited markers turn the spec into an interrogation and defeat the point of
informed defaults.

**3. Checklists as unit tests for the spec.** "No `[NEEDS CLARIFICATION]` markers remain",
"requirements are testable and unambiguous", "success criteria are measurable" — these force
systematic self-review and catch gaps that free-form re-reading misses.

**4. Gates with justification.** Simplicity and anti-abstraction gates in the plan make
over-engineering visible at design time. A failed gate is not forbidden — it must be
recorded in the Complexity Tracking table with the reason and the rejected simpler
alternative. Complexity becomes accountable rather than invisible.

**5. Hierarchical detail management.** The plan stays high-level and readable; code samples,
algorithms, and long schemas move to `research.md`, `data-model.md`, and `contracts/`. This
prevents the common failure where a specification becomes an unreadable code dump.

**6. Test-first ordering.** Contracts first, then tests (contract → integration → e2e →
unit), then source. The ordering constraint forces thinking about testability and interface
before implementation.

**7. No speculative features.** "No speculative or 'might need' features"; every feature
traces to a concrete user story with acceptance criteria. This stops the accretion of
nice-to-haves that complicate implementation and were never asked for.

Together these produce specifications that are complete, unambiguous, testable,
maintainable, and implementable — turning the model from a creative writer into a
disciplined specification engineer.

## The constitutional foundation

At the center sits a constitution: principles that govern how specifications become code.
It is the architectural DNA — the reason implementations generated months apart, or by
different models, remain compatible.

Spec Kit's reference articles, worth understanding even when you write your own:

- **Library-first** — every feature begins as a standalone library, forcing modular design and clear boundaries from the start.
- **CLI interface** — every library exposes text-in/text-out functionality, so nothing hides inside opaque classes and everything is observable and testable.
- **Test-first (non-negotiable)** — no implementation before tests are written, approved, and confirmed failing. This inverts the usual generate-and-hope loop.
- **Project-defined articles** — deliberately left to each project: integration testing, observability, versioning, security boundaries, whatever this system actually requires.
- **Simplicity and anti-abstraction** — cap the project count, justify additional structure, use frameworks directly instead of wrapping them, keep a single model representation.
- **Integration-first testing** — realistic environments over mocks; real databases and service instances; contract tests before implementation.

The power is in immutability. Implementation details evolve freely; the principles do not.
That gives consistency across time, consistency across models, architectural integrity, and
quality guarantees that don't depend on whoever happens to be reviewing.

Principles are stable, not frozen. Amendment requires a documented rationale, maintainer
approval, and a backwards-compatibility assessment — the method learns without drifting.

Beyond rules, the constitution is a stance: observability over opacity, simplicity over
cleverness, integration over isolation, modularity over monoliths.

## What this is not

It is not about replacing developers or automating creativity. It is about amplifying human
capability by automating the mechanical translation from intent to implementation, and
creating a feedback loop where specification, research, and code evolve together.
