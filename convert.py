# -*- coding: utf-8 -*-
u"""?

:copyright: Copyright (c) 2018 Bivio Software, Inc.  All Rights Reserved.
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

_SIG_RE = re.compile('Via_Rob (07)/(21)/(2017)')


def main(argv):
    for f in argv:
        pkdp(_parse(f, pkio.read_text(_SRC_D.join(f))))


def _parse(wiki_name, wiki):
    res = pkcollections.Dict()# wiki_name=wiki_name, wiki=wiki)
    fn = wiki_name.replace('_', '-')
    lines = iter(wiki.split('\n'))
    for l in lines:
        if l == '@h1':
            res.title = next(lines)
            next(lines)
            continue
        m = _SIG_RE.search(l)
        if m:
            res.date = '{}-{}-{}'.format(m.group(3), m.group(1), m.group(2))
            res.dst = _DST_D.join('{}-{}.md'.format(res.date, fn))
    return res


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
