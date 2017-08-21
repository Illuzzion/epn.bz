import random
import re
import string
from collections import defaultdict
from pprint import pprint

fname = 'src.txt'
# fname = 'small.txt'

WINDOW_SIZE = 3
WORDS_COUNT = 15


def clean_text(text):
    replace_elements = string.punctuation + '–«·»“'
    return re.sub('[' + replace_elements + ']', '', text)


def analyze_sentence(sentence, window=2):
    try:
        # разобьём предложение на слова и добавим начало и конец предложения
        tmp_list = ['*START*'] + sentence.strip().split() + ['*END*']
        # разделим предложение на части, размером в заданное окно и вернём список окон
        return [(*tmp_list[index: index + window],) for index in range(len(tmp_list)) if
                index + window <= len(tmp_list)]
    except ValueError as e:
        print(e.args)


def unpack_dict(packed):
    return sum([[key] * value for key, value in packed.items()], [])


def split_text(text):
    current_sentence, result = [], []
    last_dot = False
    text = text.replace('.', '. ')
    text = text.replace(',', ', ')
    text = text.replace('!', '! ')
    text = text.replace('?', '? ')

    for word in text.split():
        if word.istitle() and last_dot:
            sent_text = " ".join(current_sentence)
            result.append(sent_text)
            current_sentence.clear()

        last_dot = True if word[-1] in ('.', '!', '?') else False
        current_sentence.append(*word.split())

    # for s in result:
    #     print(s)

    return result


model = defaultdict(dict)

with open(fname) as f:
    text = f.read()
    sentence_list = split_text(text)

    print('предложений для обучения:', len(sentence_list))

    for sentence in sentence_list:
        # если просто пустая строка
        if not sentence:
            continue
        sentence = sentence.strip().lower()
        # print('текущее предложение:', sentence)

        sentence = clean_text(sentence)
        pairs = analyze_sentence(sentence, WINDOW_SIZE)
        # print(pairs)

        try:
            for f_word, *s_word in pairs:
                s_word = tuple(s_word)
                # print(f_word, s_word)
                model[f_word][s_word] = model[f_word].get(s_word, 0) + 1
        except ValueError as e:
            print(e.args)

# pprint(model)

new_sentence = []

for index in range(WORDS_COUNT):
    word = '*START*' if index is 0 else new_sentence[-1]
    print('слово:', word)
    unpacked = unpack_dict(model[word])
    print('варианты:', model[word].keys())
    # если вариантов для данного слова нет
    if not unpacked:
        break
    chosen_word = random.choice(unpacked)
    print('выбрано:', chosen_word)

    # если выбран символ окончания предложения, но предложение еще короткое
    if chosen_word == '*END*':
        if len(set(unpacked)) > 1:
            if len(new_sentence) < WORDS_COUNT:
                # перевыберем ещё раз
                chosen_word = random.choice(unpacked)
                print('перевыбрано:', chosen_word)
        else:
            new_sentence.append('.')
            break
    for ch in chosen_word:
        if ch == '*END*':
            break
        new_sentence.append(ch)

print('len:', len(new_sentence))
new_sentence[0] = str(new_sentence[0]).capitalize()
print(" ".join(new_sentence) + '.')
