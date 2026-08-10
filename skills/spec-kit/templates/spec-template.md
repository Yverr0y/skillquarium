# Feature Specification: [FEATURE NAME]

**Feature Directory**: `specs/[###-feature-name]`

**Created**: [DATE]

**Status**: Draft

**Input**: User description: "[original feature description, verbatim]"

## User Scenarios & Testing *(mandatory)*

<!--
  User stories are PRIORITIZED user journeys, ordered by importance.
  Each story must be INDEPENDENTLY TESTABLE — if you implement just ONE of them,
  you still have a viable MVP that delivers value.

  Assign priorities (P1, P2, P3, ...), P1 being most critical. Each story must be:
  - developed independently
  - tested independently
  - deployed independently
  - demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[The user journey in plain language]

**Why this priority**: [The value it delivers and why it ranks here]

**Independent Test**: [How this is verified on its own — "Can be fully tested by [action] and delivers [value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[The user journey in plain language]

**Why this priority**: [The value it delivers and why it ranks here]

**Independent Test**: [How this is verified on its own]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!-- Replace with the real edge cases for this feature. -->

- What happens when [boundary condition]?
- How does the system handle [error scenario]?

## Requirements *(mandatory)*

### Functional Requirements

<!-- Each requirement must be testable. Keep IDs stable — plan and tasks reference them. -->

- **FR-001**: System MUST [specific capability, e.g. "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g. "validate email addresses"]
- **FR-003**: Users MUST be able to [key interaction, e.g. "reset their password"]
- **FR-004**: System MUST [data requirement, e.g. "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g. "log all security events"]

*Marking a genuinely unresolvable ambiguity (maximum 3 in the whole spec):*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified — email/password, SSO, OAuth?]

### Key Entities *(include only if the feature involves data)*

- **[Entity 1]**: [What it represents, key attributes — no implementation types]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!-- Measurable and technology-agnostic. No frameworks, databases, or internal metrics. -->

### Measurable Outcomes

- **SC-001**: [e.g. "Users can complete account creation in under 2 minutes"]
- **SC-002**: [e.g. "System handles 1000 concurrent users without degradation"]
- **SC-003**: [e.g. "90% of users complete the primary task on first attempt"]
- **SC-004**: [e.g. "Support tickets related to [X] drop by 50%"]

## Assumptions

<!-- Every reasonable default you chose instead of asking a question belongs here. -->

- [Assumption about target users, e.g. "Users have stable internet connectivity"]
- [Assumption about scope, e.g. "Mobile support is out of scope for v1"]
- [Assumption about data/environment, e.g. "The existing authentication system is reused"]
- [Dependency on an existing system, e.g. "Requires access to the user profile API"]
