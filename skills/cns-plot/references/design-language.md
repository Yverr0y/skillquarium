# CNSPlots design language

Use this reference to reproduce the visual system faithfully while adapting it to
the data and target venue.

## Contents

1. [Text](#text)
2. [Color](#color)
3. [Graphical objects](#graphical-objects)
4. [Layout](#layout)
5. [Export](#export)

## Text

### Build a compact hierarchy

Use a small number of roles:

| Role | Source-derived default | Treatment |
|---|---:|---|
| Axes title and axis labels | 8 pt | Bold title; plain labels |
| Tick labels, legends, colorbar ticks | 7 pt | Regular |
| Panel labels | 8 pt | Bold, outside upper-left |
| Statistical annotations | Small/7 pt | Consistent format and location |

Do not shrink text to rescue an overloaded panel. Remove redundant labels, widen the
panel, reduce the number of categories, or split the view.

### Use a robust font stack

Prefer Helvetica, Helvetica Neue, Arial, then DejaVu Sans. Apply a Unicode-capable
fallback such as DejaVu Sans only to text containing unsupported glyphs. This keeps
the main visual system stable without losing Greek letters, arrows, or mathematical
symbols.

Use an en dash or a typographic minus consistently in scientific labels. Confirm the
chosen export path preserves the actual Unicode character.

### Place text in the right coordinate system

- Use data coordinates for labels attached to observations.
- Use axes coordinates for panel-internal labels and explanations.
- Use point or pixel offsets for fixed visual clearance.
- Anchor panel labels to the axes upper-left corner and offset outward. Do not place
  them at guessed data coordinates.
- Measure rendered extents when labels, titles, or legends affect layout.

For dense labels, select a scientifically meaningful subset first, then use
`adjustText` or an equivalent collision solver. Add a thin white stroke behind text
when it crosses marks, and keep leader lines narrow.

### Keep statistical text auditable

State the comparison and test in the caption or method. Keep a single annotation
format across the figure: stars, thresholds, or full values. Do not mix formats
without a reason. Do not let a plotting helper choose a test that conflicts with the
analysis plan.

## Color

### Separate cycles from maps

A qualitative **cycle** assigns distinct colors to identities. A continuous **map**
assigns lightness/hue to magnitude. Do not use a rainbow-like categorical cycle as a
continuous scale or a sequential map for unordered groups.

Use these source-derived families deliberately:

| Need | Suitable families |
|---|---|
| Accessible categorical baseline | `OkabeIto`, `TolBright`, `TolMuted` |
| Conventional categorical | `Set1`, `Set2`, `Set3`, `Tableau`, `Bold` |
| Large biological taxonomies | `Ecotyper1` through `Ecotyper6` |
| Journal-inspired look | `Cell`, `Nature`, `Science`, `Lancet`, `NEJM`, `JAMA`, `JCO` |
| Sequential magnitude | `parula`, `gnuplot`, `WhYlOrRd_custom`, `YlGnBu_custom` |
| Signed/centered value | `BuRd_custom`, `OrBu_custom`; use `BlueRed` only as a discrete cycle |

Journal-inspired palette names are visual presets, not proof of compliance with a
journal's current rules. Test all mappings for color-vision accessibility and
grayscale separation.

### Assign colors by meaning

Create an explicit dictionary such as:

```python
class_colors = {
    "Control": "#A3A3A3",
    "Responder": "#5189BB",
    "Non-responder": "#D6372E",
}
```

Reuse the dictionary across panels. Do not rely on row order or an implicit plotting
cycle when the same identity appears more than once.

The source's named accents are:

```text
RED #D6372E   BLUE #5189BB   GREEN #70B460   PURPLE #985EA8
ORANGE #F08F35   YELLOW #FADD4B   BROWN #9C5732   PINK #E787E5
GRAY #A3A3A3   VIOLET #442288   CHOCOLATE #662506
```

Use them as a starting vocabulary, not an obligation.

### Preserve contrast

Choose black or white annotation text from background luminance. The source uses
relative luminance weights `0.2126 R + 0.7152 G + 0.0722 B` and switches near `0.5`.
Also verify small text and thin strokes visually; a luminance threshold alone does
not guarantee accessibility.

Use transparency for uncertainty or overlapping density, not as a substitute for
good color selection.

## Graphical objects

### Keep geometry honest

- Begin axes at zero for bars when length encodes magnitude.
- Show the scientifically meaningful null on forest, fold-change, or effect plots.
- Preserve proportions in stacked bars and make normalization explicit.
- Match error bars to the stated uncertainty: SD, SE, CI, or model interval.
- Avoid smoothing that implies unsupported temporal or causal structure.

### Layer simple artists

Follow a restrained hierarchy:

1. Background bands or flows: low `zorder`, no border, moderate alpha.
2. Supporting stems, intervals, and reference lines: thin strokes.
3. Primary points, bars, or curves: opaque and visually dominant.
4. Labels and annotations: highest `zorder`, readable contrast.

Examples distilled from the source:

- **Lollipop:** translucent `vlines`/`hlines` plus an opaque scatter marker; add
  error bars with black 0.7-pt lines and 2-pt caps.
- **Forest:** square markers with horizontal confidence intervals; offset hue groups
  slightly; draw a dashed null line.
- **Volcano:** rasterize the dense scatter, enlarge only selected genes, use neutral
  colors for nonsignificant points, and keep labels vector.
- **Sankey:** use opaque terminal bars, semi-transparent `fill_between` ribbons, and
  direct labels outside both sides.
- **Heatmap:** rasterize cells, retain vector annotations and labels, and use a full
  thin frame when it clarifies the matrix boundary.

Use line width, marker size, fill, and alpha consistently across panels. Do not add
outlines to every point in a dense scatter; they create visual noise and large vector
files.

### Manage legends as objects

Keep legends frameless and compact. Resize legend markers independently when plot
markers are intentionally tiny. Move a legend outside the axes when it would cover
data, then include it in the export bounding box.

Direct-label a small number of series when that removes eye travel. Use a legend when
direct labels would overlap or when identities recur across panels.

## Layout

### Size the final artifact first

cnsplots uses `inches = pixels / 72`. Useful approximate widths are:

| Physical width | Layout width |
|---:|---:|
| 89 mm | 252 px |
| 120 mm | 340 px |
| 183 mm | 519 px |

Check the target venue instead of treating these as universal limits.

### Separate content, padding, and margin

For each panel:

```text
total width =
  margin left
  + panel-label width
  + rendered left decorations
  + pad left
  + axes content width
  + margin right

total height =
  margin top
  + panel-label height
  + rendered top decorations
  + pad top
  + axes content height
  + margin bottom
```

This distinction is the core of the source layout system. `pad_left` and `pad_top`
control label clearance; margins control inter-panel rhythm; `width` and `height`
control the actual data area.

### Compose by visual role

- Give plot types the aspect ratio they need instead of forcing a uniform grid.
- Align related quantitative axes when comparison matters.
- Keep shared category order, limits, and color semantics across panels.
- Use automatic left-to-right flow and wrap at a maximum width.
- Use a forced newline only when narrative grouping matters.
- Use `below="A"` for a dependent panel that should remain vertically attached to
  panel A.
- Reserve title space as a separate band, not by pushing the first row down manually.

Measure artist extents after the first draw. Recalculate panel positions when titles,
y-axis decorations, colorbars, dendrograms, or other helper axes change the occupied
space. Anchor helper axes relative to their host axes so later relayout does not
detach them.

## Export

Configure:

```python
import matplotlib as mpl

mpl.rcParams.update({
    "savefig.dpi": 288,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.01,
    "savefig.transparent": True,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})
```

Keep the same measured bounding box across raster and vector outputs. Apply a Unicode
font fallback before saving. For SVG, confirm the editor sees text nodes rather than
paths. If a PDF-to-SVG conversion tool is used, verify that bold weight, font-family
names, transforms, and clipping survive the conversion.
