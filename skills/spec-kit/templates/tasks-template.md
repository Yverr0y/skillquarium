# Tasks: [FEATURE NAME]

**Input**: Design documents from `specs/[###-feature-name]/`

**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories); `research.md`, `data-model.md`, `contracts/` if present

**Tests**: Test tasks are OPTIONAL — include them when the spec asks for them or the project constitution mandates test-first.

**Organization**: Tasks are grouped by user story so each story can be implemented, tested, and delivered independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no dependencies)
- **[Story]**: which user story the task serves (US1, US2, US3 …)
- Every description includes an exact file path

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Adjust to the structure decision recorded in `plan.md`

<!--
  The tasks below are SAMPLES showing the required shape. Replace all of them with
  real tasks derived from the user stories in spec.md, the plan, the data model,
  and the contracts. Do not ship the samples.
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST exist before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work begins until this phase is complete

- [ ] T004 Set up database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Set up API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [What this story delivers]

**Independent Test**: [How to verify this story on its own]

### Tests for User Story 1 *(only if tests were requested)* ⚠️

> Write these FIRST and confirm they FAIL before implementing.

- [ ] T010 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T011 [P] [US1] Integration test for [journey] in tests/integration/test_[name].py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T013 [P] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T014 [US1] Implement [Service] in src/services/[service].py (depends on T012, T013)
- [ ] T015 [US1] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T016 [US1] Add validation and error handling

**Checkpoint**: User Story 1 is fully functional and testable on its own

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [What this story delivers]

**Independent Test**: [How to verify this story on its own]

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US2] Implement [Service] in src/services/[service].py
- [ ] T022 [US2] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T023 [US2] Integrate with User Story 1 components (if needed)

**Checkpoint**: User Stories 1 AND 2 both work independently

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements spanning multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance work across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — start immediately
- **Foundational (Phase 2)**: depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3+)**: all depend on Foundational; then parallel if staffed, otherwise in priority order P1 → P2 → P3
- **Polish (final)**: depends on all desired user stories being complete

### Within Each User Story

- Tests (if included) written and failing before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete and validated before the next priority begins

### Parallel Opportunities

- All `[P]` tasks within a phase can run together
- Once Foundational completes, different user stories can proceed in parallel
- Models within a story marked `[P]` can run together

---

## Implementation Strategy

### MVP First

1. Phase 1: Setup
2. Phase 2: Foundational (blocks everything)
3. Phase 3: User Story 1
4. **STOP and VALIDATE** — test User Story 1 independently
5. Deploy or demo if ready

### Incremental Delivery

Setup + Foundational → US1 (MVP, validate, ship) → US2 (validate, ship) → US3 …
Each story adds value without breaking the ones before it.

---

## Notes

- `[P]` = different files, no dependencies
- `[Story]` maps each task to a user story for traceability
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate a story independently
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence
