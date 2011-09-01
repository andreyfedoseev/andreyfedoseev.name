from akismet import Akismet
from autoslug.fields import AutoSlugField
from blog.utils import render_text
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import datetime
import mptt
import tagging
import random
import string


class Blog(models.Model):

    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE,
                                unique=True)
    title = models.CharField(max_length=300, verbose_name=_(u"Title"))
    description = models.TextField(verbose_name=_(u"Description"), null=True,
                                   blank=True, default=u"")
    author_name = models.CharField(max_length=100)
    author = models.ForeignKey(User)

    feed_url = models.URLField(null=True, blank=True)

    author_google_buzz_id = models.CharField(max_length=100,
                                             verbose_name=(u"Author's Google Buzz ID"),
                                             null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.language == settings.LANGUAGE_CODE:
            urlconf = settings.ROOT_URLCONF
        else:
            urlconf = "%s_%s" % (settings.ROOT_URLCONF, self.language)
        return reverse("blog:index", urlconf=urlconf)

    def get_full_url(self):
        return "http://%s%s" % (Site.objects.get_current().domain,
                                self.get_absolute_url())

    def published_entries(self):
        return Entry.objects.published().filter(blog=self)

    def spam_comments(self):
        return Comment.objects.filter(is_spam=True, entry__blog=self)

    class Meta:
        verbose_name = _(u"Blog")
        verbose_name_plural = _(u"Blogs")


class EntryManager(models.Manager):

    def published(self, include_updates=False):
        if include_updates:
            return super(EntryManager, self).get_query_set().filter(published=True,
                             publication_timestamp__lte=datetime.datetime.now())
        else:
            return super(EntryManager, self).get_query_set().filter(published=True,
                             update_for=None,
                             publication_timestamp__lte=datetime.datetime.now())


class Entry(models.Model):

    blog = models.ForeignKey(Blog, verbose_name=_(u"Blog"))

    title = models.CharField(max_length=300, null=True, blank=True, verbose_name=_(u"Title"))
    text = models.TextField(null=True, blank=True, verbose_name=_(u"Text"))
    markdown = models.BooleanField(default=True)

    slug = AutoSlugField(populate_from="title", verbose_name=_(u"Slug"))
    published = models.BooleanField(default=False, verbose_name=_(u"Published"))
    publication_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_(u"Publication timestamp"))
    modified_on = models.DateTimeField(verbose_name=_("Modified on"), auto_now=True)

    meta_description = models.TextField(null=True, blank=True, verbose_name=_(u"Meta description"))

    include_in_rss = models.BooleanField(default=True, verbose_name=_(u"Include in RSS"))

    disable_comments = models.BooleanField(default=False, verbose_name=_(u"Disable comments"))
    hide_comments = models.BooleanField(default=False, verbose_name=_(u"Hide comments"))

    update_for = models.ForeignKey('self', null=True, blank=True, verbose_name=_(u"Update for"))

    objects = EntryManager()

    class Meta:
        ordering = ['-publication_timestamp']
        verbose_name = _(u"Entry")
        verbose_name_plural = _(u"Entries")

    def __unicode__(self):
        if self.title:
            return self.title
        if self.update_for is not None:
            return u"Update for \"%s\"" % unicode(self.update_for)
        return u"Entry #%i" % self.id

    def get_absolute_url(self):
        if self.blog.language == settings.LANGUAGE_CODE:
            urlconf = None
        else:
            urlconf = "%s_%s" % (settings.ROOT_URLCONF, self.blog.language)
        return reverse("blog:entry", urlconf=urlconf,
                       kwargs=dict(id=self.id, slug=self.slug))

    def threaded_comments(self):
        return self.comments.filter(is_spam=False).order_by('tree_id', 'lft')

    MORE_MARKER = "<!-- more -->"

    @property
    def short_text(self):
        text = self.text
        #noinspection PyUnresolvedReferences
        parts = text.split(self.MORE_MARKER, 1)
        if len(parts) > 1:
            text = parts[0]
            site = Site.objects.get_current()
            full_url = "http://%s%s" % (site.domain, self.get_absolute_url())
            text += """<p class="read-more"><a href="%s#cut">%s</a></p>""" % (full_url, _(u"Read more"))
        return mark_safe(render_text(text, self.markdown))

    @property
    def full_text(self):
        #noinspection PyUnresolvedReferences
        text = self.text.replace(self.MORE_MARKER, "<a name=\"cut\"></a>")
        return mark_safe(render_text(text, self.markdown))

    @property
    def comments_count(self):
        return self.comments.filter(is_spam=False).count()


tagging.register(Entry)


class Image(models.Model):

    THUMBNAIL_GEOMETRY = "180x180"
    SCALED_GEOMETRY = "500x500"

    entry = models.ForeignKey(Entry, null=True, verbose_name = _(u"Entry"))
    image = models.ImageField(upload_to="upload/images",
                             verbose_name = _(u"Image"))
    order = models.IntegerField(null=True, blank=True, verbose_name = _(u"Order"))

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _(u"Image")
        verbose_name_plural = _(u"Images")

    def __unicode__(self):
        return u"Image-%i" % self.id


def gen_secret(length=5):
    secret = ""
    seq = string.letters+string.digits
    for i in xrange(length):
        secret += random.choice(seq)
    return secret


class Comment(models.Model):

    entry = models.ForeignKey(Entry, related_name="comments")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    google_buzz_id = models.CharField(max_length=100, null=True, blank=True)

    timestamp = models.DateTimeField(null=False, blank=False, default=datetime.datetime.now)

    by_blog_author = models.BooleanField(default=False)

    author_name = models.CharField(max_length=100, null=True, blank=True, default=u"")
    author_email = models.EmailField(max_length=100, null=True, blank=True, default=u"")
    author_url = models.URLField(max_length=200, null=True, blank=True, default=u"")

    secret = models.CharField(max_length=5, null=True, blank=True,
                              default=gen_secret)
    notify = models.BooleanField(default=False)

    text = models.TextField()

    is_spam = models.BooleanField(default=False)

    def __unicode__(self):
        if self.by_blog_author:
            author_name = self.entry.blog.author_name
        else:
            author_name = self.author_name
        return _("Comment for \"%(entry_title)s\" by %(author_name)s") % dict(
            entry_title=self.entry.title,
            author_name=author_name,
        )

    def check_for_spam(self, request):
        if self.by_blog_author:
            return
        if not self.author_url and "http://" not in self.text:
            return
        key = getattr(settings, "AKISMET_KEY")
        if not key:
            return
        checker = Akismet(key=settings.AKISMET_KEY)
        is_spam = checker.comment_check(self.text.encode("utf-8"),
            data=dict(comment_author=self.author_name.encode("utf-8"),
                      comment_author_email=self.author_email.encode("utf-8"),
                      comment_author_url=self.author_url.encode("utf-8"),
                      user_ip=request.META["REMOTE_ADDR"],
                      user_agent=request.META["HTTP_USER_AGENT"]))
        if self.is_spam != is_spam:
            self.is_spam = is_spam
            self.save()

mptt.register(Comment, order_insertion_by=['timestamp'])
