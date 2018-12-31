# -*- coding: utf-8 -*-
u"""?

:copyright: Copyright (c) 2018 Robert Nagler.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from pykern import pkio
from pykern import pkcollections
from pykern.pkdebug import pkdp
import re
import sys


_SRC_D = pkio.py_path('~/tmp/viarob')

_DST_D = pkio.py_path('~/src/robnagler/robnagler/_posts')

_SIG_RE = re.compile(r'Via_Rob (\d+)/(\d+)/(\d+)')

_A_RE = re.compile('@a href=(\S+) (.+)')

_H1_RE = re.compile('@h1\s+(.+)')

_H3_RE = re.compile('@h3\s+(.+)')

_IMG_RE = re.compile('@img src=(\S+) alt="(.+)"')

_PRETTY_RE = re.compile(r'@code.prettyprint.lang-(\w+)')

def main(argv):
    for f in argv:
        _gen(_parse(f, pkio.read_text(_SRC_D.join(f))))


def _gen(tree):
    t = '''---
layout: post
title: {title}
date: {date}T12:00:00Z
---
'''.format(**tree)
    pkio.write_text(tree.dst, t)


def _parse(wiki_name, wiki):
    res = pkcollections.Dict()# wiki_name=wiki_name, wiki=wiki)
    fn = wiki_name.replace('_', '-')
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
        if l.startswith('@blockquote'):
            l = l.split('.')
            t.append(pkcollections.Dict(blockquote=l[1] if len(l) > 1 else True))
            continue
        if l.startswith('@/blockquote'):
            t.append(pkcollections.Dict(blockquote=None))
            continue
        if l.startswith(('@em', '@/em')):
            continue
        m = _SIG_RE.search(l)
        if m:
            y = int(m.group(3))
            if y < 100:
                y += 2000
            res.date = '{}-{}-{}'.format(y, m.group(1), m.group(2))
            res.dst = _DST_D.join('{}-{}.md'.format(res.date, fn))
            continue
        m = _A_RE.search(l)
        if m:
            t.append(pkcollections.Dict(href=m.group(1), text=_parse_text(m.group(2))))
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
                x.text.append(_parse_text(l))
            t.append(x)
            continue
        t.append(_parse_text(l))
    res.text = t
    return res


def _parse_text(text):
    text = text.replace('@&mdash', '--')
    text = text.replace('@&#8202;', ' ')
    assert '@' not in text, \
        '@ found {}'.format(text)
    return text

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
