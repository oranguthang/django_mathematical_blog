from django import template
import mistune
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()


class MyInlineLexer(mistune.InlineLexer):
    def enable_latex_formulas(self):
        # add latex_formula rules
        self.rules.latex_formula = re.compile(
            r'\`\$'       # `$
            r'([\s\S]+?)' # some text
            r'\$\`'       # $`
        )

        self.default_rules.insert(0, 'latex_formula')

    def enable_color_blocks(self):
        self.rules.block_color = re.compile(
            r'\`\@([\w]+?)\@'  # `@color@
            r'([\s\S]+?)'      # some text
            r'\@\`'            # @`
        )

        self.default_rules.insert(10, 'block_color')

    def output_latex_formula(self, m):
        text = m.group(1)
        return self.renderer.latex_formula(text)

    def output_block_color(self, m):
        color = m.group(1)
        text = m.group(2)
        return self.renderer.block_color(color, text)


class MyRenderer(mistune.Renderer):
    def block_color(self, color, text):
        return '<span style="color:%s">%s</span>' % (color, text)

    def latex_formula(self, text):
        text = text.replace("+", "%2B")
        text = text.replace(" ", "%20")
        return '<img src="/blog/render_latex?formula=%s">' % text

    def block_code(self, code, lang=None):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)

    def table(self, header, body):
        return (
            '<table class="table table-bordered">\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)


@register.filter(name='markdown')
def markdown(value):
    renderer = MyRenderer()
    inline = MyInlineLexer(renderer)
    # enable the feature
    inline.enable_latex_formulas()
    inline.enable_color_blocks()
    markdown = mistune.Markdown(renderer=renderer, inline=inline)
    return markdown(value)
