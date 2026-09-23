"""Test the HTML builder and check output against XPath."""
import re

import pytest

from sphinx import addnodes


@pytest.mark.sphinx(testroot='toctree-glob')
def test_relations(app, status, warning):
    app.builder.build_all()
    assert app.builder.relations['index'] == [None, None, 'foo']
    assert app.builder.relations['foo'] == ['index', 'index', 'bar/index']
    assert app.builder.relations['bar/index'] == ['index', 'foo', 'bar/bar_1']
    assert app.builder.relations['bar/bar_1'] == ['bar/index', 'bar/index', 'bar/bar_2']
    assert app.builder.relations['bar/bar_2'] == ['bar/index', 'bar/bar_1', 'bar/bar_3']
    assert app.builder.relations['bar/bar_3'] == ['bar/index', 'bar/bar_2', 'bar/bar_4/index']
    assert app.builder.relations['bar/bar_4/index'] == ['bar/index', 'bar/bar_3', 'baz']
    assert app.builder.relations['baz'] == ['index', 'bar/bar_4/index', 'qux/index']
    assert app.builder.relations['qux/index'] == ['index', 'baz', 'qux/qux_1']
    assert app.builder.relations['qux/qux_1'] == ['qux/index', 'qux/index', 'qux/qux_2']
    assert app.builder.relations['qux/qux_2'] == ['qux/index', 'qux/qux_1', None]
    assert 'quux' not in app.builder.relations


@pytest.mark.sphinx('singlehtml', testroot='toctree-empty')
def test_singlehtml_toctree(app, status, warning):
    app.builder.build_all()
    try:
        app.builder._get_local_toctree('index')
    except AttributeError:
        pytest.fail('Unexpected AttributeError in app.builder.fix_refuris')


@pytest.mark.sphinx('html', testroot='toctree-index')
def test_toctree_index(app, status, warning):
    app.build()
    assert 'toctree contains reference' not in warning.getvalue()

    toctree = list(app.env.get_doctree('index').findall(addnodes.toctree))[1]
    assert toctree['entries'] == [(None, 'genindex'), (None, 'modindex'),
                                  ('Search Page', 'search')]
    assert toctree['includefiles'] == []

    content = (app.outdir / 'index.html').read_text(encoding='utf8')
    assert re.search(r'<a class="reference internal" href="genindex.html">Index</a>',
                     content)
    assert re.search(r'<a class="reference internal" href="py-modindex.html">'
                     r'Module Index</a>', content)
    assert re.search(r'<a class="reference internal" href="search.html">Search Page</a>',
                     content)


@pytest.mark.sphinx(testroot='toctree', srcdir="numbered-toctree")
def test_numbered_toctree(app, status, warning):
    # give argument to :numbered: option
    index = (app.srcdir / 'index.rst').read_text(encoding='utf8')
    index = re.sub(':numbered:.*', ':numbered: 1', index)
    (app.srcdir / 'index.rst').write_text(index, encoding='utf8')
    app.builder.build_all()
