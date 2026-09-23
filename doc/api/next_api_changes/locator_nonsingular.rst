``Locator.nonsingular`` returns an increasing range
---------------------------------------------------

`Locator.nonsingular` (introduced in mpl 3.1) now returns a range ``v0, v1``
with ``v0 <= v1``. This behavior is consistent with the implementation of
``nonsingular`` by the `LogLocator` and `LogitLocator` subclasses.

``Axes.set_xlim`` and ``Axes.set_ylim`` still honor explicitly reversed
limits, including on log scales.
