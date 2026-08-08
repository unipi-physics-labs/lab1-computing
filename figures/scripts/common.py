# Copyright (C) 2026, Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).parent.parent

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "generated"


def savefigs(file_name: str, formats: tuple[str] = ("svg", "pdf")) -> None:
    """Save the current figure in the specified formats.
    """
    for fmt in formats:
        plt.savefig(OUTPUT_DIR / f"{file_name}.{fmt}")