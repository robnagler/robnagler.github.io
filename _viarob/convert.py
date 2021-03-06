# -*- coding: utf-8 -*-
u"""Converted BOP Wiki to Kramdown/Jekyll/Nginx.

For more, see https://www.robnagler.com/2019/01/13/My-Best-Worst-Program.html

:copyright: Copyright (c) 2019 Robert Nagler.  All Rights Reserved.
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

_SIG_RE = re.compile(r'Via_Rob (\d{4}|(\d+)/(\d+)/(\d+))')

_A_RE = re.compile('@a href=(\S+) (.+)')

_A_BLOCK_RE = re.compile('^@a href=(\S+)$')

_H1_RE = re.compile('@h1\s+(.+)')

_H3_RE = re.compile('@h3\s+(.+)')

_IMG_RE = re.compile(r'@img(?:.block_center)? (?:style="[^"]+" )?src=(?:/my/file/Public/WikiData/|^)(\S+) alt="([^"]+)"')

_CODE_RE = re.compile(r'^@code\s+(.+)')

_PRETTY_RE = re.compile(r'@code.prettyprint.lang-(\w+)')

page_map = pkcollections.Dict()


def main(argv):
    parsed = []
    for f in argv:
        pkdp(f)
        tree = _parse(f, _SRC_D.join(f).read())
        if 'title' not in tree:
            tree.title = f.replace('_', ' ')
        page_map[f] = tree.href
        parsed.append(tree)
    for tree in parsed:
        pkdp(tree.dst.basename)
        t = '''---
layout: post
title: "{title}"
date: {date}T12:00:00Z
---
'''.format(**tree) + _gen(iter(tree.text))
        tree.dst.write(t, 'w')
    x = ''
    for k in sorted(page_map.keys()):
        x += '/my/page/{} "https://robnagler.com{}";\n'.format(k, page_map[k])
    pkio.py_path('viarob-map.txt').write(x)


def _gen(text, prefix=''):
    res = ''
    text = iter(text)
    for x in text:
        if isinstance(x, pkconfig.STRING_TYPES):
            res += prefix + x + '\n'
        elif isinstance(x, list):
            res += _gen(x, prefix)
        elif x.get('section_head'):
            res += _gen([x.text], '## ')
        elif x.get('rstrip'):
            res = res.strip()
        elif x.get('blockquote'):
            assert not prefix
            for l in text:
                if 'blockquote' in l:
                    assert not l.blockquote, \
                        res
                    break
                if l == '--':
                    res = res.rstrip() + ' --\n'
                else:
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
            res += prefix + '[{}]({})'.format(_gen([x.text]).rstrip(), h)
        elif x.get('lang'):
            assert not prefix
            res += '```{}\n{}```\n'.format(x.lang, _gen(x.text))
        elif x.get('img'):
            assert not prefix
            res += '![{}]({})\n'.format(
                _gen([x.alt]).rstrip(),
                '/assets/i/' + x.img,
            )
        elif x.get('code'):
            res += prefix + ' `{}` '.format(_gen([x.code]).rstrip())
        elif x.get('ol'):
            for i, t2 in enumerate(x.text):
                res += prefix + _gen([t2], '{}. '.format(i + 1))
        elif x.get('ul'):
            for t2 in x.text:
                res += prefix + _gen([t2], '* ')
        elif x.get('pre'):
            assert not prefix
            res += '\n'.join(['```text'] + x.text + ['```\n'])
        else:
            raise AssertionError('unknown token: {}'.format(x))
    return res


def _parse(wiki_name, wiki):
    res = pkcollections.Dict()
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
        if l.startswith('@pre'):
            x = pkcollections.Dict(pre=True, text=[])
            for l in lines:
                if '@/pre' in l:
                    break
                x.text.append(l)
            t.append(x)
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
        if l.startswith('@ol'):
            x = pkcollections.Dict(ol=True, text=[])
            for l in lines:
                if '@/ol' in l:
                    break
                l2 = l.replace('@li ', '')
                assert l != l2, \
                    '@li not found: {}'.format(l)
                x.text.append(_parse_text(l2))
            t.append(x)
            continue
        if l.startswith('@ul'):
            x = pkcollections.Dict(ul=True, text=[])
            for l in lines:
                if '@/ul' in l:
                    break
                l2 = l.replace('@li ', '')
                assert l != l2, \
                    '@li not found: {}'.format(l)
                x.text.append(_parse_text(l2))
            t.append(x)
            continue
        if l.startswith(('@em', '@/em')):
            continue
        m = _SIG_RE.search(l)
        if m:
            assert 'date' not in res
            if m.group(4):
                yy = int(m.group(4))
                if yy < 100:
                    yy += 2000
                mm = '{:02d}'.format(int(m.group(2)))
                dd = '{:02d}'.format(int(m.group(3)))
            else:
                yy = m.group(1)
                mm = '12'
                dd = '31'
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
    text = text.replace('@&mdash;', '--')
    text = text.replace('@&mdash', '--')
    text = text.replace('@&ldquo;', '"')
    text = text.replace('@&rdquo;', '"')
    text = text.replace('@&#8202;', ' ')
    text = text.replace('@&rarr;', '&rarr;')
    if text.endswith('@'):
        assert not text.endswith('@@')
        return [
            _parse_text(text[:-1]),
            pkcollections.Dict(rstrip=True),
        ]
    m = _CODE_RE.search(text)
    if m:
        return pkcollections.Dict(code=m.group(1).replace('@@', '@'))
    m = _IMG_RE.search(text)
    if m:
        return pkcollections.Dict(img=m.group(1), alt=_parse_text(m.group(2)))
    if '@' not in text:
        return text
    n = text.count('@')
    t = text.replace('@@', '@')
    assert t.count('@') * 2 == n, \
        '@ found {}'.format(text)
    return t


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
