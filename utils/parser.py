# -*- coding: utf-8 -*-
# parser.py

import sys
import re

from StringIO import StringIO
from lxml import etree

class Parser(object):

    def build_tree(self, buf):
        pass

    def extract(self, xpath, single=False):
        pass

# end base class Parser


class XMLParser(Parser):

    def __init__(self, recover=True, encoding="utf-8"):
        self.recover = recover
        self.encoding = encoding

    def _regex(self, buf, reg):
        '''always return a list'''
        if reg is None or buf is None:
            return buf
        p = re.compile(reg)
        return p.findall(buf)

    def build_tree(self, buf):
        parser = etree.XMLParser(recover=self.recover,
                                 encoding=self.encoding)
        tree = etree.parse(StringIO(buf), parser)
        return tree

    def _single(self, lst):
        ret = None
        for e in lst:
            if e is not None and '' != e:
                ret = e
                break
        return ret

    def extract(self, tree, xpath, single=False):
        '''always return a list, single get 1st ele'''
        cells = tree.xpath(xpath)
        if single and len(cells) > 0:
            del cells[1: len(cells)]
        return cells

    def extract_many(self, tree, xpathes, single=False):
        '''dataset eg: [[a, b, c], [1, 2, 3]]'''
        dataset = []
        for xpath in xpathes:
            cells = self.extract(tree, xpath, single)
            dataset.append(cells)
        return dataset

    def extract_structured(self, tree, xpathes, single=False):
        '''xpathes should be a dict and contains __x__ each level'''
        dataset = []
        eles = self.extract(tree, xpathes["__x__"], single)
        for ele in eles:
            d = {}
            subtree = ele
            for k in xpathes:
                x = xpathes[k]
                if isinstance(x, dict):
                    d[k] = self.extract_structured(subtree, x, single)
                    pass
                elif k != "__x__":
                    tmp = self.extract(subtree, x, single)
                    tmp = self._single(tmp) if len(tmp) < 2 else tmp
                    d[k] = tmp
                else:
                    pass
            dataset.append(d)
        return dataset

    def reg_extract(self, tree, xpath, reg=None, single=False):
        i = 0
        cells = self.extract(tree, xpath, single)
        while i < len(cells):
            cells[i] = self._regex(cells[i], reg)
            i += 1
        return cells

# end class XMLParser

class HTMLParser(XMLParser):

    def __init__(self, recover=True, encoding="utf-8"):
        super(HTMLParser, self).__init__(recover, encoding)

    def build_tree(self, buf):
        parser = etree.HTMLParser(recover=self.recover,
                                 encoding=self.encoding)
        tree = etree.parse(StringIO(buf), parser)
        return tree

    def get_html(self, node):
        return html.tostring(node, encoding = 'utf-8')


# end class HTMLParser
