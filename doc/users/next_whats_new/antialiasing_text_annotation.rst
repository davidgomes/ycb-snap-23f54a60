Control antialiasing for Text and Annotation
--------------------------------------------

`~.Text` and `~.Annotation` objects (and the functions creating them, such as
`~.Axes.text`, `~.Figure.text` and `~.Axes.annotate`) now accept an
*antialiased* keyword argument, and have ``set_antialiased`` /
``get_antialiased`` methods, to control antialiasing on a per-artist basis
instead of only via :rc:`text.antialiased`.

.. code-block:: python

    plt.text(0.5, 0.5, '6 inches x 2 inches', antialiased=True)
    ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
                arrowprops=dict(facecolor='black', shrink=0.05),
                antialiased=False)

If *antialiased* is not specified, :rc:`text.antialiased` is used. This is
currently supported by the Agg and Cairo backends.
