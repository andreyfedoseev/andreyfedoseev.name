from blog.feeds import RecentFeed, TagFeed
from blog.views.admin import EntryPreview, Index as AdminIndex, EditEntry, \
    UploadImage, ListEntryImages, DeleteImage
from blog.views.archive import Archive
from blog.views.comments import AddComment, DeleteComment
from blog.views.entry import Entry
from blog.views.index import Index
from blog.views.tags import Tags
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('blog.views',

    # Blog index
    url(r'^(?:tag/(?P<tag>[^/]+)/)?(?:page/(?P<page>\d+)/)?$', Index.as_view(), name="index"),

    # View entry
    url(r'^post/(?P<id>\d+)/(?:(?P<slug>[^/]+))?$', Entry.as_view(), name="entry"),

    # Archive
    url(r'^archive/(?:(?P<year>\d{4})/)?$', Archive.as_view(), name="archive"),

    # Comments
    url(r'^add-comment/(?P<entry_id>\d+)/$', AddComment.as_view(), name="add_comment"),
    url(r'^delete-comment/(?P<comment_id>\d+)/$', DeleteComment.as_view(), name="delete_comment"),

    # Tags
    url(r'^tags/$', Tags.as_view(), name="tags"),

    # Admin
    url(r'^admin/$', AdminIndex.as_view(), name="admin_index"),
    url(r'^admin/preview/$', EntryPreview.as_view(), name="admin_preview_entry"),
    url(r'^admin/new/$', EditEntry.as_view(), name="admin_add_entry"),
    url(r'^admin/edit/(?P<entry_id>\d+)/$', EditEntry.as_view(), name="admin_edit_entry"),
    url(r'^admin/ajax/image/add$', UploadImage.as_view(), name="admin_add_image"),
    url(r'^admin/ajax/image/list/(?P<entry_id>\d+)$', ListEntryImages.as_view(), name="admin_list_images"),
    url(r'^admin/ajax/image/delete$', DeleteImage.as_view(), name="admin_delete_image"),

) + patterns('',
    url(r'^feeds/recent/$', RecentFeed()),
    url(r'^feeds/tag/(?P<tag>[^/]+)/$', TagFeed(), name="tag_feed"),
)
