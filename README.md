CSCI 3200 project - parsing a subset of HTML


For this project, I will be parsing HTML, the simple markup language for creating webpages. Through the parsing program, users should be able to create their own basic html webpage through the commandline. 

Tags to be included are mostly basic, such as: html, head, body, div, p, a, img, ul, ol, li, and h1 through h4. Styling through in-line attributes is not possible as well as using the <style> tag (because that would require parsing CSS too).

Everything not commented out using // in the "my_grammar" block is the grammar used. In html.py, starting at line 43, is the commented-out old method I used to implement the tag names... it did not exactly produce the tree I wanted.

**To run the parser, simply run the html.py program**. It will ask for user input, in which you can type HTML tags. __Users should start their input with <!DOCTYPE html> <html> and end with </html>__, as that is the standard for HTML files. To end the input and gracefullly end the program, type "end".

Sample programs are included in html.py as "sample_1" and "sample_2"

Don't forget to close your tags!

After a successful parsing of entered HTML, a .html file will save in the same directory as the html.py.