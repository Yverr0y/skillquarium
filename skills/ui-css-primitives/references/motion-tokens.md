# Motion tokens

The problem this solves: raw `cubic-bezier(...)` values scattered through a
stylesheet drift. Three named easings and three named durations, referenced
everywhere, make motion a system instead of a series of guesses.

## The token block

```css
:root {
  /* Durations — three buckets, not a continuum */
  --dur-micro: 120ms;   /* button press, toggle tick, colour shift */
  --dur-short: 220ms;   /* hover lift, tooltip, menu open */
  --dur-long:  420ms;   /* modal, drawer, accordion, page reveal */

  /* Easings — exponential; elements settle in, accelerate out */
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);      /* entering */
  --ease-in:     cubic-bezier(0.7, 0, 0.84, 0);      /* leaving */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);     /* state toggles */
}
```

Avoid `ease`, `ease-in-out` (the keyword), and `cubic-bezier(0.25, 0.1, 0.25, 1)`.
They are the browser defaults and read as uncrafted — too linear in the middle,
too abrupt at the ends.

**Exits run ≈75% of the enter duration.** Things should leave faster than they
arrive; a slow exit feels like the UI is reluctant.

```css
.menu.is-open  { transition: transform var(--dur-short) var(--ease-out); }
.menu.is-close { transition: transform calc(var(--dur-short) * 0.75) var(--ease-in); }
```

## Animate compositor-friendly properties; never layout properties

Three tiers, and the distinction matters because the middle one is fine:

| Tier | Properties | Cost per frame |
|---|---|---|
| **Compositor** | `transform`, `opacity`, `filter` | No layout, no paint — cheapest |
| **Paint** | `background-color`, `color`, `border-color`, `box-shadow` | Repaint, no layout — acceptable |
| **Layout** | `width`, `height`, `top`, `left`, `margin`, `padding`, `font-size` | Reflow every frame — never animate |

Prefer the compositor tier for anything spatial. The paint tier is *correct* for
state changes — a button's hover colour should transition `background-color`, and
doing that is not a performance defect. Keep paint-tier transitions short and on
small elements; a `box-shadow` transition across a large surface is the one to
watch.

Never animate the layout tier. If you reach for it, you want a `transform`:

```css
/* wrong — reflow every frame */
.card:hover { margin-top: -4px; }

/* right */
.card:hover { transform: translateY(-4px); }
```

Corollary: never write `transition: all`. It animates properties that should be
instant — `visibility`, outline, focus indicators — and makes every future
addition to the rule silently animated. Name the properties.

```css
transition:
  background-color var(--dur-short) var(--ease-out),
  transform        var(--dur-micro) var(--ease-out);
```

## Page-load orchestration

One sequence, staggered by DOM index via a custom property. No JavaScript
needed.

```html
<section style="--i: 0">…</section>
<section style="--i: 1">…</section>
<section style="--i: 2">…</section>
```

```css
.reveal {
  opacity: 0;
  transform: translateY(8px);
  animation: reveal var(--dur-long) var(--ease-out) forwards;
  /* clamped: a long page can't push the last item past the budget */
  animation-delay: min(calc(var(--i, 0) * 60ms), 500ms);
}
@keyframes reveal { to { opacity: 1; transform: none; } }
```

The `min()` is load-bearing. A bare `calc(var(--i) * 60ms)` grows without bound,
so a page with 20 sections staggers to 1.2s — past the point where the page feels
like it settles. Clamp it rather than trusting section counts to stay small.

## Scroll-linked motion

- Use `IntersectionObserver`, never a `scroll` event listener.
- Reveal-once only. Not every section — one orchestrated entrance beats ten
  small ones, and a page where everything fades in never settles.
- Every scroll-triggered animation needs a reduced-motion path.

## Reduced motion is not optional

Spatial motion collapses to an opacity crossfade of ≤150ms. Functional motion —
progress bars, loading spinners, skeletons — **keeps running**; it carries
information, and killing it leaves the user staring at a frozen spinner with no
indication anything is happening.

That second requirement is why the blunt global override is wrong. A universal
`animation-iteration-count: 1 !important` stops every looping animation after one
pass, including the spinners the previous paragraph promises to preserve. Opt
functional motion out explicitly:

