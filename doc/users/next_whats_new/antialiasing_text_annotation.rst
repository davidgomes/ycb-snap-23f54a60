Default antialiasing for text can now be overridden per artist
--------------------------------------------------------------

Previously, antialiasing of text was always determined by
:rc:`text.antialiased`.  `.Text` and `.Annotation` objects now accept an
*antialiased* keyword argument, and have ``set_antialiased`` and
``get_antialiased`` methods, to control this on a per-artist basis.  This is
honored by the Agg and Cairo backends, including for mathtext rendered by Agg.

.. code-block::

    plt.text(0.5, 0.5, '6 inches x 2 inches', antialiased=True)
    ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5), antialiased=False)
