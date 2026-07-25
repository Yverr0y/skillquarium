# Type ceiling

Structural constraints on type. No opinion here about *which* faces express which
mood — that belongs to the taste skills. These are the countable rules.

## The 2+1 rule — three families is the ceiling

A page may use at most **three** distinct font families:

- one **display** — headings, hero
- one **body** — prose, UI
- one optional **outlier** — a single typographic register for the wordmark, a
  hero stat, a pull quote, or a masthead

```css
:root {
  --font-display: "Fraunces", ui-serif, Georgia, serif;
  --font-body:    "Geist", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "Geist Mono", ui-monospace, monospace;   /* ≤2 slots */
}
```

Counting rules:

- **Same family at different weights is one family.** Geist 400 + Geist 700 is
  one. Pairing it with Fraunces is two.
- **Mono counts.** If mono appears anywhere — code blocks, captions, numerals —
  it is the outlier slot. Don't then add a fourth.
- **The outlier appears in ≤2 places on the whole page.** Wordmark + hero stat.
  Or pull quote + masthead. Reaching for a third slot means you have a third body
  font, which is the thing this rule exists to prevent.
- **The outlier carries one role.** Once it tags a kind of content, every
  instance of that content uses it. Not one button label but not another.

Two families is the right answer for most pages. Three is the ceiling, not a
target.

## Scale is a ratio, not increments

Pick one ratio and build from a 16px body: major third `1.25`, perfect fourth
`1.333`, perfect fifth `1.5`, or golden `1.618`.

```css
:root {
  --text-xs:   0.64rem;
  --text-sm:   0.8rem;
  --text-base: 1rem;
  --text-md:   1.25rem;
  --text-lg:   1.5625rem;
  --text-xl:   1.9531rem;
  --text-2xl:  2.4414rem;
  --text-3xl:  3.0518rem;
  --text-4xl:  3.8147rem;
  --text-display: clamp(2.75rem, 5vw + 1rem, 5.25rem);
}
```

**Use no more than five sizes on a page.** If you need more hierarchy, reach for
weight and colour, not another size.

If the project uses Tailwind, its default scale already satisfies this. Use it
rather than introducing a parallel set of tokens.

## Display cap and headline sizing

Cap display type at ~**5.5rem (88px)**. Above that, headlines crowd themselves at
1280–1440px viewports and need multi-line wrapping that reads as drama rather
than emphasis. Display-heavy treatments can push to 6rem; a single short word
(a stat, ≤12ch) can go to 7rem.

Then match size to copy length — count characters in the rendered `h1`:

| Headline length | Cap |
|---|---|
| ≤20 chars | full `--text-display`; a single word can grow further |
| **21–50 chars** (the sweet spot) | `--text-display` |
| 51–90 chars | step down one rung |
| >90 chars | rewrite shorter, or cap at `--text-4xl` with tighter leading |

A 100-character headline set at display size is a reliable tell that nobody
looked at the rendered page. When writing the headline yourself, aim for ≤7 words
and ≤50 characters from the start.

## Weight

- **Body: one weight** (400, or 350 on dark). Bold for emphasis only.
- **Headings contrast body by ≥300 units.** With body at 400 that means **700+**
  going heavier, or **100** going lighter — 200 is only a 200-unit gap and misses
  the threshold. A gap under 300 reads as a default setting rather than a decision.
  Check the face actually ships the weight: many have 700 but not 100, in which
  case heavier is the only direction available.
- **Never synthesise.** Load the weight you need. `font-weight: bold` against a
  single-weight file produces a smeared fake bold.

## Measure and leading

- Measure **45–75 characters**. `max-width: 65ch` is the working default. Under
  45ch is choppy; over 75ch loses the eye on line return.
- Line-height **1.5–1.65** for body, **1.1–1.3** for display.
- Uppercase display heads: floor `1.0`, comfortable `1.02–1.08`. See
  `responsive-correctness.md` § 8 for why.
