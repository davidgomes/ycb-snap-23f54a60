Auto-selection of contour levels for boolean inputs
---------------------------------------------------

If the height array given to `.Axes.contour` (or `.Axes.tricontour`) is a
boolean array, the levels now default to ``[0.5]``, drawing the boundary
between the True and False regions.  `.Axes.contourf` (and
`.Axes.tricontourf`) default to levels ``[0, 0.5, 1]`` in that case.
