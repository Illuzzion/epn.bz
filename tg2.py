import random
import re
import string
import sys
from collections import defaultdict, OrderedDict
from pprint import pprint
from text_spliter import split_text
import pymorphy2

fname = 'src.txt'
# fname = 'small.txt'

WINDOW_SIZE = 3
WORDS_COUNT = 20


def clean_text(text):
    replace_elements = string.punctuation + '–«·»“—'
    return re.sub('[' + replace_elements + ']', '', text)


def analyze_sentence(sentence, window=2):
    try:
        # разобьём предложение на слова и добавим начало и конец предложения
        tmp_list = ['*START*'] + sentence.strip().split() + ['*END*']

        # разделим предложение на части, размером в заданное окно и вернём список окон
        pre_result = [(*tmp_list[index: index + window],) for index in range(len(tmp_list))
                      if index + window <= len(tmp_list)]
        return pre_result
    except ValueError as e:
        print(e.args)


def unpack_dict(packed):
    return sum([[key] * value for key, value in packed.items()], [])


model = defaultdict(dict)

try:
    with open(fname) as f:
        text = f.read()
        sentence_list = split_text(text)
except FileNotFoundError as e:
    print(e)
    sys.exit(1)

print('предложений для обучения:', len(sentence_list))

# создание модели
for sentence in sentence_list:
    # если просто пустая строка
    if not sentence:
        continue
    sentence = sentence.strip().lower()

    # print('текущее предложение:', sentence)

    sentence = clean_text(sentence)

    # получим список кортежей слов с заданным размером окна
    pairs = analyze_sentence(sentence, WINDOW_SIZE)
    # print(pairs)

    try:
        for f_word, *s_word in pairs:
            s_word = tuple(s_word)
            # print(f_word, s_word)
            model[f_word][s_word] = model[f_word].get(s_word, 0) + 1
    except NameError as e:
        print(e.args)


# pprint(model)


def make_sentence(model, length=WORDS_COUNT):
    new_sentence = []
    length = int(length / WINDOW_SIZE)

    for index in range(length):
        # если интекс 0 - начало предложения, ищем в модели *START*
        word = '*START*' if index is 0 else new_sentence[-1]

        print('слово:', word)

        # если мы ещё не заканчиваем предложение
        unpacked = unpack_dict(model[word])
        if index < length - 1:
            # unpacked - list of tuple
            unpacked = [t for t in unpacked if t[-1] != '*END*']
        else:
            print('хотим закончить предложение')
            unpacked = [t for t in unpacked if t[-1] == '*END*']

        print('варианты:', set(unpacked))
        # print('варианты:', model[word].keys())
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
    return new_sentence


def make_words_agreement(word_list, pymorph):
    print('предложение:', " ".join(word_list))
    morph_list = OrderedDict()

    for word in word_list:
        pymorph_data = pymorph.parse(word)[0]
        morph_list[word] = (pymorph_data.normal_form, pymorph_data.tag)

    pprint(morph_list)


text = []
morph = pymorphy2.MorphAnalyzer()

for i in range(1):
    sent = make_sentence(model)
    text.append(" ".join(sent))
    make_words_agreement(sent, morph)

print(text)