- Body **16px** as a project default, not a conformance threshold. WCAG sets no
  absolute minimum size; what it requires is that text stays usable when scaled to
  200% (1.4.4) and reflows at 320px (1.4.10). A 14px body that zooms cleanly
  conforms; a 16px body in a fixed-height box that clips at 200% does not. Set the
  default in `rem` so user font-size preferences carry through, and verify at 200%
  rather than trusting the number.

## Tracking

- Display sizes: tighten — `letter-spacing: -0.02em` to `-0.04em`, depending on
  the face.
- Small caps and labels: loosen — `0.08em` to `0.14em` with
  `text-transform: uppercase`, or `font-variant-caps: all-small-caps` if the face
  has real small caps.
- Body: never above `0.05em`.

## Required features

The metric overrides go on a **separate fallback face**, not on the webfont. This
is the part that's easy to get backwards:

```css
/* 1 · The real face. No overrides — you want its own metrics. */
@font-face {
  font-family: "Body";
  src: url("body.woff2") format("woff2");
  font-weight: 400;              /* declare what this file actually provides */
  font-style: normal;
  font-display: swap;
}

/* 2 · One adjusted face PER fallback font. `src` is a prioritised list, so a
 *    single override set would be applied to whichever face the platform
 *    happens to have — and Arial and Helvetica Neue have different metrics.
 *    Percentages are illustrative; compute them per pair. */
@font-face {
  font-family: "Body Fallback Arial";
  src: local("Arial");
  size-adjust: 103%;
  ascent-override: 92%;
  descent-override: 8%;
  line-gap-override: 0%;
}
@font-face {
  font-family: "Body Fallback Helvetica";
  src: local("Helvetica Neue");
  size-adjust: 101%;          /* different face, different numbers */
  ascent-override: 95%;
  descent-override: 5%;
  line-gap-override: 0%;
}

/* 3 · Fallbacks sit after the real face, most-likely-available first. */
:root {
  --font-body: "Body", "Body Fallback Arial", "Body Fallback Helvetica", sans-serif;
}
```

Putting `size-adjust` on the `Body` face rescales the downloaded font itself,
which is the opposite of the intent — it distorts the real face and leaves the
fallback unadjusted, so the swap still shifts. The overrides only prevent CLS when
they're on the face being *swapped away from*.

Compute the values from the two faces' metrics (`unitsPerEm`, `ascender`,
`descender`) rather than copying the numbers above; tooling like `fontaine` or
Next.js's `next/font` does this automatically and is the better default.

- `font-display: swap` on every web font.
- **Declare `font-weight` and `font-style` on every `@font-face`.** Omitted, they
  default to `normal`/`400`, so the browser will synthesise bold and italic from
  the regular file instead of using the weights you shipped. For a variable font,
  declare the range: `font-weight: 100 900;`.
- **`font-variant-numeric: tabular-nums`** on any container showing columns of
  numbers — prices, dates, metrics, tables. Proportional figures don't align
  vertically, and misaligned numeric columns are one of the most visible signs
  nobody checked the rendered output.
- `font-variant-numeric: oldstyle-nums` for figures inside running body copy,
  where the face supports it.

## Semantics

Heading levels reflect document structure. Don't skip levels when **descending** —
`h2` → `h4` leaves a gap that makes the outline lie about nesting depth.

Returning to a higher level is not a skip and needs no filler: `h2` → `h3` → `h2`
is correct when the second section is a sibling of the first. Reading the rule as
"the sequence must never jump" produces placeholder headings that exist only to
satisfy a linter, which is worse for screen-reader navigation than the gap was.

Style them visually however you like — the constraint is the level, not the size.

## Bans

- More than three families on a page.
- The outlier face in more than two slots.
- Single-font pages — unless the single font *is* the design (a genuinely
  monospace terminal aesthetic, a one-face poster). That is a stated choice, not
  a default.
- Gradient fills on headings (`background-clip: text`).
- All-caps body copy.
- Justified text without hyphenation.
- Hard-synthesised bold or italic.
- Body copy below 14px; anything below 10px.
