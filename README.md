# Source for robnagler.com

Jekyll website. Visit [robnagler.com](https://www.robnagler.com).

## Development

```sh
sudo dnf install ruby-devel
sudo dnf install ImageMagick
gem install jekyll bundler
bundle install
bundle exec jekyll serve --watch --host=$(hostname -i)
```
