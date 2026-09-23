# Copyright (c) 2006, 2008, 2010, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2017, 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 yeting li <liyt@ios.ac.cn>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2020 bernie gray <bfgray3@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Generic classes/functions for pyreverse core/extensions. """
import os
import re
import sys
from typing import Optional, Tuple, Union

import astroid

RCFILE = ".pyreverserc"


def get_default_options():
    """Read config file and return list of options."""
    options = []
    home = os.environ.get("HOME", "")
    if home:
        rcfile = os.path.join(home, RCFILE)
        try:
            with open(rcfile) as file_handle:
                options = file_handle.read().split()
        except OSError:
            pass  # ignore if no config file found
    return options


def insert_default_options():
    """insert default options to sys.argv"""
    options = get_default_options()
    options.reverse()
    for arg in options:
        sys.argv.insert(1, arg)


# astroid utilities ###########################################################
SPECIAL = re.compile(r"^__([^\W_]_*)+__$")
PRIVATE = re.compile(r"^__(_*[^\W_])+_?$")
PROTECTED = re.compile(r"^_\w*$")


def get_visibility(name):
    """return the visibility from a name: public, protected, private or special"""
    if SPECIAL.match(name):
        visibility = "special"
    elif PRIVATE.match(name):
        visibility = "private"
    elif PROTECTED.match(name):
        visibility = "protected"

    else:
        visibility = "public"
    return visibility


ABSTRACT = re.compile(r"^.*Abstract.*")
FINAL = re.compile(r"^[^\W\da-z]*$")


def is_abstract(node):
    """return true if the given class node correspond to an abstract class
    definition
    """
    return ABSTRACT.match(node.name)


def is_final(node):
    """return true if the given class/function node correspond to final
    definition
    """
    return FINAL.match(node.name)


def is_interface(node):
    # bw compat
    return node.type == "interface"


def is_exception(node):
    # bw compat
    return node.type == "exception"


# Helpers #####################################################################

_CONSTRUCTOR = 1
_SPECIAL = 2
_PROTECTED = 4
_PRIVATE = 8
MODES = {
    "ALL": 0,
    "PUB_ONLY": _SPECIAL + _PROTECTED + _PRIVATE,
    "SPECIAL": _SPECIAL,
    "OTHER": _PROTECTED + _PRIVATE,
}
VIS_MOD = {
    "special": _SPECIAL,
    "protected": _PROTECTED,
    "private": _PRIVATE,
    "public": 0,
}


class FilterMixIn:
    """filter nodes according to a mode and nodes' visibility"""

    def __init__(self, mode):
        "init filter modes"
        __mode = 0
        for nummod in mode.split("+"):
            try:
                __mode += MODES[nummod]
            except KeyError as ex:
                print("Unknown filter mode %s" % ex, file=sys.stderr)
        self.__mode = __mode

    def show_attr(self, node):
        """return true if the node should be treated"""
        visibility = get_visibility(getattr(node, "name", node))
        return not self.__mode & VIS_MOD[visibility]


class ASTWalker:
    """a walker visiting a tree in preorder, calling on the handler:

    * visit_<class name> on entering a node, where class name is the class of
    the node in lower case

    * leave_<class name> on leaving a node, where class name is the class of
    the node in lower case
    """

    def __init__(self, handler):
        self.handler = handler
        self._cache = {}

    def walk(self, node, _done=None):
        """walk on the tree from <node>, getting callbacks from handler"""
        if _done is None:
            _done = set()
        if node in _done:
            raise AssertionError((id(node), node, node.parent))
        _done.add(node)
        self.visit(node)
        for child_node in node.get_children():
            assert child_node is not node
            self.walk(child_node, _done)
        self.leave(node)
        assert node.parent is not node

    def get_callbacks(self, node):
        """get callbacks from handler for the visited node"""
        klass = node.__class__
        methods = self._cache.get(klass)
        if methods is None:
            handler = self.handler
            kid = klass.__name__.lower()
            e_method = getattr(
                handler, "visit_%s" % kid, getattr(handler, "visit_default", None)
            )
            l_method = getattr(
                handler, "leave_%s" % kid, getattr(handler, "leave_default", None)
            )
            self._cache[klass] = (e_method, l_method)
        else:
            e_method, l_method = methods
        return e_method, l_method

    def visit(self, node):
        """walk on the tree from <node>, getting callbacks from handler"""
        method = self.get_callbacks(node)[0]
        if method is not None:
            method(node)

    def leave(self, node):
        """walk on the tree from <node>, getting callbacks from handler"""
        method = self.get_callbacks(node)[1]
        if method is not None:
            method(node)


