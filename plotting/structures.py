"""
Per-structure settings for the Bland-Altman plots.

The key is the Excel sheet name and the command line option.
"""

import numpy as np

BA_STRUCTURES = {
    "brain_stem": {
        "value_cols": ["VMAT_REF", "VMAT_Arc1"],
        "title": r"VMAT$_{\mathbf{Ref}}$ - VMAT$_{\mathbf{Arc1}}$",
        "xlabel": r"Μέσος όρος D$_{\mathbf{max}}$ (Gy)",
        "ylabel": r"Εγκεφαλικό στέλεχος: Διαφορά D$_{\mathbf{max}}$ (Gy)",
        "xlim": None,
        "xticks": None,
        "ylim": (-4, 6),
        "yticks": np.arange(-4, 6.5, 2),
    },
    "buccal_fat": {
        "value_cols": ["SECT", "VNC"],
        "title": None,
        "xlabel": r"HU Average",
        "ylabel": r"Buccal Fat: HU Difference",
        "xlim": None,
        "xticks": None,
        "ylim": (-20, 30),
        "yticks": np.arange(-20, 35, 5),
    },
}
