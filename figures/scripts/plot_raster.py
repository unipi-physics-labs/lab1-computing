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

"""Illustrate why rastered formats suck for plots.
"""

import numpy as np
from aptapy.plotting import plt, setup_gca

from common import DATA_DIR, savefigs


def plot_raster():
    """Plot a rastered image of a sine function.
    """
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    plt.figure()
    plt.plot(x, y)
    plt.gca().grid(True, linestyle="--", linewidth=0.6)
    for dpi in (30, 300):
        savefigs(f"raster_sine_{dpi}dpi", formats=("png",), dpi=dpi)


def run():
    plot_raster()



if __name__ == "__main__":
    run()
    plt.show()
