Auto-selection of contour levels for boolean inputs
---------------------------------------------------

If the height array given to `.Axes.contour` or `.Axes.contourf` (or
`.Axes.tricontour` / `.Axes.tricontourf`) is of bool dtype, the levels now
default to ``[0.5]`` or ``[0, 0.5, 1]`` respectively, i.e. a single line (or
boundary between two filled regions) separating the True and False areas.

.. plot::
    :include-source: true

    from matplotlib import pyplot as plt
    import numpy as np

    ii, jj = np.ogrid[:100, :100]
    zs = (ii + jj) % 20 < 10
    fig, axs = plt.subplots(1, 2, figsize=(6, 3))
    axs[0].contour(zs)
    axs[1].contourf(zs)
