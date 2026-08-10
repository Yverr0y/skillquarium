---
name: design-md-library
description: Library of 74 ready-to-use DESIGN.md files — complete design systems (color tokens, type scale, components, layout, motion, do's/don'ts) reverse-engineered from real product and brand websites like Stripe, Linear, Vercel, Notion, Apple, Tesla, WIRED, and Nintendo-2001. Use when a UI task names a reference brand or an aesthetic ("make it look like Linear", "Stripe-style landing page", "premium automotive dark theme"), when you need a concrete token set to start a design system from, or when a project asks for a DESIGN.md. Vendored from VoltAgent/awesome-design-md.
license: MIT (VoltAgent) — complete terms in LICENSE.txt
---

# DESIGN.md Library

74 complete, ready-to-use `DESIGN.md` design systems extracted from real websites.
Each one is a single self-contained markdown file: YAML token block (colors,
typography, spacing, radii, shadows) followed by prose sections an agent can follow
directly when generating UI.

Vendored from [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
@ `8147538` (2026-07-31), MIT. Local copies live in `designs/<site>/DESIGN.md`.

## What `DESIGN.md` is

A convention from [Google Stitch](https://stitch.withgoogle.com/docs/design-md/overview/):
plain-markdown design system doc that lives at a project root, the visual counterpart
to `AGENTS.md`.

| File | Defines |
|---|---|
| `AGENTS.md` | how to build the project |
| `DESIGN.md` | how the project should look and feel |

## When to use this skill

Use it when the desired look can be named — a brand ("like Vercel"), a category
("crypto trading dashboard", "luxury automotive", "Y2K retro"), or an adjective set
that maps onto one of the catalog entries. A vendored file gives you a coherent,
already-calibrated token set instead of a palette invented on the spot.

Do **not** use it for:

- **Writing a fresh `DESIGN.md` for a project with its own identity** → `stitch-design-taste`
  (generator; this skill is the reference library).
- **General "make this look good" with no reference point** → `design-taste-frontend`,
  `high-end-visual-design`, or `web-design-guidelines`.
- **Applying a neutral theme to slides/docs/reports** → `theme-factory`.
- **Auditing and redesigning an existing UI** → `redesign-existing-projects`.

These compose: pick a file here for the token vocabulary, then follow
`frontend-ui-engineering` / `ui-css-primitives` for the implementation.

## How to use

1. **Pick one entry from the catalog below.** Match on the aesthetic description, not
   on brand affinity.
2. **Read exactly that one file.** They run 125–850 lines (~5–25k tokens each). Never
   read several to compare — pick from the catalog blurbs, and read a second only if
   the first is clearly wrong.
3. **Install or extract:**
   - Whole-project styling: `cp designs/<site>/DESIGN.md ./DESIGN.md`, then tell the
     agent (or Stitch) to build against it. It stays in the repo as the source of truth.
   - One component or page: pull just the token block and the relevant `## Components`
     entry into context; don't paste the whole file into code comments.
4. **Reconcile with what exists.** If the project already has tokens (Tailwind config,
   CSS variables, a design system), map the file's roles onto the existing names rather
   than introducing a parallel palette.

### Anatomy of each file

```
---
version / name / description        # one-paragraph statement of the design language
colors:      semantic-name: "#hex"  # primary, ink, canvas, hairline, accents…
typography:  role: {fontFamily, fontSize, fontWeight, lineHeight, letterSpacing}
spacing / radii / shadows / motion
---
## Overview              mood, density, philosophy
## Colors                each hex + its functional role
## Typography            full hierarchy table
## Layout                grid, spacing scale, whitespace philosophy
## Elevation & Depth     shadow system, surface hierarchy
## Shapes                radii, borders, geometry
## Components            buttons, cards, inputs, nav — with states
## Do's and Don'ts       guardrails and anti-patterns
## Responsive Behavior   breakpoints, touch targets, collapse strategy
## Iteration Guide       quick color reference, ready-to-use prompts
```

The `## Do's and Don'ts` section is the highest-value part and the one most often
skipped — it is what keeps generated UI from drifting into generic-AI look.

### Blending two systems

Legitimate, but keep it disciplined: take the **color system from one** file and the
**typography + spacing from the other**, never half of each. Mixing accent colors
across two systems is what produces incoherent output.

## Guardrails

- **These are interpretations, not official brand kits.** Upstream deliberately
  renames brands in the frontmatter (`Stripi`, `Slacc`) and states it captures
  publicly visible CSS values without claiming ownership of any visual identity.
- **Don't ship a clone.** Using Stripe's spacing rhythm and weight-300 display type is
  style; reproducing its logo, wordmark, illustrations, or enough of the identity that
  users would think they're on Stripe is a trademark problem. Adapt the system, keep
  your own identity.
- **Proprietary fonts need licenses.** Many files name commercial or in-house faces
  (Söhne, Geist, SoDoSans, LamboType, Manuka, NouvelR). Each `fontFamily` ships a
  fallback stack — use the fallback, or substitute a licensed near-match, unless the
  project actually owns the font.
- **Hexes are point-in-time.** Extracted from live sites; upstream is community-
  maintained and values can be stale or slightly off. Verify contrast ratios yourself
  rather than trusting a pair to be accessible.

## Catalog

Path is `designs/<slug>/DESIGN.md`.

#### AI & LLM platforms
- **Claude** — `claude` — Warm terracotta accent, clean editorial layout
- **Cohere** — `cohere` — Vibrant gradients, data-rich dashboard aesthetic
- **ElevenLabs** — `elevenlabs` — Dark cinematic UI, audio-waveform aesthetics
- **Minimax** — `minimax` — Bold dark interface with neon accents
- **Mistral AI** — `mistral.ai` — French-engineered minimalism, purple-toned
- **Ollama** — `ollama` — Terminal-first, monochrome simplicity
- **OpenCode AI** — `opencode.ai` — Developer-centric dark theme
- **Replicate** — `replicate` — Clean white canvas, code-forward
- **Runway** — `runwayml` — Editorial film-festival: cinematic dark heroes, paper-white reading bands, pure black pill CTAs
- **Together AI** — `together.ai` — Technical, blueprint-style design
- **VoltAgent** — `voltagent` — Void-black canvas, emerald accent, terminal-native
- **xAI** — `x.ai` — Stark monochrome, futuristic minimalism

#### Developer tools & IDEs
- **Cursor** — `cursor` — Sleek dark interface, gradient accents
- **Expo** — `expo` — Dark theme, tight letter-spacing, code-centric
- **Lovable** — `lovable` — Playful gradients, friendly dev aesthetic
- **Raycast** — `raycast` — Sleek dark chrome, vibrant gradient accents
- **Superhuman** — `superhuman` — Premium dark UI, keyboard-first, purple glow
- **Vercel** — `vercel` — Black and white precision, Geist font
- **Warp** — `warp` — Dark IDE-like interface, block-based command UI

#### Backend, database & DevOps
- **ClickHouse** — `clickhouse` — Yellow-accented, technical documentation style
- **Composio** — `composio` — Modern dark with colorful integration icons
- **HashiCorp** — `hashicorp` — Enterprise-clean, black and white
- **MongoDB** — `mongodb` — Green leaf branding, developer documentation focus
- **PostHog** — `posthog` — Playful branding, developer-friendly dark UI
- **Sanity** — `sanity` — Dark-first editorial: 112px display type, IBM Plex Mono eyebrows, single coral-red CTA accent
- **Sentry** — `sentry` — Dark dashboard, data-dense, pink-purple accent
- **Supabase** — `supabase` — Dark emerald theme, code-first

#### Productivity & SaaS
- **Cal.com** — `cal` — Clean neutral UI, developer-oriented simplicity
- **Intercom** — `intercom` — Friendly blue palette, conversational UI patterns
- **Linear** — `linear.app` — Ultra-minimal, precise, purple accent
- **Mintlify** — `mintlify` — Clean, green-accented, reading-optimized
- **Notion** — `notion` — Warm minimalism, serif headings, soft surfaces
- **Resend** — `resend` — Minimal dark theme, monospace accents
- **Slack** — `slack` — Deep aubergine primary, cream-lavender hero gradients, pastel-mesh product mockups
- **Zapier** — `zapier` — Warm orange, friendly illustration-driven

#### Design & creative tools
- **Airtable** — `airtable` — Colorful, friendly, structured data aesthetic
- **Clay** — `clay` — Organic shapes, soft gradients, art-directed layout
- **Figma** — `figma` — Vibrant multi-color, playful yet professional
- **Framer** — `framer` — Bold black and blue, motion-first, design-forward
- **Miro** — `miro` — Bright yellow accent, infinite canvas aesthetic
- **Webflow** — `webflow` — Blue-accented, polished marketing site aesthetic

#### Fintech & crypto
- **Binance** — `binance` — Bold yellow on monochrome, trading-floor urgency
- **Coinbase** — `coinbase` — Clean blue identity, trust-focused, institutional
- **Kraken** — `kraken` — Purple-accented dark UI, data-dense dashboards
- **Mastercard** — `mastercard` — Warm cream canvas, orbital pill shapes, editorial warmth
- **Revolut** — `revolut` — Sleek dark interface, gradient cards, fintech precision
- **Stripe** — `stripe` — Indigo primary, atmospheric gradient mesh, weight-300 elegance
- **Wise** — `wise` — Bright green accent, friendly and clear

#### E-commerce & retail
- **Airbnb** — `airbnb` — Warm coral accent, photography-driven, rounded UI
- **Meta** — `meta` — Photography-first, binary light/dark surfaces, blue CTAs
- **Nike** — `nike` — Monochrome UI, massive uppercase Futura, full-bleed photography
- **Shopify** — `shopify` — Dark-first cinematic, neon green accent, ultra-light display type
- **Starbucks** — `starbucks` — Four-tier earth-green system, warm cream canvas

#### Media & consumer tech
- **Apple** — `apple` — Premium white space, SF Pro, cinematic imagery
- **HP** — `hp` — Pure white canvas, electric-blue signal CTA, geometric sans, chevron decorations
- **IBM** — `ibm` — Carbon design system, structured blue palette
- **NVIDIA** — `nvidia` — Green-black energy, technical power aesthetic
- **Pinterest** — `pinterest` — Red accent, masonry grid, image-first
- **PlayStation** — `playstation` — Three-surface channel layout, cyan hover-scale interaction
- **SpaceX** — `spacex` — Stark black and white, full-bleed imagery, futuristic
- **Spotify** — `spotify` — Vibrant green on dark, bold type, album-art-driven
- **The Verge** — `theverge` — Acid-mint and ultraviolet accents, Manuka display type
- **Uber** — `uber` — Bold black and white, tight type, urban energy
- **Vodafone** — `vodafone` — Monumental uppercase display, red chapter bands
- **WIRED** — `wired` — Paper-white broadsheet density, custom serif, ink-blue links

#### Automotive
- **BMW** — `bmw` — Dark premium surfaces, precise German engineering aesthetic
- **BMW M** — `bmw-m` — Motorsport contrast, M color accents, precision-driven layout
- **Bugatti** — `bugatti` — Cinema-black canvas, monochrome austerity, monumental display type
- **Ferrari** — `ferrari` — Chiaroscuro black-white editorial, red accent, extreme sparseness
- **Lamborghini** — `lamborghini` — True black cathedral, gold accent, custom Neo-Grotesk
- **Renault** — `renault` — Vivid aurora gradients, proprietary typeface, zero-radius buttons
- **Tesla** — `tesla` — Radical subtraction, cinematic full-viewport photography

#### Retro web
- **Dell (1996)** — `dell-1996` — Catalog-era enterprise web: black page frame, flat color-block ribbon cards, Helvetica-Black over Times Roman, hand-cut GIF stickers
- **Nintendo.com (2001)** — `nintendo-2001` — Y2K console chrome: brushed-periwinkle beveled panels, halftone carbon nav, outlined Arial-Black wordmarks

## Updating the library

```bash
cd $(mktemp -d) && git clone --depth 1 https://github.com/VoltAgent/awesome-design-md.git
cd awesome-design-md && git log -1 --format=%h   # note the SHA for SKILL.md
for d in design-md/*/; do
  s=$(basename "$d")
  mkdir -p ~/.agents/skills/design-md-library/designs/"$s"
  cp "$d/DESIGN.md" ~/.agents/skills/design-md-library/designs/"$s"/DESIGN.md
done
```

Then refresh the catalog above from upstream's `README.md` (its Collection section
occasionally lags the folder list — `slack` was present as a folder but missing from
the README at `8147538`) and update the vendored commit SHA.
