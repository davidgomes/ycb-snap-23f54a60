import sys

from abc import abstractmethod


class Foo:
    """docstring"""

    @property
    def prop(self) -> int:
        """docstring"""


if sys.version_info >= (3, 9):
    class ClassProp:
        """docstring"""

        @classmethod
        @property
        def classprop(cls) -> int:
            """docstring"""
            return 1

        @classmethod
        @property
        @abstractmethod
        def absclassprop(cls) -> int:
            """docstring"""
            return 2

    class ClassPropSub(ClassProp):
        """docstring"""

    class Meta(type):
        """docstring"""

        @classmethod
        @property
        def metaprop(cls) -> int:
            """docstring"""
            return 3
