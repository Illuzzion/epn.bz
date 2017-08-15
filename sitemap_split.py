from lxml import etree, objectify
import argparse

url_template = """<url>
<loc>%s</loc>
<lastmod>%s</lastmod>
<changefreq>%s</changefreq>
<priority>%s</priority>
</url>
"""


def parse_args():
    args = argparse.ArgumentParser()
    args.description = 'split sitemap'
    args.add_argument('sitemap', help='path to input sitemap')
    args.add_argument('-m', '--maxurls', type=int, default=None, help='max urls in small sitemap')
    return args.parse_args()


def print_xml_data(obj):
    print obj.localname
    # print obj.tag, obj.text, obj.attrib, obj.namespace


if __name__ == '__main__':
    all_args = parse_args()
    try:
        # data = etree.parse(all_args.sitemap, etree.XMLParser(encoding='utf-8', ns_clean=True, recover=True))
        data = etree.parse(all_args.sitemap)
        objectify.deannotate(data, cleanup_namespaces=True)
        etree.cleanup_namespaces(data)

        print 'sitemap loaded'
        urlset = data.getroot()


        # print urlset.findall('url')


        urls = urlset.xpath('*')

        for index, url in enumerate(urlset):
            # print url.tag, url.text, url.attrib

            for param in url:
                print param.tag
                # print url_template % tuple(url.xpath('*/text()'))




    except Exception as e:
        print e.args
