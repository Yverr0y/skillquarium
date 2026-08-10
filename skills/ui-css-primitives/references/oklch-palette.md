# OKLCH palette construction

Why OKLCH: it is perceptually near-uniform, so the `L` channel predicts how light
a colour actually looks and stays stable as you change hue. `hsl()` does not —
`hsl(60 100% 50%)` (yellow) and `hsl(240 100% 50%)` (blue) claim identical
lightness and differ enormously in practice. That single property is what makes a
palette constructible rather than guessed at.

Syntax: `oklch(<L> <C> <H>)` — lightness `0–100%`, chroma `0` to ~`0.37` in
practice, hue `0–360`. Baseline-supported in all current major browsers.

## Pick an anchor hue first

One hue number drives the whole palette. It comes from the brand, the accent, or
the mood. Every neutral then carries a trace of it.

```css
/* anchor hue = 80 (warm oat) */
:root {
  --hue: 80;
}
```

## The four layers

```css
:root {
  /* 1 · Paper — the base surface */
  --color-paper:    oklch(96% 0.012 var(--hue));
  --color-paper-2:  oklch(93% 0.014 var(--hue));   /* raised surface */

  /* 2 · Neutrals — 5–9 steps, each tinted.
   *    Roles are not interchangeable; the ratios below are vs --color-paper. */
  --color-rule:     oklch(82% 0.010 var(--hue));   /* 1.6:1 — DECORATIVE hairlines only */
  --color-border:   oklch(60% 0.020 var(--hue));   /* 3.5:1 — control borders (see note) */
  --color-neutral:  oklch(56% 0.008 var(--hue));   /* 4.1:1 — icons/UI, NOT body text */
  --color-muted:    oklch(40% 0.008 var(--hue));   /* 8.2:1 — secondary text */

  /* 3 · Ink — primary text */
  --color-ink:      oklch(18% 0.010 var(--hue));   /* 16.8:1 */

  /* 4 · Accent — exactly one, with real chroma */
  --color-accent:     oklch(52% 0.16 45);
  --color-accent-ink: oklch(98% 0.01 45);          /* 5.5:1 vs accent — see below */
  --color-focus:      oklch(55% 0.19 55);
}
```

**Two of those roles are load-bearing and easy to conflate.**

`--color-rule` is a *decorative* hairline — a section separator, a table rule. Decorative
boundaries carry no contrast requirement, which is why 1.6:1 is fine for it and
disqualifying for anything else.

`--color-border` is for a boundary that **identifies a control** — an input's edge,
a button outline. When that boundary is the only thing making the control
perceivable, WCAG 1.4.11 requires **3:1** against the adjacent background. Using
`--color-rule` on an input is the failure this split exists to prevent.

`--color-neutral` clears 3:1 but not 4.5:1, so it is a UI/icon colour, not a body
text colour. For text, `--color-muted` is the floor.

Recompute all of these whenever you change the paper lightness — the ratios above
hold for `--color-paper` at `L 96%` and nothing else.

Ranges that work:

| Layer | Light mode | Dark mode |
|---|---|---|
| Paper | `L 96–98%`, `C 0.005–0.015` | `L 12–16%`, `C 0.008–0.015` |
| Ink | `L 16–22%` | `L 92–96%` |
| Neutrals | 5–9 steps between, `C 0.005–0.015` | same |
| Accent | `C 0.12–0.22` | `C` reduced 0.02–0.04, `L` raised 5–10% |

## Two hard rules

**No pure extremes.** `#000` and `#fff` read as flat and synthetic because
nothing in the physical world is either. Use tinted paper and tinted ink.

**No zero-chroma neutrals.** `oklch(56% 0 80)` is a dead grey. Give every neutral
at least `0.005` chroma toward the anchor hue. A page with a warm accent and cool
grey body text looks wrong in a way most people can't name — this is why.

One exception worth knowing: a deliberately monochrome system (the
Stripe/Linear/ElevenLabs school) can run true zero-chroma neutrals as a stated
choice. That is a decision, not a default.

## The accent budget — heuristic, not a rule

> Everything in this section is a **taste heuristic**, not a correctness
> requirement. It is here because it constrains how many tokens you need, not
> because a page violating it is broken. The taste skills own this decision; if
> one of them calls for a saturated full-bleed section, follow it and skip this.

One accent, two at most, occupying a small fraction of any given viewport —
treating it as a highlighter rather than a colour block. Typical uses: active nav
item, focus ring, link underline on hover, a primary CTA's border or text.

The part that *is* a correctness requirement: however much accent you use, every
text and icon sitting on it needs a verified paired foreground. See below.

## Contrast: the two failures that actually ship

Both are cases where the model set a background and forgot the foreground.

### 1 · Text on an accent fill

Whenever `--color-accent` fills a surface that carries text, a paired
`--color-accent-ink` must exist, be verified against `--color-accent` (not
against the page background), and be applied as the `color` on that fill.

