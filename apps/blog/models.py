from autoslug.fields import AutoSlugField
from blog.utils import render_text
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.fields import ImageWithThumbnailsField
import datetime
import mptt
import tagging


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

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.language == settings.LANGUAGE_CODE:
            urlconf = None
        else:
            urlconf = "%s_%s" % (settings.ROOT_URLCONF, self.language)
        return reverse("blog:index", urlconf=urlconf)

    def published_entries(self):
        return Entry.objects.published().filter(blog=self)

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

    slug = AutoSlugField(populate_from="title", unique=True, verbose_name=_(u"Slug"))
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
        return self.comments.order_by('tree_id', 'lft')

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
        return mark_safe(render_text(text))

    @property
    def full_text(self):
        #noinspection PyUnresolvedReferences
        text = self.text.replace(self.MORE_MARKER, "<a name=\"cut\"></a>")
        return mark_safe(render_text(text))


tagging.register(Entry)


class Image(models.Model):

    entry = models.ForeignKey(Entry, null=True, verbose_name = _(u"Entry"))
    image = ImageWithThumbnailsField(upload_to="upload/images",
                                     thumbnail={'size': (180, 180)},
                                     extra_thumbnails={
                                        'scaled': {'size': (500, 500)},
                                        'grid': {'size': (250, 250)},
                                     },
                                     verbose_name = _(u"Image"))
    order = models.IntegerField(null=True, blank=True, verbose_name = _(u"Order"))

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _(u"Image")
        verbose_name_plural = _(u"Images")

    def __unicode__(self):
        return u"Image-%i" % self.id
    
    
class Comment(models.Model):
    
    entry = models.ForeignKey(Entry, related_name="comments")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    timestamp = models.DateTimeField(null=False, blank=False, default=datetime.datetime.now)
    
    by_blog_author = models.BooleanField(default=False)

    author_name = models.CharField(max_length=100, null=True, blank=True)
    author_email = models.EmailField(max_length=100, null=True, blank=True)
    author_url = models.URLField(max_length=200, null=True, blank=True)
    
    notify = models.BooleanField(default=False)

    text = models.TextField()
        
mptt.register(Comment, order_insertion_by=['timestamp'])
