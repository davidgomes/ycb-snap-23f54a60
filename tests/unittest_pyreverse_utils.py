# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Tests for pylint.pyreverse.utils"""

from unittest.mock import patch

import astroid
import pytest

from pylint.pyreverse.utils import get_annotation, infer_node


@pytest.mark.parametrize(
    "assign, label",
    [
        ("a: str = None", "Optional[str]"),
        ("a: str = 'mystr'", "str"),
        ("a: Optional[str] = 'str'", "Optional[str]"),
        ("a: Optional[str] = None", "Optional[str]"),
    ],
)
def test_get_annotation_annassign(assign, label):
    node = astroid.extract_node(assign)
    got = get_annotation(node.target).name
    assert got == label


@pytest.mark.parametrize(
    "init_method, label",
    [
        ("def __init__(self, x: str):                   self.x = x", "str"),
        ("def __init__(self, x: str = 'str'):           self.x = x", "str"),
        ("def __init__(self, x: str = None):            self.x = x", "Optional[str]"),
        ("def __init__(self, x: Optional[str]):         self.x = x", "Optional[str]"),
        ("def __init__(self, x: Optional[str] = None):  self.x = x", "Optional[str]"),
        ("def __init__(self, x: Optional[str] = 'str'): self.x = x", "Optional[str]"),
    ],
)
def test_get_annotation_assignattr(init_method, label):
    node = astroid.extract_node(
        f"""
        class A:
            {init_method}
        """
    )
    instance_attrs = node.instance_attrs
    for _, assign_attrs in instance_attrs.items():
        for assign_attr in assign_attrs:
            got = get_annotation(assign_attr).name
            assert isinstance(assign_attr, astroid.AssignAttr)
            assert got == label


def test_get_annotation_none_without_hint():
    node = astroid.extract_node(
        """
        class A:
            def __init__(self, x=None):
                self.x = x
        """
    )
    (assign_attr,) = node.instance_attrs["x"]
    assert get_annotation(assign_attr) is None


@patch("pylint.pyreverse.utils.get_annotation")
@patch("astroid.node_classes.NodeNG.infer", side_effect=astroid.InferenceError)
def test_infer_node_inference_error(mock_infer, mock_get_annotation):
    """Return an empty set if node.infer() raises InferenceError"""
    mock_get_annotation.return_value = None
    node = astroid.extract_node("a: str = 'mystr'")
    assert infer_node(node) == set()
    assert mock_infer.called
