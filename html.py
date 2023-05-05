from lark import Lark

my_grammar = """

start: "<!DOCTYPE html>" html -> start

html: "<html>" head* body* "</html>" -> html
head: "<head>" title* div* "</head>" -> head
body: "<body>" (div* | p* | h1* | h2* | h3* | h4* | a* | img* | ul* | ol* | li*)* "</body>" -> body
div: "<div>" (div* | p* | h1* | h2* | h3* | h4* | a* | img* | ul* | ol* | li*)* "</div>" -> div
title: "<title>" (WORD* | SYMBOL | NUMBER*)* "</title>" -> title
p: "<p>" (WORD* | SYMBOL* | NUMBER*)* "</p>" -> p
h1: "<h1>"(WORD* | SYMBOL* | NUMBER*)* "</h1>" -> h1
h2: "<h2>" (WORD* | SYMBOL* | NUMBER*)* "</h2>" -> h2
h3: "<h3>" (WORD* | SYMBOL* | NUMBER*)* "</h3>" -> h3
h4: "<h4>" (WORD* | SYMBOL* | NUMBER*)* "</h4>" -> h4
a: "<a href=" ESCAPED_STRING ">" (WORD* | SYMBOL | NUMBER*)* "</a>" -> a
img: "<img src=" ESCAPED_STRING "/>" -> img
ul: "<ul>" li* "</ul>" -> ul
ol: "<ol>" li* "</ol>" -> ol
li: "<li>" (WORD* | SYMBOL | NUMBER*)* "</li>" -> li

SYMBOL: "."
        | ","
        | "!"
        | "?"
        | "$"
        | "#"
        | "%"
        | "("
        | ")"
        | "*"
        | "&"
        | "/"
        | "+"
        | "-"


attribute: attribute_name "=" ESCAPED_STRING
attribute_name: "style" -> style
    | "id" -> id
    | "class" -> class

id: "id=" WORD
class: "class=" WORD

%import common.WS   
%import common.WORD
%import common.ESCAPED_STRING
%import common.NUMBER

%ignore WS 

//tag: "<" content attribute* ">" (tag | text)*"</" content ">"

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

// style: "style=" ESCAPED_STRING
// style_option: "margin" | "width" | "height" | "padding" |
"""


parser = Lark(my_grammar)

file = 0
content = 0

def run_instruction(t, name=0):
    global content
    if t.data == 'start':
        global file
        file = open(name + '.html', 'w')
        file.write('<!DOCTYPE html> ')
        if (len(t.children) > 0):
            for child in t.children:
                run_instruction(child)

    elif t.data == 'html':
        file.write('<html> ')
        if (len(t.children) > 0):
            for child in t.children:
                run_instruction(child)
        file.write('</html>')
        file.close()

    elif t.data == 'head':
        file.write('<head>')
        if (len(t.children) > 0):
            for child in t.children:
                run_instruction(child)
        file.write('</head>')

    elif t.data == 'body':
        file.write('<body> ')
        if (len(t.children) > 0):
            for child in t.children:
                run_instruction(child)
        file.write('</body>')

    elif t.data == 'div':
        file.write('<div>')
        if (len(t.children) > 0):
            for child in t.children:
                run_instruction(child)
        file.write('</div>')

    elif t.data == 'title':
        file.write('<title>' + t.children[0] + '</title>')

    elif t.data == 'p':
        if len(t.children) > 1:
            textList = []
            for text in t.children:
                textList.append(text)
            content = ' '.join(textList)
            file.write('<p>' + content + '</p>')
        else:
            file.write('<p>' + str(t.children[0].value) + '</p>')

    elif t.data == 'h1':
        if len(t.children) > 1:
            textList = []
            for text in t.children:
                textList.append(text)
            content = ' '.join(textList)
            file.write('<h1>' + content + '</h1>')
        else:
            file.write('<h1>' + str(t.children[0].value) + '</h1>')

    elif t.data == 'h2':
        if len(t.children) > 1:
            textList = []
            for text in t.children:
                textList.append(text)
            content = ' '.join(textList)
            file.write('<h2>' + content + '</h2>')
        else:
            file.write('<h2>' + str(t.children[0].value) + '</h2>')

    elif t.data == 'h3':
        if len(t.children) > 1:
            textList = []
            for text in t.children:
                textList.append(text)
            content = ' '.join(textList)
            file.write('<h3>' + content + '</h3>')
        else:
            file.write('<h3>' + str(t.children[0].value) + '</h3>')

    elif t.data == 'h4':
        if len(t.children) > 1:
            textList = []
            for text in t.children:
                textList.append(text)
            content = ' '.join(textList)
            file.write('<h4>' + content + '</h4>')
        else:
            file.write('<h4>' + str(t.children[0].value) + '</h4>')

    elif t.data == 'a':
        if len(t.children) > 1:
            textList = []
            for text in t.children:
                textList.append(text)
            file.write('<a href=' + textList[0] + '>' + textList[1] + '</a>')
        else:
            file.write('<a href=' + t.children[0] + '>' + '</a>')

    elif t.data == 'img':
        file.write('<img src=' + t.children[0].value + '/>')

    elif t.data == 'ul':
        file.write('<ul>')
        if (len(t.children) > 0):
            for child in t.children:
                run_instruction(child)
        file.write('</ul>')

    elif t.data == 'ol':
        file.write('<ol>')
        if (len(t.children) > 0):
            for child in t.children:
                run_instruction(child)
        file.write('</ol>')

    elif t.data == 'li':
        if len(t.children) > 1:
            textList = []
            for text in t.children:
                textList.append(text)
            content = ' '.join(textList)
            file.write('<li>' + content + '</li>')
        else:
            file.write('<li>' + str(t.children[0].value) + '</li>')

    else:
        raise SyntaxError('Unknown instruction: %s' % t.children)

sample_1 = """
<!DOCTYPE html>
<html>
<head>
<title>This is the title!</title>
</head>
<body>
<h1>This is h1!</h1>
<p>This is p!</p>
</body>
</html>
"""

sample_2 = """
<!DOCTYPE html>
<html>
<head>
<title>Sample 2</title>
</head>
<body>
<h1>Welcome</h1>
<h2>to</h2>
<h3>HTML</h3>
<p>Sample text</p>
<ul>
<li>List item 1</li>
<li>List item 2</li>
</ul>
</body>
</html>
"""

def run_html(program, name):
    parse_tree = parser.parse(program)
    run_instruction(parse_tree, name)

def main():
    while True:
        name = input('Enter a file name (exclude .html)  or type "end" to close the program: ')
        if name == 'end':
            print('Closing program...')
            return 0;
        sequence = input('Write some HTML (beginning with <!DOCTYPE html> <html>): ')
        try:
            run_html(sequence, name)
            file = open(name + '.html', 'r')
            print(' ')
            print('******FOR DEBUG PURPOSES******')
            print(file.readlines())

            run_html(sample_1, 'sample_1')
            print('******SAMPLE PROGRAM #1 RAN AND SAVED AS SAMPLE_1.HTML******')

            run_html(sample_2, 'sample_2')
            print('******SAMPLE PROGRAM #2 RAN AND SAVED AS SAMPLE_2.HTML******')
        except Exception as e:
            print(e)

main()