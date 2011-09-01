from django.contrib import admin
from blog.models import Entry, Image, Blog, Comment


admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(Image)


class CommentAdmin(admin.ModelAdmin):

    list_display = ["__unicode__", "is_spam"]
    list_display_links = ["__unicode__"]
    list_editable = ["is_spam"]

admin.site.register(Comment, CommentAdmin)
