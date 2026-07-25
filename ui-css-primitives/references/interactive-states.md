# Interactive states

Most UIs ship `default` and `hover` and call the component done. The remaining
six states are where an interface stops feeling finished.

## First: check whether you should hand-roll this at all

If the project uses **Radix, Base UI, or React Aria**, those primitives already
handle `:focus-visible`, focus trapping, keyboard interaction, and ARIA wiring
correctly — and better than a hand-written version. Per `baseline-ui`: never
rebuild focus or keyboard behaviour by hand unless explicitly asked.

What a primitive does *not* give you is a `loading`, `error`, or `success`
appearance, or the input geometry discipline below. The matrix still applies; you
are styling states the primitive exposes rather than inventing the behaviour.

## The eight states

Every interactive element ships all eight. Not aspirationally — in code.

| State | Signal | Notes |
|---|---|---|
| **default** | Resting appearance | — |
| **hover** | One change, not four | Pointer only; must have a focus equivalent |
| **`:focus-visible`** | Visible ring ≥3:1 contrast | Never animated in |
| **`:active`** | Pressed | `translateY(1px)` or a background shift |
| **disabled** | Three channels — see below | Not opacity alone |
| **loading** | Spinner or skeleton + label | Blocks re-submission |
| **error** | Colour + icon or text, never colour alone | Says how to fix |
| **success** | Usually silent | Only when the effect isn't visible |

Use `:focus-visible`, not `:focus`. `:focus` fires on mouse click too, which is
why people disabled outlines in the first place; `:focus-visible` fires only when
the browser judges a focus ring useful, which is what you actually want.

Never `outline: none` without an equivalent replacement indicator.

## Hover needs a non-hover equivalent

Any affordance revealed only on hover — a menu, a delete button, a tooltip
carrying necessary information — is invisible to touch and keyboard users. Every
hover affordance needs a focus state and must be reachable by tap on coarse
pointers.

```css
@media (hover: hover) and (pointer: fine) {
  .row:hover .row__actions { opacity: 1; }
}
.row:focus-within .row__actions { opacity: 1; }   /* keyboard */
@media (pointer: coarse) {
  .row__actions { opacity: 1; }                   /* touch: always visible */
}
```

## Disabled needs three channels

Opacity alone is ambiguous — it can read as "loading" or just as low-contrast
text. Ship all three:

```css
.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
```

Plus the native `disabled` attribute (or `aria-disabled="true"` when the element
must stay focusable so screen-reader users can discover why it's unavailable).

Note that `opacity` on disabled controls will often drop text below 4.5:1. That
is generally accepted — WCAG 1.4.3 exempts inactive controls — but if the
disabled label carries information the user needs, keep it readable.

## The five input failures

Inputs are where almost-right UIs lose. Each of these is a real bug, not a
preference.

### 1 · `border-width` changes between states

```css
/* wrong — the field grows 1px on focus and shifts everything beside it */
.input:focus { border-width: 2px; }
```

Keep `border-width: 1px` across default, hover, focus, and error. State goes to
`background-color`, `outline`, `box-shadow`, or `border-color`.

### 2 · Focus ring built from `border` instead of `outline`

`border` participates in layout; `outline` does not.

```css
.input {
  border: 1px solid var(--color-rule);
  outline: 2px solid transparent;      /* reserved — no geometry shift later */
  outline-offset: 1px;
}
.input:focus-visible { outline-color: var(--color-focus); }
```

### 3 · Input height ≠ adjacent button height

A 38px input beside a 44px button in the same row is the most common form-tuning
slop. Share one base height token.

```css
:root { --control-h: 2.75rem; }   /* 44px */
.input, .btn { min-height: var(--control-h); }
```

On target size: **WCAG 2.5.8 (AA, 2.2)** requires 24×24 CSS px minimum;
**WCAG 2.5.5 (AAA)** requires 44×44. 44px is the value to design to — it is also
roughly the platform guidance on both iOS and Android — but 24px is the AA
conformance floor, so don't report a 32px control as an AA failure.

### 4 · Helper-text slot collapses when empty

If the helper/error line only exists when there's an error, the page jumps
downward the moment validation fires.

```css
.field__help {
  min-height: 1lh;   /* reserved whether or not there's text */
}
```

`1lh` is the element's own line height — supported in all current browsers. Fall
back to a matching `rem` value if you need older support.

### 5 · Placeholder used as the label

A placeholder disappears on input, fails contrast at typical greys, and leaves
screen-reader users without a persistent name. Ship a real `<label>`. Placeholders
are for format examples (`MM / YY`), not names.

## Error messaging

Three parts, in order:

1. **What happened** — past tense, factual. *"That card was declined."*
2. **Why, if known** — *"Your bank flagged the charge."*
3. **What to do** — imperative. *"Try another card, or contact your bank."*

Never colour-only. Pair the error colour with an icon or text so it survives
colour-vision differences and greyscale.

Never apologetic about the user's input — no "Oops!" on a validation error. A
field that won't accept a value should explain the value, not perform
embarrassment. And no humour in frustration paths: forgot-password,
payment-failed, account-locked.

## A demo harness worth building

For any component with eight states, a throwaway preview page that renders all
eight at once, each labelled, catches more than clicking through them will. Force
the pseudo-states with a parallel class:

```css
.btn:hover,         .btn.is-hover  { background: var(--color-paper-2); }
.btn:focus-visible, .btn.is-focus  { outline-color: var(--color-focus); }
.btn:active,        .btn.is-active { transform: translateY(1px); }
```

Then a page with one row per state. It is not production code — open it, confirm
the component works, delete it.

## Loading copy

- Short wait: spinner, no text.
- Over ~2s: spinner plus "Loading…".
- Over ~10s: progress indication plus an honest label — *"Compiling (this can
  take a minute)."*
