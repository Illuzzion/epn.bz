import argparse
from lxml import etree


def parse_args():
    args = argparse.ArgumentParser()
    args.description = 'split sitemap'
    args.add_argument('sitemap', help='path to input sitemap')
    args.add_argument('-p', '--parts', type=int, default=None, help='count of small sitemaps')
    return args.parse_args()


def normalize_node_name(node):
    if node.tag.startswith('{'):
        last = node.tag.index('}')
        node.tag = node.tag[last + 1:]
    return node


def get_url_text(url_node):
    url_tag = normalize_node_name(url_node).tag
    params = ["<{tag}>{text}</{tag}>".format(tag=normalize_node_name(param).tag, text=param.text) for param in url]
    return "<{tag}>\n{inner}\n</{tag}>".format(tag=url_tag, inner="\n".join(params))


if __name__ == '__main__':
    # https://www.sitemaps.org/ru/protocol.html#sitemapXMLExample
    all_args = parse_args()

    try:
        data = etree.parse(all_args.sitemap, etree.XMLParser(encoding='utf-8', ns_clean=True, recover=True))

        print 'sitemap loaded'
        root = data.getroot()
        print 'found', len(root), 'urls'

        if not all_args.parts:
            all_args.parts = (len(root) / 50000) + 1
            print all_args.parts

        for index, url in enumerate(root):
            print 'sitemap' + index/all_args.parts
            print get_url_text(url)






    except Exception as e:
        print e.args
