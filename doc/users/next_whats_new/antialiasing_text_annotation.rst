Per-artist antialiasing for text and annotations
------------------------------------------------
``Text`` and ``Annotation`` now accept *antialiased*, and expose
`.Text.get_antialiased` / `.Text.set_antialiased`. When *antialiased* is
omitted, the artist copies :rc:`text.antialiased` at creation::

    fig.text(0.5, 0.5, "hello", antialiased=False)
    ax.annotate("local max", xy=(2, 1), xytext=(3, 1.5), antialiased=False)

Math expressions still use :rc:`text.antialiased` and ignore *antialiased*.
The Agg and Cairo backends honor the per-artist flag for regular text.
