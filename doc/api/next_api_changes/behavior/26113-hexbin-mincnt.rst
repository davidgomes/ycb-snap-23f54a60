``hexbin`` *mincnt* is inclusive when *C* is given
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previously, ``Axes.hexbin`` treated *mincnt* as inclusive when *C* was
omitted (cells with ``count >= mincnt`` were shown) but exclusive when *C*
was given (cells were shown only when ``count > mincnt``). *mincnt* is now
inclusive in both cases. When *C* is given and *mincnt* is left as ``None``,
cells still need at least one point before *reduce_C_function* is called.
Passing ``mincnt=0`` reduces empty cells as well.
