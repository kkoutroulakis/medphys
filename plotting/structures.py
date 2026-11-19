"""
Per-structure settings for the Bland-Altman plots.

The key is the Excel sheet name and the command line option.
"""

import numpy as np

BA_STRUCTURES = {
    "brain_stem": {
        "title": r"VMAT$_{\mathbf{Ref}}$ - VMAT$_{\mathbf{Arc1}}$",
        "xlabel": r"Μέσος όρος D$_{\mathbf{max}}$ (Gy)",
        "ylabel": r"Εγκεφαλικό στέλεχος: Διαφορά D$_{\mathbf{max}}$ (Gy)",
        "xlim": None,
        "xticks": None,
        "ylim": (-4, 6),
        "yticks": np.arange(-4, 6.5, 2),
    }
}
