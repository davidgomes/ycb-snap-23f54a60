from django.test import SimpleTestCase
from django.utils.safestring import mark_safe

from ..utils import setup


class EscapeseqTests(SimpleTestCase):
    @setup({"escapeseq01": '{{ a|escapeseq|join:", " }} -- {{ b|escapeseq|join:", " }}'})
    def test_basic(self):
        output = self.engine.render_to_string(
            "escapeseq01",
            {"a": ["x&y", "<p>"], "b": [mark_safe("x&y"), mark_safe("<p>")]},
        )
        self.assertEqual(output, "x&amp;y, &lt;p&gt; -- x&y, <p>")

    @setup(
        {
            "escapeseq02": (
                '{% autoescape off %}{{ a|escapeseq|join:", " }}'
                " -- "
                '{{ b|escapeseq|join:", " }}{% endautoescape %}'
            )
        }
    )
    def test_autoescape_off(self):
        output = self.engine.render_to_string(
            "escapeseq02",
            {"a": ["x&y", "<p>"], "b": [mark_safe("x&y"), mark_safe("<p>")]},
        )
        self.assertEqual(output, "x&amp;y, &lt;p&gt; -- x&y, <p>")
