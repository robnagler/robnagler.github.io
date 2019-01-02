# -*- coding: utf-8 -*-
u"""?

:copyright: Copyright (c) 2018 Robert Nagler.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from pykern import pkcollections
from pykern import pkconfig
from pykern import pkio
from pykern.pkdebug import pkdp
import re
import sys


_SRC_D = pkio.py_path('wiki')

_DST_D = pkio.py_path('_posts')

_SIG_RE = re.compile(r'Via_Rob (\d+)/(\d+)/(\d+)')

_A_RE = re.compile('@a href=(\S+) (.+)')

_A_BLOCK_RE = re.compile('^@a href=(\S+)$')

_H1_RE = re.compile('@h1\s+(.+)')

_H3_RE = re.compile('@h3\s+(.+)')

_IMG_RE = re.compile('@img src=(?:/my/file/Public/WikiData/|^)(\S+) alt="(.+)"')

_CODE_RE = re.compile(r'^@code\s+(.+)')

_PRETTY_RE = re.compile(r'@code.prettyprint.lang-(\w+)')

page_map = pkcollections.Dict()


def main(argv):
    parsed = []
    for f in argv:
        pkdp(f)
        tree = _parse(f, pkio.read_text(_SRC_D.join(f)))
        if 'title' not in tree:
            tree.title = f
        page_map[f] = tree.href
        parsed.append(tree)
    for tree in parsed:
        t = '''---
layout: post
title: "{title}"
date: {date}T12:00:00Z
---
'''.format(**tree) + _gen(iter(tree.text))
        pkio.write_text(tree.dst, t)


def _gen(text, prefix=''):
    res = ''
    text = iter(text)
    for x in text:
        if isinstance(x, pkconfig.STRING_TYPES):
            res += prefix + x + '\n'
        elif x.get('section_head'):
            res += _gen([x.text], '## ')
        elif x.get('rstrip'):
            res = res.strip()
        elif x.get('blockquote'):
            for l in text:
                if 'blockquote' in l:
                    assert not l.blockquote
                    break
                res += _gen([l], '> ')
        elif x.get('href'):
            h = x.href
            if h.startswith('^'):
                h = h[1:]
                if h in page_map:
                    h = page_map[h]
                else:
                    assert '.' in h and not h.startswith('http'), \
                        'missing value in page_map: {}'.format(x.href)
                    h = 'http://' + h
            res += '[{}]({})\n'.format(_gen([x.text]).rstrip(), h)
        elif x.get('lang'):
            res += '```{}\n{}```\n'.format(x.lang, _gen(x.text))
        elif x.get('img'):
            res += '![{}]({})\n'.format(
                _gen([x.alt]).rstrip(),
                '/assets/i/' + x.img,
            )
        elif x.get('code'):
            res += ' `{}` '.format(_gen([x.code]).rstrip())
        else:
            raise AssertionError('unknown token: {}'.format(x))
    return res


def _parse(wiki_name, wiki):
    res = pkcollections.Dict()# wiki_name=wiki_name, wiki=wiki)
    res.md_name = wiki_name.replace('_', '-')
    lines = iter(wiki.split('\n'))
    t = []
    prefix = ''
    for l in lines:
        if l == '@h1':
            assert not 'title' in res
            res.title = next(lines)
            next(lines)
            continue
        m = _H1_RE.search(l)
        if m:
            assert not 'title' in res
            res.title = _parse_text(m.group(1))
            continue
        m = _H3_RE.search(l)
        if m:
            t.append(pkcollections.Dict(section_head=True, text=_parse_text(m.group(1))))
            continue
        if l.startswith('@b-html'):
            l = next(lines)
            if not l.startswith('<script'):
                assert l.startswith('<iframe'), \
                    '@b-html is not expected: {}'.format(l)
                t.append(l)
            l = next(lines)
            assert l.startswith('@/b-html'), \
                'expecting @/b-html: {}'.format(l)
            continue
        if l.startswith('@blockquote'):
            l = l.split('.')
            t.append('')
            t.append(pkcollections.Dict(blockquote=l[1] if len(l) > 1 else True))
            continue
        if l.startswith('@/blockquote'):
            t.append(pkcollections.Dict(blockquote=None))
            t.append('')
            continue
        if l.startswith(('@em', '@/em')):
            continue
        m = _SIG_RE.search(l)
        if m:
            yy = int(m.group(3))
            if yy < 100:
                yy += 2000
            mm = '{:02d}'.format(int(m.group(1)))
            dd = '{:02d}'.format(int(m.group(2)))
            res.date = '{}-{}-{}'.format(yy, mm, dd)
            res.dst = _DST_D.join('{}-{}.md'.format(res.date, res.md_name))
            res.href = '/{}/{}/{}/{}.html'.format(yy, mm, dd, res.md_name)
            continue
        m = _A_RE.search(l)
        if m:
            t2 = m.group(2)
            if t2.endswith('@'):
                t2 = t2[:-1]
            t.append(pkcollections.Dict(href=m.group(1), text=_parse_text(t2)))
            if m.group(2) != t2:
                t.append(pkcollections.Dict(rstrip=True))
            continue
        m = _A_BLOCK_RE.search(l)
        if m:
            x = pkcollections.Dict(href=m.group(1), text=_parse_text(next(lines)))
            l = next(lines)
            assert '@/a' == l, \
                'expecting @/a: {}'.format(l)
            t.append(x)
            continue
        m = _IMG_RE.search(l)
        if m:
            t.append(pkcollections.Dict(img=m.group(1), alt=_parse_text(m.group(2))))
            continue
        m = _PRETTY_RE.search(l)
        if m:
            x = pkcollections.Dict(lang=m.group(1), text=[])
            for l in lines:
                if '@/code' in l:
                    break
                x.text.append(l.replace('@@', '@'))
            t.append(x)
            continue
        l2 = l.replace('@div.bib by ', 'By ')
        if l != l2:
            t.append(_parse_text(l2))
            continue
        t.append(_parse_text(l))
    res.text = t
    return res


def _parse_text(text):
    text = text.replace('@&mdash', '--')
    text = text.replace('@&#8202;', ' ')
    m = _CODE_RE.search(text)
    if m:
        return pkcollections.Dict(code=m.group(1).replace('@@', '@'))
    if '@' not in text:
        return text
    n = text.count('@')
    t = text.replace('@@', '@')
    assert t.count('@') * 2 == n, \
        '@ found {}'.format(text)
    return t


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
