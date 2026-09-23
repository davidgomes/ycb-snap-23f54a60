"""
    test_ext_autodoc_private_members
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly for private-members option.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_field(app):
    app.config.autoclass_content = 'class'
    options = {"members": None}
    actual = do_autodoc(app, 'module', 'target.private', options)
    assert list(actual) == [
        '',
        '.. py:module:: target.private',
        '',
        '',
        '.. py:function:: _public_function(name)',
        '   :module: target.private',
        '',
        '   public_function is a docstring().',
        '',
        '   :meta public:',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_field_and_private_members(app):
    app.config.autoclass_content = 'class'
    options = {"members": None,
               "private-members": None}
    actual = do_autodoc(app, 'module', 'target.private', options)
    assert list(actual) == [
        '',
        '.. py:module:: target.private',
        '',
        '',
        '.. py:function:: _public_function(name)',
        '   :module: target.private',
        '',
        '   public_function is a docstring().',
        '',
        '   :meta public:',
        '',
        '',
        '.. py:function:: private_function(name)',
        '   :module: target.private',
        '',
        '   private_function is a docstring().',
        '',
        '   :meta private:',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_with_specific_names(app):
    options = {"members": None,
               "private-members": "_private_one"}
    actual = do_autodoc(app, 'module', 'target.private_members', options)
    assert list(actual) == [
        '',
        '.. py:module:: target.private_members',
        '',
        '',
        '.. py:function:: _private_one()',
        '   :module: target.private_members',
        '',
        '   _private_one is a docstring().',
        '',
        '',
        '.. py:function:: public_function()',
        '   :module: target.private_members',
        '',
        '   public_function is a docstring().',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_without_members_option(app):
    options = {"private-members": "_private_two"}
    actual = do_autodoc(app, 'module', 'target.private_members', options)
    assert list(actual) == [
        '',
        '.. py:module:: target.private_members',
        '',
        '',
        '.. py:function:: _private_two()',
        '   :module: target.private_members',
        '',
        '   _private_two is a docstring().',
        '',
    ]