class LocalsVisitor(ASTWalker):
    """visit a project by traversing the locals dictionary"""

    def __init__(self):
        ASTWalker.__init__(self, self)
        self._visited = set()

    def visit(self, node):
        """launch the visit starting from the given node"""
        if node in self._visited:
            return None

        self._visited.add(node)
        methods = self.get_callbacks(node)
        if methods[0] is not None:
            methods[0](node)
        if hasattr(node, "locals"):  # skip Instance and other proxy
            for local_node in node.values():
                self.visit(local_node)
        if methods[1] is not None:
            return methods[1](node)
        return None


def get_annotation_label(ann: astroid.node_classes.NodeNG) -> str:
    """return the text to display for the annotation node `ann`"""
    if isinstance(ann, astroid.Const) and isinstance(ann.value, str):
        # string annotations are forward references, e.g. "MyClass"
        return ann.value
    return ann.as_string()


def _get_argument_annotation(
    arguments: astroid.Arguments, name: str
) -> Tuple[
    Optional[astroid.node_classes.NodeNG], Optional[astroid.node_classes.NodeNG]
]:
    """return the annotation and the default value of the argument `name`"""
    annotated_args = zip(
        arguments.posonlyargs + arguments.args + arguments.kwonlyargs,
        arguments.posonlyargs_annotations
        + arguments.annotations
        + arguments.kwonlyargs_annotations,
    )
    ann = next((ann for arg, ann in annotated_args if arg.name == name), None)
    try:
        default = arguments.default_value(name)
    except astroid.NoDefault:
        default = None
    return ann, default


def _get_annotation_and_default(
    node: astroid.node_classes.NodeNG,
) -> Tuple[
    Optional[astroid.node_classes.NodeNG], Optional[astroid.node_classes.NodeNG]
]:
    """return the annotation of the assignment target `node` and the value
    assigned to it by default"""
    if isinstance(node.parent, astroid.AnnAssign):
        return node.parent.annotation, node.parent.value
    if isinstance(node, astroid.AssignName) and isinstance(
        node.parent, astroid.Arguments
    ):
        return _get_argument_annotation(node.parent, node.name)
    if (
        isinstance(node, astroid.AssignAttr)
        and isinstance(node.parent, astroid.Assign)
        and isinstance(node.parent.value, astroid.Name)
    ):
        # ``self.attr = name`` takes the annotation of ``name``, e.g. a parameter
        _, assignments = node.parent.value.lookup(node.parent.value.name)
        if len(assignments) == 1:
            return _get_annotation_and_default(assignments[0])
    return None, None


def get_annotation(
    node: Union[astroid.AssignAttr, astroid.AssignName]
) -> Optional[astroid.Name]:
    """return a node whose name is the annotation label of `node`, or None if
    `node` is not annotated

    The label of an annotation whose value defaults to None is wrapped in
    ``Optional``.
    """
    ann, default = _get_annotation_and_default(node)
    if ann is None:
        return None
    label = get_annotation_label(ann)
    if (
        isinstance(default, astroid.Const)
        and default.value is None
        and not label.startswith(("Optional[", "typing.Optional["))
    ):
        label = f"Optional[{label}]"
    return astroid.Name(
        name=label, lineno=ann.lineno, col_offset=ann.col_offset, parent=ann.parent
    )


def infer_node(node: Union[astroid.AssignAttr, astroid.AssignName]) -> set:
    """return a set containing the annotation of `node` if it exists,
    otherwise a set of the types inferred for `node`

    An annotation naming a class is resolved to that class, so that it is
    handled like an inferred type, e.g. to find associations.
    """
    ann = get_annotation(node)
    if ann is None:
        try:
            return set(node.infer())
        except astroid.InferenceError:
            return set()
    # the label node sits where the annotation was written, so a plain class
    # name resolves like the annotation would, while a label like
    # ``Optional[str]`` is not a valid name and fails to infer
    try:
        inferred = set(ann.infer())
    except astroid.InferenceError:
        return {ann}
    if all(isinstance(value, astroid.ClassDef) for value in inferred):
        return inferred
    return {ann}
