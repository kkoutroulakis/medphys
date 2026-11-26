"""Figures are saved as valid images, at the expected paths."""

import sys

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from PIL import Image

import main
from plotting import plots
from plotting.helpers import grouped_bar_chart
from plotting.registry import OPTIONS, OPTIONS_REQUIRED, PLOTS
from plotting.structures import BA_STRUCTURES

# (plot key, option, path relative to the output folder)
EXPECTED = [
    *[("bland-altman", s, f"bland_altman/{s}.jpg") for s in BA_STRUCTURES],
    ("double-barchart", None, "barcharts/fsect_fvm.jpg"),
    ("triple-barchart", None, "barcharts/triple_barchart.jpg"),
    ("circle-diagram", None, "diagrams/overlapping_circles_shape.jpg"),
    ("circle-diagram", "shape", "diagrams/overlapping_circles_shape.jpg"),
    ("circle-diagram", "context", "diagrams/overlapping_circles_context.jpg"),
]
IDS = [key if option is None else f"{key}-{option}" for key, option, _ in EXPECTED]


def saved_files(out_dir):
    """All files under out_dir, as sorted relative paths."""

    if not out_dir:
        return []
    return sorted(
        p.relative_to(out_dir).as_posix() for p in out_dir.rglob("*") if p.is_file()
    )


def run_plot(key, option):
    func = PLOTS[key]

    if option is None:
        func()
    else:
        func(option)


def run_cli(monkeypatch, *argv):
    """Run main.py as if called from the command line."""

    monkeypatch.setattr(sys, "argv", ["main.py", *argv])
    args = main.parse_args()
    main.run(args.plot, args.option)


def bland_altman_template():
    """A real structure entry, to build test structures from."""

    return next(iter(BA_STRUCTURES.values()))


# ---------------------------------------------------------------------------
# Each plot saves exactly one file, at its exepected path
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("key", "option", "path"), EXPECTED, ids=IDS)
def test_plot_saves_one_file_at_expected_path(fake_data, out_dir, key, option, path):
    run_plot(key, option)

    assert saved_files(out_dir) == [path]


def test_every_registered_plot_has_an_expected_path():
    """A new plot or option must be added to EXPECTED, so it gets tested."""

    expected = {(key, option) for key, option, _ in EXPECTED}
    for key in PLOTS:
        variants = list(OPTIONS[key])
        if not OPTIONS_REQUIRED[key]:
            variants.append(None)
        for option in variants:
            assert (key, option) in expected, f"add ({key!r}, {option!r}) to EXPECTED"


# ---------------------------------------------------------------------------
# Every structure gets its own file
# ---------------------------------------------------------------------------


def test_each_structure_gets_its_own_file(tmp_path, out_dir, monkeypatch):
    template = bland_altman_template()
    col_a, col_b = template["value_cols"]
    excel = tmp_path / "ba.xlsx"

    with pd.ExcelWriter(excel) as writer:
        pd.DataFrame({col_a: [40, 45, 50], col_b: [39, 44, 49]}).to_excel(
            writer, sheet_name="organ_one", index=False
        )
        pd.DataFrame({col_a: [50, 52, 54], col_b: [52, 55, 58]}).to_excel(
            writer, sheet_name="organ_two", index=False
        )
    monkeypatch.setattr(plots, "BLAND_ALTMAN_DATA", excel)
    monkeypatch.setattr(
        plots, "BA_STRUCTURES", {"organ_one": template, "organ_two": template}
    )

    plots.run_bland_altman("organ_one")
    plots.run_bland_altman("organ_two")

    assert saved_files(out_dir) == [
        "bland_altman/organ_one.jpg",
        "bland_altman/organ_two.jpg",
    ]

    one = (out_dir / "bland_altman" / "organ_one.jpg").read_bytes()
    two = (out_dir / "bland_altman" / "organ_two.jpg").read_bytes()

    assert one != two, "different data should give different images"


# ---------------------------------------------------------------------------
# The command line saves the same file
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("key", "option", "path"), EXPECTED, ids=IDS)
def test_cli_saves_one_file_at_expected_path(
    fake_data, out_dir, monkeypatch, key, option, path
):
    run_cli(monkeypatch, key, *([] if option is None else [option]))

    assert saved_files(out_dir) == [path]


def test_missing_output_folders_are_created(fake_data, out_dir):
    assert not out_dir.exists()

    run_plot("double-barchart", None)

    assert (out_dir / "barcharts").is_dir()


# ---------------------------------------------------------------------------
# A failed run saves nothing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "argv",
    [
        ["bland-altman"],
        ["bland-altman", "not_a_structure"],
        ["double-barchart", "extra"],
        ["circle-diagram", "not_a_style"],
    ],
    ids=["missing-structure", "unknown-structure", "unexpected-option", "bad-style"],
)
def test_cli_rejects_bad_arguments_and_saves_nothing(
    fake_data, out_dir, monkeypatch, argv
):
    with pytest.raises(SystemExit) as exc:
        run_cli(monkeypatch, *argv)

    assert exc.value.code == 2
    assert saved_files(out_dir) == []


@pytest.mark.parametrize("problem", ["missing-sheet", "missing-column"])
def test_bad_excel_layout_saves_nothing(tmp_path, out_dir, monkeypatch, problem):
    template = bland_altman_template()
    col_a, col_b = template["value_cols"]
    excel = tmp_path / "ba.xlsx"
    second_col = "wrong_name" if problem == "missing-column" else col_b

    pd.DataFrame({col_a: [1, 2], second_col: [1, 2]}).to_excel(
        excel, sheet_name="organ", index=False
    )

    structure = "other_organ" if problem == "missing-sheet" else "organ"
    monkeypatch.setattr(plots, "BLAND_ALTMAN_DATA", excel)
    monkeypatch.setattr(plots, "BA_STRUCTURES", {structure: template})

    with pytest.raises(ValueError):
        plots.run_bland_altman(structure)

    assert saved_files(out_dir) == []


# ---------------------------------------------------------------------------
# The saved file is a valid JPEG
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("key", "option", "path"), EXPECTED, ids=IDS)
def test_saved_file_is_valid_jpeg(fake_data, out_dir, key, option, path):
    run_plot(key, option)
    file = out_dir / path

    assert file.stat().st_size > 0
    with Image.open(file) as img:
        assert img.format == "JPEG"
        img.verify()  # raises if file is corrupt


# ---------------------------------------------------------------------------
# No figures left open after saving
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("key", "option", "path"), EXPECTED, ids=IDS)
def test_no_figures_left_open(fake_data, key, option, path):
    run_plot(key, option)

    assert plt.get_fignums() == []


def test_figure_passed_in_by_caller_stays_open(tmp_path):
    fig, axes = plt.subplots(1, 2)

    grouped_bar_chart(
        pd.DataFrame({"a": [1, 2]}), ["a"], ax=axes[0], save_path=tmp_path / "x/jpg"
    )

    assert plt.fignum_exists(fig.number)
