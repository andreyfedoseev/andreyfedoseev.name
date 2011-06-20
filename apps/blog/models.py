from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.fields import ImageWithThumbnailsField
import datetime
import mptt
import tagging


class Blog(models.Model):
    
    title = models.CharField(max_length=300, verbose_name=_(u"Title"))
    site = models.OneToOneField(Site, verbose_name=_(u"Site"))
    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'blog:blog.views.index', ()

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


TEXT_TYPE = "text"
PHOTO_TYPE = "photo"
VIDEO_TYPE = "video"
AUDIO_TYPE = "audio"
LINK_TYPE = "link"
QUOTE_TYPE = "quote"


ENTRY_TYPES = (
    (TEXT_TYPE, _(u"Text")),
    (PHOTO_TYPE, _(u"Photo")),
    (VIDEO_TYPE, _(u"Video")),
    (AUDIO_TYPE, _(u"Audio")),
    (LINK_TYPE, _(u"Link")),
    (QUOTE_TYPE, _(u"Quote")),
)


class Entry(models.Model):
    
    blog = models.ForeignKey(Blog, verbose_name=_(u"Blog"))
    
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name=_(u"Title"))
    text = models.TextField(null=True, blank=True, verbose_name=_(u"Text"))
    
    slug = AutoSlugField(populate_from='title', unique=True, verbose_name=_(u"Slug"))
    published = models.BooleanField(default=False, verbose_name=_(u"Published"))
    publication_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_(u"Publication timestamp"))
    
    meta_description = models.TextField(null=True, blank=True, verbose_name=_(u"Meta description"))
    
    entry_type = models.CharField(max_length=20, null=False, blank=False, default=TEXT_TYPE,
                                  choices=ENTRY_TYPES, verbose_name=_(u"Entry type"))
    
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
    
    @models.permalink
    def get_absolute_url(self):
        if self.slug:
            return 'blog:blog.views.entry', [self.id, self.slug]
        else:
            return 'blog:blog.views.entry', [self.id]
        

    def threaded_comments(self):
        return self.comments.order_by('tree_id', 'lft')


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
    
    author = models.ForeignKey(User, null=True, blank=True, related_name="blog_comments")
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(max_length=100, null=True, blank=True)
    author_url = models.URLField(max_length=200, null=True, blank=True)
    
    notify = models.BooleanField(default=False)

    text = models.TextField()
        
mptt.register(Comment, order_insertion_by=['timestamp'])
