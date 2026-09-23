Support customizing antialiasing for text and annotation
--------------------------------------------------------
``matplotlib.pyplot.annotate()`` and ``matplotlib.pyplot.text()`` now support
the *antialiased* parameter. When *antialiased* is ``True``, antialiasing is
applied to the text. When it is ``False``, antialiasing is not applied. When
it is not specified, the value is taken from :rc:`text.antialiased` at the
time the ``Text`` or ``Annotation`` is created.

Examples::

    mpl.text.Text(.5, .5, "foo\nbar", antialiased=True)
    plt.text(0.5, 0.5, '6 inches x 2 inches', antialiased=True)
    ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5), antialiased=False)

The same setting applies to the whole text, including mathtext::

    # no part will be antialiased for the text below
    plt.text(0.5, 0.25, r"$I'm \sqrt{x}$", antialiased=False)

Antialiasing for tick labels is taken from :rc:`text.antialiased` when the
labels are created (usually when a ``Figure`` is created). Changing
:rc:`text.antialiased` afterwards does not update text that already exists.

Create and save the figure under the same rc setting when you want that
setting to apply::

    # previously this was a no-op, now it is what works
    with rccontext({'text.antialiased': False}):
        fig, ax = plt.subplots()
        ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5))
        fig.savefig('/tmp/test.png')

    # previously this had an effect, now this is a no-op
    fig, ax = plt.subplots()
    ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5))
    with rccontext({'text.antialiased': False}):
        fig.savefig('/tmp/test.png')
