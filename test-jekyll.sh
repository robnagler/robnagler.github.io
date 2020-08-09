#!/bin/bash
#
# runs github page version of jekyll (in busybox, but generally ok)
# If you "rm -f Gemfile.lock", it will recreate it.
#
docker rm -f jekyll
# for some reason docker control isn't working. probably busybox or no -t
trap 'echo exit; exit 1' INT
trap 'docker rm -f jekyll' EXIT
docker run --name=jekyll --net=host -i --rm -v="$PWD":/srv/jekyll jekyll/jekyll:pages bash <<'EOF' &
bundle install
bundle exec jekyll serve --host 0.0.0.0
EOF
echo "Visit http://$(hostname -f):4000"
wait
