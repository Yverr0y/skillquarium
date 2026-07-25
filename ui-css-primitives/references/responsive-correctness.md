# Responsive correctness

These are bugs, not preferences — and no framework fixes them for you. Tailwind,
Radix, and every component library will happily ship all of them.

Verify at **320 · 375 · 414 · 768 px** CSS widths. 320px is the practical floor
(iPhone SE class); 414px catches the large-phone case people skip; 768px catches
the tablet-portrait breakpoint where two-column layouts usually break first.

## 1 · `overflow-x: clip`, never `hidden`

Any page with a deliberately overflowing element — a full-bleed marquee, an
oversized headline, a figure that extends past its column — needs a global clip
so the document doesn't scroll horizontally.

```css
html { overflow-x: clip; }
body { overflow-x: clip; }   /* both: older Safari honours it on body */
```

**Use `clip`, not `hidden`.** `overflow: hidden` creates a scroll container, which
breaks `position: sticky` and `position: fixed` on descendants and can trap focus
on overflowing inputs. `clip` clips without creating one.

The containing section keeps `overflow: visible` so the element still renders past
its parent edge — the global clip is the only safety net needed.

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

## 4 · Clickable text never wraps to two lines

A button label, nav link, footer link, breadcrumb, or CTA reading on two lines
looks broken — readers can't tell whether the break is intentional, and the row's
vertical rhythm breaks because that one control grew taller than its siblings.
The worst case is a single orphaned word on line two.

Fixes, in order of preference:

1. **Shorten the label.** Most CTA copy is too long. *"Get started free"* →
   *"Start free"*. *"Read the documentation"* → *"Read docs"*.
2. `white-space: nowrap` on the affordance, and let the parent flex container
   reflow around it.
3. Drop a non-essential nav item at narrow widths.
4. Collapse the nav into a sheet or menu below a threshold.

Never let a primary CTA or a nav link wrap.

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
