``Patch`` now respects the dash offset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Previously, the offset of a dash tuple passed as the *linestyle* of a `.Patch`
(e.g. ``linestyle=(10, (10, 10))``) was silently ignored and treated as 0.  The
offset is now applied when drawing, consistent with `.Line2D`.
