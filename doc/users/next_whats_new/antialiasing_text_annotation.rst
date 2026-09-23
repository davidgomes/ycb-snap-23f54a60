Antialiasing for text and annotation
------------------------------------

`.Text` and `.Annotation` objects (and therefore ``plt.text``,
``plt.annotate``, `.Axes.text`, `.Axes.annotate`, `.Figure.text`, etc.) now
support the *antialiased* parameter, as well as the
`.Text.set_antialiased` and `.Text.get_antialiased` methods, to control
antialiasing on a per-artist basis.  When *antialiased* is not given, it
defaults to :rc:`text.antialiased`.  This also applies to text containing
math expressions.

.. code-block:: python

    plt.text(0.5, 0.5, '6 inches x 2 inches', antialiased=True)
    ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5), antialiased=False)
