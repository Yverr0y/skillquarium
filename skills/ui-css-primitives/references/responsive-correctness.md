# Responsive correctness

These are bugs, not preferences — and no framework fixes them for you. Tailwind,
Radix, and every component library will happily ship all of them.

Verify at **320 · 375 · 414 · 768 px** CSS widths. 320px is the practical floor
(iPhone SE class); 414px catches the large-phone case people skip; 768px catches
the tablet-portrait breakpoint where two-column layouts usually break first.

## 1 · Clip the container that overflows, not the document

When one element deliberately overflows — a full-bleed marquee, an oversized
headline, a figure extending past its column — clip **that element's container**:

```css
.marquee-wrap { overflow-x: clip; }
```

**Use `clip`, not `hidden`.** `overflow: hidden` makes the box a scroll container.
That breaks `position: sticky` on descendants, because they now stick to that
container rather than the viewport. `clip` clips without creating a scroll
container, so sticky keeps working.

`overflow` alone does **not** create a containing block for `position: fixed` —
that takes `transform`, `filter`, `perspective`, `backdrop-filter`, `contain`, or
`will-change` on an ancestor. Sticky is the one this affects.

### Why not just clip `html` and `body`

A global `overflow-x: clip` on the root is tempting as a blanket safety net, and
it is the wrong default for two reasons:

1. **It can strand focusable content.** Once the root clips, overflowing content
   is no longer reachable by user scrolling — there is no scrollbar to drag. If a
   real control or link overflows because of an actual layout defect, keyboard
   focus still moves to it while it sits visually outside the clip, which is a
   WCAG 2.4.7 / 1.4.10 problem and worse than the scrollbar it replaced. (What
   the browser does on focus differs between `clip` and `hidden` — `hidden` still
   permits programmatic scrolling, so focus may yank the layout sideways instead.
   Neither outcome is one you want.)
2. **It suppresses your own detection.** The pre-ship sweep at the bottom of this
   file works by watching for a horizontal scrollbar. Clipping the root removes
   the symptom and leaves the defect.

So: scope the clip to the decorative container that is *supposed* to overflow, and
fix anything else that does. Reach for the root-level clip only as a deliberate,
commented last resort, after confirming nothing focusable sits in the clipped
region:

```css
/* Last resort. Verified: only .hero__marquee extends past the viewport,
 * and it contains no focusable content. */
html, body { overflow-x: clip; }
```

The containing section keeps `overflow: visible` so the element still renders past
its parent edge.

Related: never `width: 100vw`. It includes the scrollbar width on desktop
browsers that reserve space, producing a few pixels of horizontal scroll. Use
`width: 100%` with container padding, or `100dvw` if you genuinely need viewport
units.

## 2 · `minmax(0, 1fr)` on tracks holding images

This is the single most common cause of "my grid blows out on mobile."

`1fr` is shorthand for `minmax(auto, 1fr)`, and the `auto` minimum resolves to the
item's min-content contribution. For a replaced element like an `<img>`, that is
its intrinsic width — so a 1600px-wide source forces a 1600px minimum track,
pushing the layout past the viewport.

```css
/* wrong */
grid-template-columns: 1fr 1fr;

/* right */
grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
```

One character per track. Applies to `grid-template-rows` equally. The same
underlying issue bites flex items — `min-width: 0` is the flex equivalent.

Belt and braces on the image itself:

```css
img { max-width: 100%; height: auto; display: block; }
```

## 3 · Long words in display type

Display-size headings overflow when the only break opportunity is a hyphen —
"AI-generated", long compound brand names, URLs.

```css
h1, .display {
  overflow-wrap: anywhere;
  min-width: 0;
}
```

`overflow-wrap: anywhere` lets the engine break inside a word as a last resort
and, unlike `break-word`, is accounted for when computing intrinsic min-content
size — which is what actually prevents the overflow. Pair with `hyphens: auto`
and a `lang` attribute if hyphenation is wanted.

## 4 · Clickable text that wraps unintentionally

A button label or primary nav link breaking onto two lines usually looks broken —
readers can't tell whether the break was intended, and the row's rhythm goes with
it because one control grew taller than its siblings. Worst case is a single
orphaned word on line two.

**The requirement is that no label overflows, clips, or becomes unreadable.** It is
*not* that no label ever wraps. That distinction matters because:

- German and Finnish routinely run 40–60% longer than English. "Get started free"
  → "Kostenlos loslegen" → and a translator can't always shorten it.
- WCAG 1.4.4 requires text to stay usable at 200% zoom, and 1.4.10 requires reflow
  at 320px. `white-space: nowrap` on a long label defeats both — the label
  overflows its container or gets clipped instead of wrapping.

Fixes, in order of preference:

1. **Shorten the label.** Most CTA copy is too long. *"Get started free"* →
   *"Start free"*. Available for copy you control; often unavailable for
   translated strings.
2. **Let the container reflow** — wrap the row, stack the nav, drop a
   non-essential item at narrow widths, or collapse into a sheet or menu.
