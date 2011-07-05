from blog.models import Entry
from haystack import fields, site, indexes


class EntryIndex(indexes.RealTimeSearchIndex):

    text = fields.CharField(document=True, use_template=True)
    blog = fields.IntegerField(model_attr="blog__id")
    published = fields.BooleanField(model_attr="published")


site.register(Entry, EntryIndex)