# Skill Toggle Multi-Selection Design

## Goal

Allow users to mark multiple visible skills and apply normalized Claude Code,
Codex, or combined invocation-state changes from the existing OpenTUI interface.
Preserve the current single-skill workflow when no rows are marked.

## Interaction

- The current cursor row remains separate from the marked set and continues to
  control the Details panel.
- `M` marks or unmarks the current row.
- A fixed-width selection column displays `[x]` for marked rows and `[ ]` for
  unmarked rows without shifting the existing columns.
- `C`, `X`, and Space target all marked rows. When no rows are marked, they
  target only the current cursor row, matching the existing behavior.
- A skill with a catalog error cannot be marked.
- Search or filter changes remove marks for skills that are no longer visible,
  so a batch action never modifies a hidden skill.

## Batch Toggle Semantics

Batch actions normalize the target set:

- Claude: if every target has Claude enabled, disable Claude for all targets;
  otherwise enable Claude for all targets.
- Codex: if every target has Codex enabled, disable Codex for all targets;
  otherwise enable Codex for all targets.
- Both: if every target has both products enabled, disable both products for
  all targets; otherwise enable both products for all targets.

## Components and Data Flow

The TUI owns a set of marked skill keys alongside the existing cursor key.
Filtering intersects that set with the visible catalog keys. A batch action
resolves its targets from the marked set, falling back to the cursor key, and
derives one normalized enabled value from the current catalog records.

The backend interface accepts all target keys in one operation. The Python CLI
already accepts multiple skill names for enable and disable commands, so the
OpenTUI backend sends one process invocation and refreshes the catalog once
after it succeeds.

## Error Handling

The TUI prevents known catalog-error rows from entering the marked set. If the
backend command fails, the catalog is not refreshed and the error is shown in
the message area. A successful operation reports the product, resulting state,
and number of affected skills.

## Testing

Renderer tests will cover marking and unmarking with `M`, fixed selection-column
rendering, normalized mixed-state batch toggles, the cursor fallback when no
rows are marked, and removal of hidden marks after filtering. Backend tests will
verify that multiple keys are passed through one enable or disable command.
