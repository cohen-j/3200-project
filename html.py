from lark import Lark
import dominate
from dominate.tags import *

my_grammar = """

start: "<!DOCTYPE html>" html -> start

//tag: "<" content attribute* ">" (tag | text)*"</" content ">"

html: "<html>" head* body* "</html>" -> html
head: "<head>" title* div* "</head>" -> head
body: "<body>" (div* | p* | h1* | h2* | h3* | h4* | a* | img* | ul* | ol* | li*)* "</body>" -> body
div: "<div>" (div* | p* | h1* | h2* | h3* | h4* | a* | img* | ul* | ol* | li*)* "</div>" -> div
title: "<title>" WORD* "</title>" -> title
p: "<p>" WORD* "</p>" -> p
h1: "<h1>" WORD* "</h1>" -> h1
h2: "<h2>" WORD* "</h2>" -> h2
h3: "<h3>" WORD* "</h3>" -> h3
h4: "<h4>" WORD* "</h4>" -> h4
a: "<a href=" ESCAPED_STRING ">" WORD* "</a>" -> a
img: "<img src=" ESCAPED_STRING "/>" -> img
ul: "<ul>" li* "</ul>" -> ul
ol: "<ol>" li* "</ol>" -> ol
li: "<li>" WORD* "</li>" -> li


// tag: html
//     | head
//     | body
//     | div
//     | title
//     | p
//     | h1
//     | h2
//     | h3
//     | h4
//     | a
//     | img
//     | ul
//     | ol
//     | li

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

test2 = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
</body>
</html>
"""

parser = Lark(my_grammar)

doc = dominate.document('')

print(parser.parse(test).pretty())

def run_instruction(t):
    if t.data == 'start':
        doc = dominate.document('your page')
        print('checked start')
        run_instruction(t.children)
    elif t.data == 'html':
        print('checked html')
        map(run_instruction, t.children)
    elif t.data == 'head':
        print('checked head')
        with doc.head:
            map(run_instruction, t.children)
    elif t.data == 'body':
        print('checked body')
        with doc.body:
            map(run_instruction, t.children)
    elif t.data == 'div':
        div(map(run_instruction, t.children))
    elif t.data == 'title':
        title(t.children)
    elif t.data == 'p':
        print('checked p')
        p(t.children)
    elif t.data == 'h1':
        h1(t.children)
    elif t.data == 'h2':
        h2(t.children)
    elif t.data == 'h3':
        h3(t.children)
    elif t.data == 'h4':
        h4(t.children)
    elif t.data == 'a':
        a(href=t.children)
    elif t.data == 'img':
        img(src=t.children)
    elif t.data == 'ul':
        ul(map(run_instruction, t.children))
    elif t.data == 'ol':
        ol(map(run_instruction, t.children))
    elif t.data == 'li':
        li(t.children)
    else:
        raise SyntaxError('Unknown instruction: %s' % t.children)


def run_html(program):
    parse_tree = parser.parse(program)
    print(parse_tree)
    run_instruction(parse_tree)


def main():
    while True:
        sequence = input('Write some HTML: ')
        if sequence == 'end':
            return 0
        try:
            run_html(sequence)
            print(doc)
        except Exception as e:
            print(e)

main()