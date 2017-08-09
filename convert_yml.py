#!/usr/bin/env python3
import argparse
import datetime
import functools
import json
import os.path

from lxml import etree
from slugify import slugify


def dump_json(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        for offer in result:
            of_dict = dict(offer)
            f_name = of_dict['id'] + '.json'
            with open(os.path.join('out', f_name), mode='w') as f:
                json.dump(of_dict, f, ensure_ascii=False)
        return result

    return wrapper


def dump_md(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        for offer in result:
            f_name = offer['id'] + '.md'
            header = dict(
                Title=offer['name'],
                Slug=offer['name_slug'],
                Date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                Author='admin',
                Category=offer['category_slug'],
                RuCategory=offer['category'],
                Price=offer['price'],
                Status='published'
            )
            fields_order = ('Title', 'Slug', 'Date', 'Author', 'Category', 'RuCategory', 'Price', 'Status')
            data = ["{key}: {value}\n".format(key=name, value=header[name]) for name in fields_order]
            data.append('\n[![{alt}]({url})'.format(alt='', url=offer['picture']))
            data.append('\n[{text}]({url})'.format(text='Купить на AliExpress', url=offer['url']))

            with open(os.path.join('out', f_name), mode='w') as f:
                f.writelines(data)
        return result

    return wrapper


def get_categories(cat_data):
    return {category.attrib['id']: category.text for category in cat_data}


@dump_md
def offers(of_data, cat_dict, hash):
    for offer in of_data:
        tmp = {inner.tag: inner.text for inner in offer if inner.text}
        tmp['category'] = cat_dict.get(tmp['categoryId'], None)
        assert tmp['category'], 'category in None {}'.format(tmp)
        tmp['url'] = str(tmp['url']).replace('__DEEPLINK-HASH__', hash)
        # перенесем атрибуты
        for k, v in offer.attrib.items():
            tmp[k] = v

        tmp['category_slug'] = slugify(tmp['category'])
        tmp['name_slug'] = slugify(tmp['name'])

        yield tmp


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.description = 'epn.bz yml file converter'
    arg_parser.add_argument('yml_path', help='path to yml file')
    arg_parser.add_argument('-d', '--deeplink_hash', default='12345678', help='DEEPLINK HASH')
    args = arg_parser.parse_args()

    # создадим XMLParser с кодировкой и прочими плюшками, чтобы избежать ошибок при открытии
    data = etree.parse(args.yml_path, etree.XMLParser(encoding='utf-8', ns_clean=True, recover=True))
    print('xml tree loaded!')

    yml_catalog = data.getroot()

    categories_dict = {}
    # сначала загрузим категории
    for shop in yml_catalog:
        for sub in shop:
            if sub.tag == 'categories':
                categories_dict = get_categories(sub)
    print('categories loaded')

    # теперь грузим оферы
    for shop in yml_catalog:
        for sub in shop:
            if sub.tag == 'offers':
                offers(sub, categories_dict, args.deeplink_hash)
    print('done')
