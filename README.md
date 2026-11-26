# medphys

Figures for a medical study, generated from Excel data with matplotlib.

## Usage

```sh
uv run main.py -h                           # list available plots and their oprions
uv run main.py bland-altman <structure>     # structure is required
uv run main.py double-barchart
uv run main.py triple-barchart
uv run main.py circle-diagram <style>       # legend style: shape | context
```

Figures are written to `figures/` (not tracked by git).

## Data

Excel files go in `data/` (not tracked by git).

| File                     | Sheet                           | Columns                                                                | Used by           |
| ------------------------ | ------------------------------- | ---------------------------------------------------------------------- | ----------------- |
| `bland_altman_data.xlsx` | one per structure, e.g. `tumor` | set pre structure in `plotting/structures.py` (`tumor`: `SECT`, `VNC`) | `bland_-altman`   |
| `bar_charts_data.xlsx`   | `double_bar_chart`              | `FSECT`, `FVM`                                                         | `double-barchart` |
| `bar_charts_data.xlsx`   | `triple_bar_chart`              | `VSECT`, `VVM`, `Vintersection`                                        | `triple-barchart` |

Each row is one patient. Column headers are stripped of surrounding spaces.

## Project layout

```
config.py               paths to data and output folders
main.py                 command line entry point
plotting/
    plots.py            one registered function per figure, with its settings
    structures.py       pre-structure settings for the Bland-Altman plots
    helpers.py          reusable plot functions (Bland-Altman, grouped bars)
    diagrams.py         schemantic figures (overlapping circles)
    statistics.py       Bland-Altman statistics
    style.py            shared colors and matplotlib defaults
    registry.py         maps command-line keys to plot functions
tests/                  pytest tests
```

### Adding a plot

Add an entry to `BA_STRUCTURES` in `plotting/structures.py` and decorate it with `@register("key", "description")`.
Pass `options=(...)` to accent a second argument on the command line, and `options_required=True` if the user must always give one.

### Adding a Bland-Altman structure

Add an entry to `BA_STRUCTURES` in `plotting/structures.py`, keyed by the Excel sheet name, with the two columns to compare (`value_cols`),
the title, axis labels and (optionally) axis limits and ticks for the structure.

## Development

```sh
uv run pytest
uv run ruff check .
uv run ruff format .
```
