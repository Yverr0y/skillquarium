# CNSPlots implementation recipes

Use these patterns as starting points. Keep data preparation and inferential decisions
outside the plotting call unless the library helper exactly matches the analysis plan.

## Contents

1. [Plot chooser](#plot-chooser)
2. [Built-in cnsplots pattern](#built-in-cnsplots-pattern)
3. [External axes pattern](#external-axes-pattern)
4. [Multi-panel pattern](#multi-panel-pattern)
5. [Custom graphical objects](#custom-graphical-objects)
6. [Specialized scientific plots](#specialized-scientific-plots)

## Plot chooser

| Question | Plot/API |
|---|---|
| Compare distributions | `boxplot`, `violinplot`, `stripplot`, `ridgeplot` |
| Compare estimates or means | `barplot`, `lollipopplot`, `forestplot`, `slopeplot` |
| Show association or trajectory | `scatterplot`, `regplot`, `lineplot` |
| Show a distribution | `histplot`, `kdeplot`, `distplot`, `qqplot` |
| Show composition | `stackplot`, `pieplot`, `donutplot` |
| Show matrices or enrichment | `heatmapplot`, `dotplot`, `confusionplot` |
| Show differential expression | `volcanoplot`, `gseaplot` |
| Show classification performance | `rocplot`, `confusionplot` |
| Show time-to-event analysis | `survivalplot`, `cumulativeincidenceplot` |
| Show sets or flows | `vennplot`, `upsetplot`, `sankeyplot` |

## Built-in cnsplots pattern

```python
import cnsplots as cns

with cns.settings.context(
    palette_qual="OkabeIto",
    pvalue_format="full",
    pvalue_loc="inside",
):
    cns.figure(width=252, height=190)
    ax = cns.boxplot(
        data=df,
        x="condition",
        y="response",
        order=["Control", "Low", "High"],
        pairs=[("Control", "Low"), ("Control", "High")],
    )
    ax.set_xlabel("")
    ax.set_ylabel("Response (a.u.)")
    cns.savefig("response.svg")
```

Confirm from the installed version which statistical test the chosen helper performs.
Report that test, sidedness, multiplicity correction, and exact sample unit.

## External axes pattern

Use cnsplots as the style and export layer:

```python
import cnsplots as cns
import matplotlib.pyplot as plt
import seaborn as sns

cns.setup_matplotlib(color_cycle="OkabeIto")
fig, ax = plt.subplots(figsize=(252 / 72, 180 / 72), dpi=144)

sns.scatterplot(
    data=df,
    x="x",
    y="y",
    hue="class",
    s=10,
    linewidth=0,
    rasterized=True,
    ax=ax,
)
ax.set(xlabel="Dimension 1", ylabel="Dimension 2")
cns.setup_ax(ax)
cns.take_legend_out(title="Class", ax=ax)
cns.savefig("embedding.svg")
```

Keep labels and legend vector even when the point cloud is rasterized.

## Multi-panel pattern

```python
import cnsplots as cns

mp = cns.multipanel(max_width=518, title="Integrated analysis", loc="left")

ax_a = mp.panel(
    "A",
    width=150,
    height=145,
    pad_left=8,
    pad_top=6,
    margin_bottom=18,
)
cns.violinplot(data=df, x="group", y="score", ax=ax_a)
ax_a.set(xlabel="", ylabel="Score")

ax_b = mp.panel(
    "B",
    width=220,
    height=145,
    pad_left=8,
    pad_top=6,
    margin_right=0,
)
cns.scatterplot(data=emb, x="x", y="y", hue="class", s=5, ax=ax_b)
cns.take_legend_out(ax=ax_b)

ax_c = mp.panel(
    "C",
    width=150,
    height=90,
    pad_left=8,
    below="A",
)
cns.barplot(data=summary, x="group", y="estimate", ax=ax_c)

cns.savefig("integrated-analysis.svg")
```

Use `mp.get_axes("A")` only when an axes was not retained. Use `mp.newline()` to
express narrative row breaks; use `below=` when a panel must stay attached to another
panel as a vertical subtree.

## Custom graphical objects

### Lollipop

```python
ax.vlines(x, 0, value, color=colors, linewidth=0.8, alpha=0.4, zorder=2)
ax.scatter(x, value, color=colors, s=18, linewidth=0, zorder=3)
ax.errorbar(
    x,
    value,
    yerr=error,
    fmt="none",
    ecolor="black",
    elinewidth=0.7,
    capsize=2,
    zorder=4,
)
```

### Estimate or forest plot

```python
ax.errorbar(
    estimate,
    y,
    xerr=[lower_error, upper_error],
    fmt="s",
    markersize=3,
    markeredgewidth=0.8,
    elinewidth=0.8,
    capsize=2,
)
ax.axvline(null_value, color="black", linestyle="--", linewidth=0.8)
```

Offset multiple groups slightly around each y position; keep their colors stable. Add
a secondary p-value panel only if it contributes information not already encoded.

### Line plus uncertainty

```python
ax.plot(x, mean, color=color, linewidth=1.2, label=label, zorder=3)
ax.fill_between(
    x,
    lower,
    upper,
    color=color,
    alpha=0.18,
    linewidth=0,
    zorder=1,
)
```

State what the band represents. Do not call it a confidence interval unless it is one.

## Specialized scientific plots

### Volcano

Use a neutral baseline layer and a sparse label layer:

```python
ax = cns.volcanoplot(
    data=de,
    x="log2FoldChange",
    y="-log10(padj)",
    symbol="gene",
    show_list=["TP53", "EGFR", "KRAS"],
)
```

Compute transformed p-values safely before plotting, define fold-change and adjusted
p-value thresholds in the analysis, and label a prespecified or defensible subset.
Keep the dense scatter rasterized and the annotations vector.

### Heatmap

```python
plotter = cns.heatmapplot(
    adata,
    layer="scaled",
    row_annotation=["cell_type", "batch"],
    col_cluster=True,
    cmap="BuRd_custom",
    label="Scaled expression",
    rasterized=True,
)
```

Use qualitative mappings for categorical annotations and sequential mappings for
numeric annotations. Supply explicit annotation color dictionaries when identities
must remain stable across figures. Keep dendrograms, labels, and colorbars attached to
the heatmap host during relayout.

### Stacked composition

```python
ax = cns.stackplot(
    data=df,
    x="sample",
    stack="cell_type",
    stack_order=cell_type_order,
    normalize=True,
)
ax.set_ylabel("Fraction")
```

Preserve the same stack order across samples and panels. Use counts when sample sizes
matter; use normalized fractions only when the denominator is clear.

### Sankey or alluvial flow

```python
ax = cns.sankeyplot(
    data=transitions,
    x="state_before",
    y="state_after",
    label_rotation=0,
)
```

The public API counts rows for each source-target pair. Expand or transform weighted
input explicitly only when that operation is statistically valid. The public API
derives its colors; build the flow from Matplotlib artists when a fixed semantic color
dictionary or asymmetric weights are required. Use terminal bars as anchors,
semi-transparent ribbons for flow, and direct labels outside the diagram. Hide axes
only when scale ticks genuinely add no meaning.

### Unicode and export

```python
cns.apply_unicode_font(ax)
cns.savefig("figure.svg")
cns.savefig("figure.pdf")
cns.savefig("figure.png")
```

Open the saved SVG in a vector editor or inspect its XML. Confirm labels are text,
bold panel labels remain bold, clip paths are sane, and the PNG has the same visible
bounds.
