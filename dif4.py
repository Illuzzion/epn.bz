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


def get_string_dif(str1, str2):
    if isinstance(str1, (unicode,)) and isinstance(str2, (unicode,)):
        strdif = difflib.SequenceMatcher(None, str1, str2)
        # match_ratio = strdif.ratio()
        # print 'string match: %s%%' % match_ratio
        return [(reason, slice(s1, s2), slice(s3, s4))
                for reason, s1, s2, s3, s4 in strdif.get_opcodes()
                if reason is not 'equal']
        # print str1[difference[1]:difference[2]], '->', str2[difference[3]:difference[4]]


if __name__ == '__main__':
    a_fname, b_fname = '3.html', '4.html'

    a_root = open_html(a_fname)
    b_root = open_html(b_fname)

    xpath_value = 'head'
    print 'xpath: %s' % xpath_value

    # возьмём 0 элемент
    a_part = a_root.xpath(xpath_value)[0]
    a_html = get_html_code(a_part)
    a_list = html2list(a_html)
    a_struct = htmlstruct2list(a_list)

    b_part = b_root.xpath(xpath_value)[0]
    b_html = get_html_code(b_part)
    b_list = html2list(b_html)
    b_struct = htmlstruct2list(b_list)

    difres = difflib.SequenceMatcher(None, a_list, b_list)
    print 'page struct match: %s%%' % (difres.ratio() * 100)

    for el in difres.get_opcodes():
        a_result = slice(el[1], el[2])
        b_result = slice(el[3], el[4])

        if el[0] is not 'equal':
            for not_match_a, not_match_b in zip(a_list[a_result], b_list[b_result]):
                print "\n%s\na = %s\nb = %s" % (el[0], not_match_a, not_match_b)

                dif_list = get_string_dif(not_match_a, not_match_b)
                for d in dif_list:
                    print d[0], not_match_a[d[1]], not_match_b[d[2]]
