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

  /* 2 · Neutrals — 5–9 steps, each tinted */
  --color-rule:     oklch(82% 0.010 var(--hue));   /* hairlines, borders */
  --color-neutral:  oklch(56% 0.008 var(--hue));
  --color-muted:    oklch(40% 0.008 var(--hue));   /* secondary text */

  /* 3 · Ink — primary text */
  --color-ink:      oklch(18% 0.010 var(--hue));

  /* 4 · Accent — exactly one, with real chroma */
  --color-accent:   oklch(58% 0.16 45);
  --color-accent-ink: oklch(98% 0.01 45);          /* text ON the accent — see below */
  --color-focus:    oklch(55% 0.19 55);
}
```

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

## The accent budget

One accent. Two maximum. It should occupy **≤3–5% of any given viewport by
area** — count solid fills, large headings set in accent, and full-bleed accent
backgrounds.

The accent is a highlighter, not a colour block. Legitimate uses: active nav
item, focus ring, link underline on hover, a primary CTA's border or text, a
small square anchoring a heading. Not: filling large buttons, setting whole
sections, decorative gradients.

## Contrast: the two failures that actually ship

Both are cases where the model set a background and forgot the foreground.

### 1 · Text on an accent fill

Whenever `--color-accent` fills a surface that carries text, a paired
`--color-accent-ink` must exist, be verified against `--color-accent` (not
against the page background), and be applied as the `color` on that fill.

The bug this prevents: `color: var(--color-ink)` on `background: var(--color-ink)`
— black text on a black button. Quick check: if the computed text colour and the
fill are within **5% lightness and 0.05 chroma** in OKLCH, it fails.

### 2 · Dark section, unswapped ink

Any section or panel whose `background-color` has OKLCH lightness **< 50%** must
also set its text colour in the same rule — typically to `--color-paper` — and
ensure nested children inherit it.

```css
/* wrong — children keep inheriting dark ink */
.panel--inverted { background: var(--color-ink); }

/* right */
.panel--inverted {
  background: var(--color-ink);
  color: var(--color-paper);
}
```

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

## Bans

- Pure `#000` or `#fff` as a base surface.
- Zero-chroma neutrals (unless monochrome is a declared choice).
- Purple→blue, purple→pink, cyan→magenta gradients. Every model reaches for these.
- Gradient fills on text (`background-clip: text`).
- Three-stop gradients. Two stops only.
- Accent as a background fill covering more than ~5% of a view.
- Grey text on a coloured background — always reads washed out.
- Red/green as the only signal. Pair with an icon or shape.
- Alpha transparency as the *definition* of a palette colour. Named tokens are
  opaque; transparency is a modifier for overlays and shadows.
