The dash offset of `.Patch` edges is no longer ignored
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previously, when setting the linestyle of a `.Patch` object using a dash tuple
``(offset, (on_off_seq))``, the offset was ignored when drawing.  The offset is
now respected, consistent with `.Line2D` objects.
