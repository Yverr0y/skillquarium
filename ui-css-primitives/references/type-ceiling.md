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
- **Headings contrast body by ≥300 units.** If body is 400, headings are 700 or
  200 — not 500 or 600. A 200-unit gap reads as a default setting rather than a
  decision.
- **Never synthesise.** Load the weight you need. `font-weight: bold` against a
  single-weight file produces a smeared fake bold.

## Measure and leading

- Measure **45–75 characters**. `max-width: 65ch` is the working default. Under
  45ch is choppy; over 75ch loses the eye on line return.
- Line-height **1.5–1.65** for body, **1.1–1.3** for display.
- Uppercase display heads: floor `1.0`, comfortable `1.02–1.08`. See
  `responsive-correctness.md` § 8 for why.
- Body minimum **16px**. Below 14px is accessibility-hostile; nothing below 10px
  anywhere.

## Tracking

- Display sizes: tighten — `letter-spacing: -0.02em` to `-0.04em`, depending on
  the face.
- Small caps and labels: loosen — `0.08em` to `0.14em` with
  `text-transform: uppercase`, or `font-variant-caps: all-small-caps` if the face
  has real small caps.
- Body: never above `0.05em`.

## Required features

```css
@font-face {
  font-family: "Body";
  src: url("body.woff2") format("woff2");
  font-display: swap;
  /* Match fallback metrics to prevent CLS on swap */
  size-adjust: 103%;
  ascent-override: 92%;
  descent-override: 8%;
  line-gap-override: 0%;
}
```

- `font-display: swap` on every web font.
- Metric overrides on the fallback so the swap doesn't shift layout. The four
  properties above are what turn a visible reflow into an invisible one.
- **`font-variant-numeric: tabular-nums`** on any container showing columns of
  numbers — prices, dates, metrics, tables. Proportional figures don't align
  vertically, and misaligned numeric columns are one of the most visible signs
  nobody checked the rendered output.
- `font-variant-numeric: oldstyle-nums` for figures inside running body copy,
  where the face supports it.

## Semantics

Skip no heading levels: `h1` → `h2` → `h3`. Style them visually however you
like, but keep the document order intact — screen-reader navigation depends on
it, and so does every outline tool.

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
