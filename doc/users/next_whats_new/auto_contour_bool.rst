Auto-detection of bool arrays passed to contour()
-------------------------------------------------

Passing a bool array to `~.Axes.contour` (or `~.Axes.tricontour`) without
specifying *levels* now uses ``levels=[0.5]``, i.e. draws the boundary line
between the True and False regions, instead of the default 8 levels which
would all be drawn on top of each other.  Likewise, `~.Axes.contourf` (and
`~.Axes.tricontourf`) default to ``levels=[0, 0.5, 1]`` for bool inputs.

.. plot::
    :include-source: true

    import matplotlib.pyplot as plt
    import numpy as np

    ii, jj = np.ogrid[:100, :100]
    im = (ii + jj) % 20 < 10

    fig, axs = plt.subplots(1, 2, layout='constrained')
    axs[0].imshow(im, cmap='gray')
    axs[0].contour(im)
    axs[1].imshow(im, cmap='gray')
    axs[1].contourf(im, alpha=.5)

    plt.show()
