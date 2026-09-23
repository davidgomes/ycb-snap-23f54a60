``Locator.nonsingular`` returns an increasing range
----------------------------------------------------

`Locator.nonsingular` (introduced in Matplotlib 3.1) now returns a range
``v0, v1`` with ``v0 <= v1``.  This matches `~.ticker.LogLocator` and
`~.ticker.LogitLocator`, which already returned an increasing range.

`~.Axes.set_xlim`, `~.Axes.set_ylim`, and the 3D limit setters still honor
an inverted limit order, including on log scales.  Subclasses that override
`nonsingular` should return ``v0 <= v1`` as well; the axis will swap the
values back when the caller requested a reversed axis.
