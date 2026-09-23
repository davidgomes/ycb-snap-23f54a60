``ContourSet.set_paths``
------------------------

`.ContourSet` now has a `~.ContourSet.set_paths` method, so the paths of all
contour levels can be replaced at once, e.g. with transformed versions::

    cs.set_paths(transformed_paths)

instead of mutating the list returned by `~.Collection.get_paths` in place.
