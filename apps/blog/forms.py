from blog.models import Image, Comment
from django import forms
from django.forms import ModelForm
from django.forms.fields import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _
from tagging.forms import TagField
from tagging.utils import edit_string_for_tags
from tagging.models import Tag
import datetime


class ImagesWidget(forms.HiddenInput):
    
    def render(self, name, value, attrs=None):
        if isinstance(value, list):
            value = ",".join([str(v) for v in value])
        return super(ImagesWidget, self).render(name, value, attrs)
    

class ImagesField(forms.Field):
    
    widget = ImagesWidget
    
    def clean(self, value):        
        if self.required and value in EMPTY_VALUES:
            raise forms.ValidationError(self.error_messages['required'])
        values = value.split(",")
        try:
            values = [int(v) for v in values if v]
        except ValueError:
            raise forms.ValidationError(u"Values must be integers.")
        return values
            

class EntryForm(forms.Form):

    success_message = _(u"Your changes were saved.")
    error_message = _(u"Please correct the indicated errors.")

    title = forms.CharField(max_length=300,
                            required=True,
                            widget=forms.TextInput({"class": "title",
                                                    "placeholder": _(u"Title")}),
                            label=_(u"Title"),
                            )

    slug = forms.CharField(max_length=300,
                           required=False,
                           widget=forms.TextInput({"class": "slug",
                                                 "placeholder": _(u"Slug")}),
                           label=_(u"Slug"))

    text = forms.CharField(required=True,
                           widget=forms.Textarea({"class": "text markitup",
                                                  "placeholder": _(u"Text")}),
                           label=_(u"Text"),
                           )

    markdown = forms.BooleanField(required=False, initial=True,
                                   widget=forms.CheckboxInput({"class": "checkbox"}),
                                   label=_(u"Markdown"),
                                   )

    images = ImagesField(required=False,
                         label=_(u"Images"),
                         )

    published = forms.BooleanField(required=False, initial=False,
                                   widget=forms.CheckboxInput({"class": "checkbox"}),
                                   label=_(u"Published"),
                                   )
    publication_date = forms.DateField(required=False, input_formats=['%d.%m.%Y'],
                                       label=_(u"Publish on"),
                                       widget=forms.DateInput({"class": "date",
                                                               "size": "11",
                                                               "maxlength": "11",
                                                               }, format="%d.%m.%Y"))
    publication_time = forms.TimeField(required=False,
                                       label=_(u"Publication time"),
                                       widget=forms.TimeInput({"class": "time",
                                                               "size": "5",
                                                               "maxlength": "5",
                                                               }, format="%H:%M"))
    disable_comments = forms.BooleanField(required=False, initial=False, 
                                          label=_(u"Disable comments"),                                          
                                          widget=forms.CheckboxInput({"class": "checkbox"}))
    hide_comments = forms.BooleanField(required=False, initial=False,
                                       label=_(u"Hide comments"),
                                       widget=forms.CheckboxInput({"class": "checkbox"}))
    include_in_rss = forms.BooleanField(required=False, initial=True,
                                        label=_(u"Include in RSS"),
                                        widget=forms.CheckboxInput({"class": "checkbox"}))

    tags = TagField(required=False, label=_(u"Tags"),
                    widget=forms.TextInput({"class": "tags",
                                            "placeholder": _(u"Tags")}))
    
    def __init__(self, *args, **kwargs):
        #noinspection PyArgumentEqualDefault
        self.instance = kwargs.pop("instance", None)
        if self.instance:
            initial = kwargs.pop("initial", {})
            initial['title'] = self.instance.title
            initial['slug'] = self.instance.slug
            initial['text'] = self.instance.text
            initial['markdown'] = self.instance.markdown
            initial['published'] = self.instance.published
            initial['publication_date'] = self.instance.publication_timestamp and self.instance.publication_timestamp.date() 
            initial['publication_time'] = self.instance.publication_timestamp and self.instance.publication_timestamp.time()
            initial['images'] = [image.id for image in Image.objects.filter(entry=self.instance)]
            initial['disable_comments'] = self.instance.disable_comments
            initial['hide_comments'] = self.instance.hide_comments
            initial['include_in_rss'] = self.instance.include_in_rss
            initial['tags'] = edit_string_for_tags(Tag.objects.get_for_object(self.instance))
            kwargs["initial"] = initial
        super(EntryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.instance:
            return None
        data = self.cleaned_data
        self.instance.title = data.get('title')
        slug = data.get('slug')
        if slug:
            self.instance.slug = slug
        self.instance.text = data.get('text')
        self.instance.markdown = data.get('markdown')
        self.instance.published = data.get('published', False)
        publication_date = data.get('publication_date')
        publication_time = data.get('publication_time')
        now = datetime.datetime.now()
        if self.instance.published and not publication_date:
            publication_date = now.date()
        if self.instance.published and not publication_time:
            publication_time = now.time()
        if publication_date and publication_time:
            self.instance.publication_timestamp = datetime.datetime.combine(publication_date, publication_time)
        self.instance.disable_comments = data.get('disable_comments', False)
        self.instance.hide_comments = data.get('hide_comments', False)
        self.instance.include_in_rss = data.get('include_in_rss', False)
        if commit:
            self.instance.save()
        images = data.get("images", [])
        if images:
            for image_id in images:
                image = Image.objects.get(pk=int(image_id))
                if image.entry != self.instance:
                    image.entry = self.instance
                    image.save()
        Tag.objects.update_tags(self.instance, data.get('tags'))
        return self.instance


class BlogAuthorCommentForm(ModelForm):

    success_message = _(u"Your comment was added.")
    error_message = _(u"Please correct the indicated errors.")

    parent = forms.ModelChoiceField(queryset=Comment.objects.all(),
                                    required=False,
                                    widget=forms.HiddenInput())

    text = forms.CharField(required=True, widget=forms.Textarea(),
                           label=_(u"Text"),
                           help_text=_("""You can use <a class="dashed markdown" href="#">Markdown</a> here."""))

    class Meta:
        model = Comment
        fields = ["parent", "text"]


class CommentForm(BlogAuthorCommentForm):

    author_name = forms.CharField(required=True, label=_(u"Your name"),
                                  widget=forms.TextInput())
    author_email = forms.EmailField(required=False, label=_(u"Your email"),
                                    widget=forms.TextInput(),
                                    help_text=_("Optional. Used to get your Gravatar."))
    author_url = forms.URLField(required=False, label=_(u"Your site URL"),
                                widget=forms.TextInput(),
                                help_text=_("Optional."))

    notify = forms.BooleanField(required=False, label=_(u"Notify on replies by email"),
                                widget=forms.CheckboxInput())

    class Meta:
        model = Comment
        fields = ["parent", "text", "author_name", "author_email",
                  "author_url", "notify"]