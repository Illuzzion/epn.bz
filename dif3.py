# coding: utf-8
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


if __name__ == '__main__':
    a_fname = '1.html'
    b_fname = '2.html'

    with open(a_fname) as f:
        a_list = html2list(f.read())

    with open(b_fname) as f:
        b_list = html2list(f.read())

    a_struct = htmlstruct2list(a_list)
    b_struct = htmlstruct2list(b_list)

    # for el in a_struct:
    #     print el

    # for el in b_struct:
    #     print el

    difres = difflib.SequenceMatcher(None, a_struct, b_struct)
    print difres.ratio()

    for el in difres.get_opcodes():
        a_result = slice(el[1], el[2])
        b_result = slice(el[3], el[4])
        # print 'raw result', el
        if el[0] is not 'equal':
            print "{result}\na={a_res}\nb={b_res}".format(
                result=el[0],
                a_res=" ".join(a_struct[a_result]),
                b_res=" ".join(b_struct[b_result])
            )
