from django.conf.urls.defaults import patterns, url
from blog import feeds


feeds = {
    'recent': feeds.Recent,
}


urlpatterns = patterns('',
    url(r'^(?:page/(?P<page>\d+)/)?$', 'blog.views.index', name="index"),
    url(r'^types/$', 'blog.views.by_type', name="by_type"),
    url(r'^types/(?P<entry_type>\w+)/(?:page/(?P<page>\d+)/)?$', 'blog.views.index_by_type', name="index_by_type"),
    url(r'^dates/$', 'blog.views.by_date', name="by_date"),
    url(r'^dates/(?P<year>\d{4})/(?:(?P<month>\d{1,2})/)?(?:page/(?P<page>\d+)/)?$', 'blog.views.index_by_date', name="index_by_date"),
    url(r'^post/(\d+)/$', 'blog.views.entry'),
    url(r'^post/(\d+)/([^/]+)/$', 'blog.views.entry'),
    url(r'^comment-form/(?P<entry_id>\d+)/$', 'blog.commentviews.form', name="comment_form"),
    url(r'^add-comment/(?P<entry_id>\d+)/$', 'blog.commentviews.add_comment', name="add_comment"),
    url(r'^preview-comment/$', 'django.views.generic.simple.direct_to_template', {'template': 'blog/comments/preview.html'}, name="preview_comment"),
    url(r'^post/(\d+)/([^/]+)/$', 'blog.views.entry'),
    url(r'^i18n.js$', 'django.views.i18n.javascript_catalog', {'packages': ('blog',)}, name="i18n.js"),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feed"),
    url(r'^admin/$', 'blog.adminviews.index', name="admin-index"),
    url(r'^admin/preview/$', 'blog.adminviews.preview', name="preview"),
    url(r'^admin/new/$', 'blog.adminviews.add_entry', name="add-entry"),
    url(r'^admin/new/$', 'blog.adminviews.add_entry', name="add-entry"),
    url(r'^admin/edit/(\d+)/$', 'blog.adminviews.edit_entry', name="edit-entry"),
    url(r'^admin/ajax/upload-image/$', 'blog.adminviews.ajax_upload_image', name="ajax-upload-image"),
    url(r'^admin/ajax/get-images/$', 'blog.adminviews.ajax_get_images', name="ajax-get-images"),
    url(r'^admin/ajax/delete-image/$', 'blog.adminviews.ajax_delete_image', name="ajax-delete-image"),
)