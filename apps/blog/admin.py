from django.contrib import admin
from blog.models import Entry, Image, Blog

admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(Image)