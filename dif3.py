# coding: utf-8
from __future__ import print_function

import difflib
import string


def html2list(text):
    result = []
    # opentag = False
    content = ''

    def dump(s, res):
        if s.strip():
            res.append(s.strip())
            s = ''
        return s

    for c in text:
        if c == '<':
            content = dump(content, result)
            content += c
        elif c == '>':
            content += c
            content = dump(content, result)
        else:  # если текст
            if c in string.whitespace:
                # если символ пробельный (в т.ч \n,\t ...) то пишем пробел
                c = ' ' if c in string.whitespace else c

                # не добавляем пробелы к пробелам
                if content.endswith(' ') and c == ' ':
                    continue
                content += c
            else:
                content += c

    return result


def htmlstruct2list(html_list, text_replacement='$$$'):
    return [lel if lel.startswith('<') and lel.endswith('>') else text_replacement for lel in html_list]


def show_dif(a_list, b_list):
    difres = difflib.SequenceMatcher(None, a_list, b_list)
    print('match: {}%\n'.format(difres.ratio() * 100))

    for el in difres.get_opcodes():
        a_result = slice(el[1], el[2])
        b_result = slice(el[3], el[4])

        if el[0] is not 'equal':
            print(a_list[el[1] - 1: el[2] + 1])
            print(b_list[el[3] - 1: el[4] + 1])

            print("{result}\na={a_res}\nb={b_res}\n".format(
                result=el[0],
                a_res=" ".join(a_list[a_result]),
                b_res=" ".join(b_list[b_result])
            ))


if __name__ == '__main__':
    a_fname = '3.html'
    b_fname = '4.html'

    with open(a_fname) as f:
        a_list = html2list(f.read())

    with open(b_fname) as f:
        b_list = html2list(f.read())

    a_struct = htmlstruct2list(a_list)
    b_struct = htmlstruct2list(b_list)

    show_dif(a_struct, b_struct)
    show_dif(a_list, b_list)
