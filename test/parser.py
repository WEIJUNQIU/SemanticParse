import sys, cgi, re
from bs4 import BeautifulSoup, element
magical_class = "Nd92KSx3u2"
restricted_tags="title script object embed".split()
re_my_span = re.compile(r'&lt;span class="%s"&gt;(.+?)&lt;/span&gt;' % magical_class)

def no_nl(s): return str(s).replace("\r", "").replace("\n", " ")

if len(sys.argv) != 3:
    print "Usage: %s <input_html_file> <output_html_file>" % sys.argv[0]
    sys.exit(1)

def process(elem):
    for x in elem.children:
        if isinstance(x, element.Comment): continue
        if isinstance(x, element.Tag):
            if x.name in restricted_tags:
                continue
        if isinstance(x, element.NavigableString):
            if not len(no_nl(x.string).strip()):
                continue  # it's just empty space
            print '[', no_nl(x.string).strip(), ']',  # debug output of found strings
            s = ""
            for c in x.string:
                if c in (' ', '\r', '\n', '\t'): s += c
                else: s += '<span class="%s">%s</span>' % (magical_class, c)
            x.replace_with(s)
            continue
        process(x)

soup = BeautifulSoup(open(sys.argv[1]))
process(soup)
output = re_my_span.sub(r'<span class="%s">\1</span>' % magical_class, str(soup))
with open(sys.argv[2], 'w') as f:
    f.write(output)