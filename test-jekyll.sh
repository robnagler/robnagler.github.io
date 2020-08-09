#!/bin/bash
#
# runs github page version of jekyll (in busybox, but generally ok)
# If you "rm -f Gemfile.lock", it will recreate it.
#
docker rm -f jekyll
docker run -d --name=jekyll --net=host -i --rm -v="$PWD":/srv/jekyll jekyll/jekyll:pages bash <<'EOF'
bundle install
bundle exec jekyll serve --host 0.0.0.0
EOF
echo 'You can:

docker stop jekyll
'
