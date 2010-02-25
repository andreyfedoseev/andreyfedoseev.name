from django.conf.urls.defaults import patterns, url
from blog import feeds


feeds = {
    'recent': feeds.Recent,
}


urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^page/(?P<page>\d+)/$', 'blog.views.index', name="blog_listing_page"),
    url(r'^post/(\d+)/$', 'blog.views.entry'),
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