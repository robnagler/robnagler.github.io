# Source for robnagler.com

Jekyll website. Visit [robnagler.com](https://www.robnagler.com).

## Development

```sh
sudo dnf install ruby-devel
sudo dnf install ImageMagick
gem install jekyll bundler
bundle install
bundle exec jekyll serve --drafts --watch --host=$(hostname -i)
```


## Notes

Relative links:

```
[The God's Eye View]({{ site.baseurl }}{% post_url 2019-02-23-Gods-Eye-View %})
```
