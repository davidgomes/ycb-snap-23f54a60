from django.template.defaultfilters import escapeseq
from django.test import SimpleTestCase
from django.utils.safestring import SafeString, mark_safe

from ..utils import setup


class EscapeseqTests(SimpleTestCase):
    """
    The "escapeseq" filter escapes each element of a sequence. It works the
    same whether autoescape is on or off, and has no effect on strings already
    marked as safe.
    """

    @setup(
        {"escapeseq01": '{{ a|escapeseq|join:", " }} -- {{ b|escapeseq|join:", " }}'}
    )
    def test_escapeseq01(self):
        output = self.engine.render_to_string(
            "escapeseq01",
            {"a": ["x&y", "<z>"], "b": [mark_safe("x&y"), mark_safe("<z>")]},
        )
        self.assertEqual(output, "x&amp;y, &lt;z&gt; -- x&y, <z>")

    @setup(
        {
            "escapeseq02": (
                '{% autoescape off %}{{ a|join:", " }} -- '
                '{{ a|escapeseq|join:", " }} -- '
                '{{ b|escapeseq|join:", " }}{% endautoescape %}'
            )
        }
    )
    def test_escapeseq02(self):
        output = self.engine.render_to_string(
            "escapeseq02",
            {"a": ["x&y", "<z>"], "b": [mark_safe("x&y"), mark_safe("<z>")]},
        )
        self.assertEqual(output, "x&y, <z> -- x&amp;y, &lt;z&gt; -- x&y, <z>")


class FunctionTests(SimpleTestCase):
    def test_escapes_each_item(self):
        result = escapeseq(["x&y", "<z>"])
        self.assertEqual(result, ["x&amp;y", "&lt;z&gt;"])
        self.assertTrue(all(isinstance(item, SafeString) for item in result))

    def test_preserves_safe_strings(self):
        result = escapeseq([mark_safe("x&y"), mark_safe("<z>")])
        self.assertEqual(result, ["x&y", "<z>"])
