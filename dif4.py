# coding: utf-8
import difflib
from StringIO import StringIO
from lxml.html import parse, HtmlElement, HtmlComment, tostring

from dif3 import html2list, htmlstruct2list


def print_el(node, level=0):
    if isinstance(node, (HtmlElement, HtmlComment)):
        node_text = node.text.strip().encode('utf-8') if node.text else ''
        attrs = ", ".join([key + ': ' + val for key, val in node.attrib.items()])

        print "%stag=%s, text='%s', attr={%s}" % ("\t" * level, node.tag, node_text, attrs)

        # если дочерние элементы
        if len(node):
            for sub_el in node:
                print_el(sub_el, level + 1)
    else:
        raise Exception('not HtmlElement')


def open_html(filename):
    with open(filename) as f:
        file_content = f.read().decode(encoding='utf-8')
        return parse(StringIO(file_content)).getroot()


def get_html_code(node):
    return tostring(node, encoding="utf8").strip().decode('utf-8')


if __name__ == '__main__':
    a_fname, b_fname = '1.html', '2.html'

    a_root = open_html(a_fname)
    b_root = open_html(b_fname)

    xpath_value = 'body'

    # возьмём 0 элемент
    a_part = a_root.xpath(xpath_value)[0]
    a_html = get_html_code(a_part)
    a_list = html2list(a_html)
    a_struct = htmlstruct2list(a_list)

    b_part = b_root.xpath(xpath_value)[0]
    b_html = get_html_code(b_part)
    b_list = html2list(b_html)
    b_struct = htmlstruct2list(b_list)

    difres = difflib.SequenceMatcher(None, a_struct, b_struct)
    print 'match: %s%%' % (difres.ratio() * 100)

    for el in difres.get_opcodes():
        a_result = slice(el[1], el[2])
        b_result = slice(el[3], el[4])

        if el[0] is not 'equal':
            for not_match_a, not_match_b in zip(a_struct[a_result], b_struct[b_result]):
                print "\n%s\na=%s\nb=%s" % (el[0], not_match_a, not_match_b)
