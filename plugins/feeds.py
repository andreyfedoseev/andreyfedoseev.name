from __future__ import print_function
from markupsafe import Markup
from pelican import signals
from pelican.utils import set_date_tzinfo
from pelican.writers import Writer as BaseWriter
from six.moves.urllib.parse import urlparse, urljoin


class Writer(BaseWriter):

    def _add_item_to_the_feed(self, feed, item):
        title = Markup(item.title).striptags()
        link = urljoin(self.site_url, item.url)
        feed.add_item(
            title=title,
            link=link,
            unique_id='tag:%s,%s:%s' % (urlparse(link).netloc,
                                        item.date.date(),
                                        urlparse(link).path.lstrip('/')),
            description=item.get_content(self.site_url),
            categories=item.tags if hasattr(item, 'tags') else None,
            author_name=getattr(item, 'author', ''),
            pubdate=set_date_tzinfo(
                item.modified if hasattr(item, 'modified') else item.date,
                self.settings.get('TIMEZONE', None)))

    def write_feed(self, elements, context, path=None, feed_type='atom'):
        elements = filter(lambda x: getattr(x, "feed", None) not in ("false", "no", "False"), elements)
        return super(Writer, self).write_feed(elements, context, path, feed_type)


def get_writer(pelican):
    return Writer


def register():
    signals.get_writer.connect(get_writer)