3. **`white-space: nowrap` only where the design contract genuinely requires one
   line** — a fixed-width toolbar button, a table header, a chip. Pair it with a
   guard so an over-long string degrades visibly rather than escaping its box:

   ```css
   .chip {
     white-space: nowrap;
     max-width: 100%;
     overflow: hidden;
     text-overflow: ellipsis;   /* truncates instead of overflowing */
   }
   ```

   Truncation loses information, so it needs a `title` or accessible name carrying
   the full text.
4. **Allow the wrap** when the container can't reflow and the label can't shrink.
   Two clean lines with a preserved tap target beat a clipped single line. Keep it
   deliberate: `text-wrap: balance` splits the lines evenly, and `min-height`
   keeps the row aligned with its siblings.

The failure to hunt for is a label wrapping *by accident* at one breakpoint nobody
checked — not wrapping as such.

## 5 · Two sticky elements both at `top: 0`

If a sticky page nav and a sticky in-page element (a section head, a table of
contents, a sticky feature pane) are both at `top: 0`, both dock to the viewport
top and overlap. The one deeper in the DOM paints over the nav.

```css
:root {
  --banner-h: 3.5rem;
  --z-sticky:     200;   /* in-page sticky elements */
  --z-sticky-nav: 300;   /* the top nav always wins */
}
.site-nav     { position: sticky; top: 0;              z-index: var(--z-sticky-nav); }
.section-head { position: sticky; top: var(--banner-h); z-index: var(--z-sticky); }
```

Also give anchored scrolling room to breathe:

```css
:target, [id] { scroll-margin-top: calc(var(--banner-h) + var(--space-md)); }
```

## 6 · Viewport units on mobile

`100vh` does not match the visible viewport on mobile browsers with dynamic
toolbars — content ends up under the URL bar.

Use `100dvh` (dynamic) for full-height layouts, or `100svh` (small) when you want
the guaranteed-visible height and no reflow as the toolbar hides. `lvh` is the
large variant. Per `baseline-ui`: prefer `h-dvh` over `h-screen` in Tailwind.

Respect device insets on anything fixed:

```css
.bottom-bar {
  padding-bottom: max(var(--space-md), env(safe-area-inset-bottom));
}
```

## 7 · Per-theme grid overrides that forget mobile

If a theme or variant overrides a shared grid template, it also needs the mobile
collapse — otherwise the override wins at every width and the layout keeps its
desktop template on a phone.

```css
/* the override */
[data-theme="wide"] .section__head { grid-template-columns: 0.4fr 1fr; }

/* the collapse it needs — matching specificity */
@media (max-width: 48rem) {
  [data-theme] .section__head { grid-template-columns: minmax(0, 1fr); }
}
```

Specificity has to match or exceed the override, or the media query silently
loses.

## 8 · Uppercase display heads need `line-height` ≥ 1.0

Uppercase glyphs have no descenders, so their cap-tops sit at the very top of the
line box. At `line-height: 0.94` the cap-tops of line 2 collide with the baseline
— or a trailing comma — of line 1 when the heading wraps. Condensed faces make it
worse.

Floor is `1.0`; `1.02–1.08` is comfortable. Either raise the line-height or drop
the `text-transform: uppercase`.

## 9 · CSS-only radio tabs that scroll-jump

Tab toggles built from `<input type="radio">` siblings plus `:checked` selectors
will jump the page to the section top on every tab click if the radios sit at
`position: absolute; top: 0`.

Either keep the radios in normal flow with zero size and `opacity: 0`, or
intercept the label click in JS and focus with `{ preventScroll: true }`.

**A visually hidden radio still takes focus**, so the focus indicator has to be
forwarded to something visible or keyboard users navigate blind:

```css
.tab-radio {                    /* in flow, zero size — no scroll jump */
  position: static;
  width: 0; height: 0;
  opacity: 0;
  margin: 0;
}
/* forward both states to the visible label */
.tab-radio:focus-visible + .tab-label { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.tab-radio:checked       + .tab-label { border-block-end: 2px solid var(--color-accent); }
```

Never `display: none` or `visibility: hidden` on the input — both remove it from
the tab order and the pattern stops being keyboard-operable at all.

Worth saying plainly: this pattern is fiddly enough that a real tablist —
`role="tablist"` with arrow-key handling, or a library primitive — is usually the
better answer. CSS-only tabs are a reasonable choice for a static page with no JS,
not for an application.

## Pre-ship sweep

Drag the devtools width from 320 to 1920 and watch for a horizontal scrollbar
appearing at any width. Then at each of 320/375/414/768:

- [ ] No horizontal scroll
- [ ] No clickable text on two lines
- [ ] No image forcing a track wider than the viewport
- [ ] No heading overflowing its container
- [ ] Sticky elements stack rather than overlap
- [ ] Fixed bottom elements clear the safe-area inset
- [ ] Multi-column heads have collapsed to one column
