from blog import feeds
from blog.views.admin import EntryPreview, Index, AddEntry, EditEntry
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import permission_required
from django.views.generic.base import TemplateView


feeds = {
    'recent': feeds.Recent,
}


urlpatterns = patterns('blog.views',

    # Blog index
    url(r'^(?:page/(?P<page>\d+)/)?$', 'index.index', name="index"),

    # View entry
    url(r'^post/(\d+)/$', 'entry.entry'),
    url(r'^post/(\d+)/([^/]+)/$', 'entry.entry'),

    # Archive
    url(r'^types/$', 'archive.by_type', name="by_type"),
    url(r'^types/(?P<entry_type>\w+)/(?:page/(?P<page>\d+)/)?$',
        'archive.index_by_type', name="index_by_type"),
    url(r'^dates/$', 'archive.by_date', name="by_date"),
    url(r'^dates/(?P<year>\d{4})/(?:(?P<month>\d{1,2})/)?(?:page/(?P<page>\d+)/)?$',
        'archive.index_by_date', name="index_by_date"),
    url(r'^tags/$', 'archive.by_tag', name="by_tag"),
    url(r'^tags/(?P<tag>[^/]+)/(?:page/(?P<page>\d+)/)?$',
        'archive.index_by_tag', name="index_by_tag"),

    # Switch display type
    url(r'^switch-display-type$', 'index.switch_display_type', name="switch_display_type"),

    # Comments
    url(r'^comment-form/(?P<entry_id>\d+)/$', 'comments.form', name="comment_form"),
    url(r'^add-comment/(?P<entry_id>\d+)/$', 'comments.add_comment', name="add_comment"),
    url(r'^preview-comment/$', TemplateView.as_view(template_name="blog/comments/preview.html"), name="preview_comment"),

    # Admin
    url(r'^admin/$', permission_required("add_entry")(Index.as_view()), name="admin_index"),
    url(r'^admin/preview/$', permission_required("add_entry")(EntryPreview.as_view()), name="admin_preview_entry"),
    url(r'^admin/new/$', permission_required("add_entry")(AddEntry.as_view()), name="admin_add_entry"),
    url(r'^admin/edit/(?P<pk>\d+)/$', permission_required("edit_entry")(EditEntry.as_view()), name="admin_edit_entry"),
    url(r'^admin/ajax/image/add$', 'admin.ajax_upload_image', name="admin_add_image"),
    url(r'^admin/ajax/image/list/(?P<entry_id>\d+)$', 'admin.ajax_list_entry_images', name="admin_list_images"),
    url(r'^admin/ajax/image/delete$', 'admin.ajax_delete_image', name="admin_delete_image"),

) + patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feed"),
    url(r'^i18n.js$', 'django.views.i18n.javascript_catalog', {'packages': ('blog',)}, name="i18n.js"),
)