```css
@media (prefers-reduced-motion: reduce) {
  /* Decorative motion: collapse. :not() spares anything marked functional. */
  *:not([data-motion="functional"]),
  *:not([data-motion="functional"])::before,
  *:not([data-motion="functional"])::after {
    animation-duration: 150ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 150ms !important;
  }

  .reveal { animation: reveal-reduced 150ms linear forwards; }
  @keyframes reveal-reduced { to { opacity: 1; transform: none; } }

  /* Functional loaders keep looping — slower, and without spatial travel. */
  [data-motion="functional"] { animation-duration: 1.2s; }
}
```

Then mark the loaders: `<div class="spinner" data-motion="functional">`. If you'd
rather not carry an attribute, scope the override to a decorative class instead —
the requirement is that *something* distinguishes the two, not this exact
mechanism. A reduced-motion spinner should also prefer an opacity pulse over a
rotation.

## Focus rings appear instantly

Never transition a focus indicator into existence. A ring that fades in over
200ms means a keyboard user has no indicator for 200ms — exactly when they need
it.

```css
/* wrong */
.btn { transition: outline-color var(--dur-short); }

/* right — reserve the ring, swap the colour with no transition */
.btn { outline: 2px solid transparent; outline-offset: 2px; }
.btn:focus-visible { outline-color: var(--color-focus); }
```

Reserving `outline: 2px solid transparent` at rest also prevents the geometry
shift some layouts get when the outline appears.

## Component recipes

**Button** — `--dur-micro`, `--ease-out`, `translateY(-1px)` on hover,
`translateY(0)` on `:active`. On a dark surface, never transition `box-shadow` on
hover; it produces a glow.

**Menu / tooltip / dropdown** — `--dur-short`, `--ease-out` opening,
`--ease-in` closing.

> Focus is a separate concern from the transition, and `inert` does not cover it.
> `inert` only removes a subtree from focus order and hit-testing — it cannot move
> focus into the widget, implement arrow-key navigation, or restore focus to the
> trigger on close. Applied to the widget it disables the widget; applied to the
> background it is one part of modal focus handling, not the whole of it. Use an
> accessible primitive (Radix, Base UI, React Aria) or the native `<dialog>` /
> Popover API and implement the focus lifecycle deliberately.

**Modal** — `--dur-long`, scale `0.96 → 1` plus an opacity crossfade. Backdrop
fades at the same duration.

**Accordion** — animate `grid-template-rows: 0fr → 1fr` with `--ease-in-out`,
not `height`.

> Support note: interpolating to and from `0fr` works in Chromium 117+, Safari
> 17.2+, and Firefox 129+. If you need older support, either animate a
> `max-height` to a known value or accept an instant toggle — don't animate
> `height: auto`, which does not interpolate. `calc-size()` will eventually make
> this cleaner but is not broadly available yet.

**Tooltips** — hover delay 800–1000ms; focus delay **0ms**. Different intents
deserve different timing: a hover may be accidental, a focus never is.

## Bans

- `ease` — the browser default.
- `linear` on anything except progress bars and ticking loaders.
- Bounce / elastic / overshoot easings on UI state (buttons, modals, tooltips).
  Reserve overshoot for genuine physical interaction, like a drag release.
- More than one hover effect on the same element. Pick translate *or* scale *or*
  shadow *or* colour — not four.
- A uniform `hover:scale-105` applied across unrelated elements.
- Animating any layout property.
- `will-change` set preemptively across a class. Only on the element, only while
  it animates.
- Parallax. Custom cursor followers.
- Infinite loops other than functional loaders — they pull the eye and never
  release it.
- Auto-rotating carousels without pause-on-hover-and-focus (WCAG 2.2.2).
- Celebratory toasts for an action whose effect is already visible. Silent
  success; toasts for failures and invisible async effects.
- Spinners that flash for 50ms. Either delay-show by ~150ms or enforce a ~300ms
  minimum once shown. Prefer skeletons when the layout is known.

## The governing question

If you cannot say what a transition communicates, cut it. Most pages have too
much motion, not too little — subtract before you add.
