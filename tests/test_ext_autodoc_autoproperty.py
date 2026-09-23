"""
    test_ext_autodoc_autoproperty
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly the Documenters; the auto
    directives are tested in a test source file translated by test_build.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import sys

import pytest

from .test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.prop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.prop',
        '   :module: target.properties',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.skipif(sys.version_info < (3, 9), reason='python 3.9+ is required.')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_class_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.ClassProp.classprop')
    assert list(actual) == [
        '',
        '.. py:property:: ClassProp.classprop',
        '   :module: target.properties',
        '   :classmethod:',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]

    actual = do_autodoc(app, 'property', 'target.properties.ClassProp.absclassprop')
    assert list(actual) == [
        '',
        '.. py:property:: ClassProp.absclassprop',
        '   :module: target.properties',
        '   :abstractmethod:',
        '   :classmethod:',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.skipif(sys.version_info < (3, 9), reason='python 3.9+ is required.')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_class_properties_as_members(app):
    options = {'members': None}
    actual = do_autodoc(app, 'class', 'target.properties.ClassProp', options)
    assert list(actual) == [
        '',
        '.. py:class:: ClassProp()',
        '   :module: target.properties',
        '',
        '   docstring',
        '',
        '',
        '   .. py:property:: ClassProp.absclassprop',
        '      :module: target.properties',
        '      :abstractmethod:',
        '      :classmethod:',
        '      :type: int',
        '',
        '      docstring',
        '',
        '',
        '   .. py:property:: ClassProp.classprop',
        '      :module: target.properties',
        '      :classmethod:',
        '      :type: int',
        '',
        '      docstring',
        '',
    ]

    actual = do_autodoc(app, 'class', 'target.properties.ClassPropSub', options)
    assert list(actual) == [
        '',
        '.. py:class:: ClassPropSub()',
        '   :module: target.properties',
        '',
        '   docstring',
        '',
    ]

    options = {'members': None, 'inherited-members': None}
    actual = do_autodoc(app, 'class', 'target.properties.ClassPropSub', options)
    assert list(actual) == [
        '',
        '.. py:class:: ClassPropSub()',
        '   :module: target.properties',
        '',
        '   docstring',
        '',
        '',
        '   .. py:property:: ClassPropSub.absclassprop',
        '      :module: target.properties',
        '      :abstractmethod:',
        '      :classmethod:',
        '      :type: int',
        '',
        '      docstring',
        '',
        '',
        '   .. py:property:: ClassPropSub.classprop',
        '      :module: target.properties',
        '      :classmethod:',
        '      :type: int',
        '',
        '      docstring',
        '',
    ]

    options = {'members': None}
    actual = do_autodoc(app, 'class', 'target.properties.Meta', options)
    assert list(actual) == [
        '',
        '.. py:class:: Meta',
        '   :module: target.properties',
        '',
        '   docstring',
        '',
        '',
        '   .. py:property:: Meta.metaprop',
        '      :module: target.properties',
        '      :classmethod:',
        '      :type: int',
        '',
        '      docstring',
        '',
    ]
