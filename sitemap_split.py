# coding: utf-8
import argparse
from lxml import etree
from urlparse import urlparse

MAX_SITEMAP_URLS = 50000


def parse_args():
    args = argparse.ArgumentParser()
    args.description = 'split big sitemap to few small sitemaps'
    args.add_argument('sitemap', help='path to input sitemap')
    args.add_argument('-p', '--parts', type=int, default=None, help='count of small sitemaps')
    return args.parse_args()


def normalize_node_name(node):
    """
    убираем нэймспейсы в именах тегов

    :param node: xml node с нэймспесом
    :return: xml node без нэймспейса
    """
    if node.tag.startswith('{'):
        start = node.tag.index('}') + 1
        node.tag = node.tag[start:]
    return node


def get_url_text(url_node):
    """
    присылают xml node с неймспесами, возвращаем очищенную строку

    :param url_node: xml node
    :return: str
    """
    url_tag = normalize_node_name(url_node).tag
    params = ["<{tag}>{text}</{tag}>".format(tag=normalize_node_name(param).tag, text=param.text) for param in url_node]
    return "<{tag}>\n{inner}\n</{tag}>\n".format(tag=url_tag, inner="\n".join(params))


def gen_sitemap_index(count, baseurl, filename='sitemap_index.xml'):
    """
    Пишем индекс сайтмэпов

    :param count: количество sitemap в индексе
    :param baseurl: базовый url
    :param filename: имя индекс файла
    :return: None
    """
    INDEX_BEGIN = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    INDEX_END = '</sitemapindex>'
    baseurl = baseurl if baseurl.endswith('/') else baseurl + '/'

    with open(filename, mode='w') as f:
        f.write(INDEX_BEGIN)
        for i in range(count):
            f.write(
                '<sitemap>\n<loc>{baseurl}sitemap{index}.xml</loc>\n</sitemap>\n'.format(baseurl=baseurl, index=i + 1)
            )
        f.write(INDEX_END)


def gen_sitemap_part(url_list, name):
    """
    пишем в файл часть сайтмэпов

    :param url_list: список с url
    :param name: имя файла
    :return: None
    """
    SITEMAP_BEGIN = '<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
                    'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" ' \
                    'xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 ' \
                    'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'
    SITEMAP_END = '</urlset>'
    with open(name, mode='w') as f:
        f.write(SITEMAP_BEGIN)
        for url in url_list:
            f.write(get_url_text(url))
        f.write(SITEMAP_END)


if __name__ == '__main__':
    # https://www.sitemaps.org/ru/protocol.html#sitemapXMLExample
    all_args = parse_args()

    try:
        data = etree.parse(all_args.sitemap, etree.XMLParser(encoding='utf-8', ns_clean=True, recover=True))

        print 'sitemap loaded'
        root = data.getroot()
        print 'found urls:', len(root)

        baseurl = ''
        for param in root[0]:
            if normalize_node_name(param).tag == 'loc':
                url_params = urlparse(param.text)
                print url_params
                baseurl = url_params.scheme + '://' + url_params.netloc

        print 'using baseurl:', baseurl

        if not all_args.parts:
            all_args.parts = (len(root) / MAX_SITEMAP_URLS) + 1
        print 'using parts:', all_args.parts

        urls_in_sitemap = len(root) / all_args.parts

        print 'urls in sitemap part: %s' % urls_in_sitemap

        slice_list = [slice(i * urls_in_sitemap, (i + 1) * urls_in_sitemap) for i in range(all_args.parts)]
        # заменим последний слайс и включим в него все оставшиеся записи
        slice_list[-1] = slice(slice_list[-1].start, len(root))

        gen_sitemap_index(len(slice_list), baseurl=baseurl)

        for index, cur_slice in enumerate(slice_list, 1):
            gen_sitemap_part(root[cur_slice], name='sitemap%d.xml' % index)

    except Exception as e:
        print e.args
