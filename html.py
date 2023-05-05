from lark import Lark
import dominate
from dominate.tags import *

my_grammar = """

start: "<!DOCTYPE html>" tag+

//tag: "<" content attribute* ">" (tag | text)*"</" content ">"

html: "<html>" tag* "</html>"
head: "<head>" tag* "</head>"
body: "<body>" tag* "</body>"
div: "<div>" tag* "</div>"
title: "<title>" WORD* "</title>"
p: "<p>" WORD* "</p>"
h1: "<h1>" WORD* "</h1>"
h2: "<h2>" WORD* "</h2>"
h3: "<h3>" WORD* "</h3>"
h4: "<h4>" WORD* "</h4>"
a: "<a href=" ESCAPED_STRING ">" WORD* "</a>"
img: "<img src=" ESCAPED_STRING "/>"
ul: "<ul>" tag* "</ul>"
ol: "<ol>" tag* "</ol>"
li: "<li>" WORD* "</li>"


?tag: html
    | head
    | body
    | div
    | title
    | p
    | h1
    | h2
    | h3
    | h4
    | a
    | img
    | ul
    | ol
    | li

attribute: attribute_name "=" ESCAPED_STRING
attribute_name: "style" -> style
    | "id" -> id
    | "class" -> class

// style: "style=" ESCAPED_STRING
// style_option: "margin" | "width" | "height" | "padding" |

id: "id=" WORD
class: "class=" WORD

%import common.WS   
%import common.WORD
%import common.ESCAPED_STRING
%import common.NUMBER

%ignore WS                     
"""

test = """
<!DOCTYPE html>
<html>
<head>
<title>LOL</title>
</head>
<body>
<h1>Hello</h1>
<p>Goodbye</p>
</body>
</html>
"""

parser = Lark(my_grammar)

doc = 0

print(parser.parse(test).pretty())

def run_instruction(t):
    if t.children == 'start':
        doc = dominate.document('your page')
        run_instruction(t.children)
    elif t.children == 'html':
        run_instruction(t.children)
    elif t.children == 'head':
        with doc.head:
            run_instruction(t.children)
    elif t.children == 'body':
        with doc.body:
            run_instruction(t.children)
    elif t.children == 'title':
        title(t.children)
    elif t.children == 'p':
        p(t.children)
    elif t.children == 'h1':
        h1(t.children)
    else:
        raise SyntaxError('Unknown instruction: %s' % t.children)


def run_html(program):
    parse_tree = parser.parse(program)
    for inst in parse_tree.children:
        run_instruction(inst)


def main():
    while True:
        sequence = input('Write some HTML: ')
        try:
            run_html(sequence)
            print(doc)
        except Exception as e:
            print(e)
    
print(parser.parse(test))