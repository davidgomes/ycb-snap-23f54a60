Fix the dash offset of the Patch class
--------------------------------------

Formerly, when setting the line style on a `.Patch` object using a dash tuple,
the offset was ignored. Now the offset is applied to the Patch as expected and
it can be used as it is used with `.Line2D` objects.
