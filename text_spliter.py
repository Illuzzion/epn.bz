def split_text(text):
    """
    Разделяем поток текста на предложения и складываем их в список

    :param text:
    :return:
    """
    current_sentence, result = [], []
    new_sentence_flag = False
    text = text.replace('.', '. ')
    text = text.replace(',', ', ')
    text = text.replace('!', '! ')
    text = text.replace('?', '? ')

    def dump_sentence(sent_list, min_len=2):
        """
        если переданный список слов подходит под условия,
        то формируем предложение и добавляем к результату

        :param sent_list:
        :param min_len:
        :return:
        """
        if isinstance(sent_list, list) and len(sent_list) > min_len:
            result.append(' '.join(sent_list))
        sent_list.clear()

    for word in text.split(' '):
        # пропускаем пробелы и пустоту
        if not word.strip():
            continue

        if word.istitle() and new_sentence_flag:
            dump_sentence(current_sentence)

        new_sentence_flag = True if word[-1] in ('.', '!', '?') else False

        # если есть перевод строки, разделим часть текста по ним
        if not new_sentence_flag and '\n' in word:
            splited = word.split('\n')
            if len(splited) == 2:
                left, word = splited[0], splited[1]
                if left.strip():
                    current_sentence.append(left)
                dump_sentence(current_sentence)

            # если в получившемсся списке больше 2 слов
            else:
                # print('текущее предложение:', current_sentence)
                # если перечисление, типа список
                if not splited[0].endswith(':'):
                    pretender = " ".join([w for w in splited if w]).strip()
                    # print('pretender:', pretender)
                    if pretender.istitle():
                        # print('с заглавной')
                        dump_sentence(current_sentence)
                    word = pretender

        current_sentence.append(word.strip())

    # for s in result:
    #     print(s)

    return result


if __name__ == '__main__':
    with open('src.txt') as f:
        text = f.read()
        sentence_list = split_text(text)

    with open('out.txt', mode='w') as f:
        f.write("\n\n".join(sentence_list))