The bug this prevents: `color: var(--color-ink)` on `background: var(--color-ink)`
— black text on a black button.

A fast smell test: if the computed text colour and the fill sit within ~5%
lightness and ~0.05 chroma in OKLCH, the pair is almost certainly unusable. That
is a trigger to investigate, **not** a pass/fail rule — WCAG thresholds are
defined on relative-luminance ratios, so the actual ratio still has to be
computed. Nothing here substitutes for that calculation.

### 2 · Dark section, unswapped ink

Any section or panel whose `background-color` has OKLCH lightness **< 50%** must
also set its text colour in the same rule, and ensure nested children inherit it.

Reach for a **token defined for that surface**, not `--color-paper`. Under a dark
theme `--color-paper` *is* the dark value, so hard-coding it here produces
dark-on-dark text in exactly the mode where it's hardest to notice.

```css
/* wrong — children keep inheriting dark ink */
.panel--inverted { background: var(--color-ink); }

/* also wrong — breaks under [data-theme="dark"], where paper is L 14% */
.panel--inverted { background: var(--color-ink); color: var(--color-paper); }

/* right — an explicit pair that is verified in every theme it renders in */
:root, [data-theme="dark"] {
  --color-inverted-surface: oklch(18% 0.010 var(--hue));
  --color-inverted-ink:     oklch(96% 0.006 var(--hue));
}
.panel--inverted {
  background: var(--color-inverted-surface);
  color: var(--color-inverted-ink);
}
```

Declaring the pair once, outside the theme switch, is what keeps it from
inverting along with the rest of the palette.

The common real-world version: a comparison table where the first column is
painted with the accent but the inner cells still use default ink.

## Thresholds

Verify every `(color, background-color)` pair on the page — including inherited
pairs where a card switched its background but not its text.

| Content | WCAG 2.1 (normative) | APCA (informative) |
|---|---|---|
| Body text (<24px regular, <18.66px bold) | **4.5:1** | Lc ≥ 60 |
| Large text (≥24px regular, ≥18.66px bold) | **3:1** | Lc ≥ 45 |
| UI component boundaries, focus rings | **3:1** | Lc ≥ 45 |

**Accuracy note.** APCA models perceived contrast better than WCAG 2.1's ratio,
especially for light text on dark and for thin type. But it is a *candidate*
method — it is not in a published W3C Recommendation, and conformance claims
(VPATs, procurement, most legal requirements) are still made against WCAG 2.x.
Use APCA to make better decisions; use WCAG 2.1 ratios when you have to certify.
Where they disagree, satisfy both.

OKLCH lightness is a useful fast pre-check: if `|L_text − L_bg| < 50%`, the pair
probably fails 4.5:1 — then compute properly rather than trusting it.

## Dark mode

Not an inversion. A separate tuning of the same anchor.

```css
[data-theme="dark"] {
  --color-paper: oklch(14% 0.008 var(--hue));
  --color-ink:   oklch(94% 0.006 var(--hue));
}
```

- **Paper `L 12–18%`**, not `#000`. **Ink `L 92–96%`**, not `#fff`.
- **Reduce body font-weight by ~50 units** (400 → 350). Light type on dark gains
  apparent weight; without this, body copy looks heavier in dark mode. Requires a
  variable font or a matching static weight — don't synthesise.
- **Elevation is lightness, not shadow.** Higher surfaces are *lighter*: add ~3%
  `L` per level. A drop shadow on a dark surface reads as a glow, which is the
  tell.
- **Never change the hue between modes.** Only `L` and `C` move. Switching hue
  makes the two modes read as two different products.

## Correctness requirements

Checkable, and a page violating one is defective:

- **Every text/icon-on-fill pair is computed**, not eyeballed — including pairs
  formed by inheritance when a container changes its background.
- **Red/green as the only signal.** Colour alone fails WCAG 1.4.1; pair it with an
  icon, shape, or text.
- **Gradient fills on text** (`background-clip: text` with `color: transparent`)
  have no computable contrast ratio and degrade to invisible if the background
  fails to paint. Use a solid colour.
- **Alpha transparency as the definition of a palette colour.** A token's value
  should be opaque, because a semi-transparent token's effective contrast depends
  on whatever happens to sit behind it. Transparency is a modifier for overlays
  and shadows.
- **Control boundaries reach 3:1** when the boundary is what makes the control
  perceivable (WCAG 1.4.11).

## Taste heuristics

Defaults worth following absent a reason, but owned by the taste skills — not
defects:

- Pure `#000` / `#fff` as a base surface, and zero-chroma neutrals, both read as
  synthetic. A declared monochrome system is the standing exception.
- Purple→blue, purple→pink, and cyan→magenta gradients are the ones every model
  reaches for.
- Two gradient stops rather than three.
- Grey text on a saturated background tends to read washed out — usually a sign
  the text wants the surface's paired ink token instead.
