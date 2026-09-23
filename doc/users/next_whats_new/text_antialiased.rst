Per-artist antialiasing for `.Text`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`.Text` (and subclasses such as `.Annotation`) now support
``get_antialiased`` / ``set_antialiased``.  When unset, the value still comes
from :rc:`text.antialiased`.  Backends read the flag from the graphics context
while drawing, so individual labels can be antialiased independently of the
global setting.
