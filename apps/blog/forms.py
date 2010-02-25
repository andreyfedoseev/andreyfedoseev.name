from blog.models import Image, TEXT_TYPE, ENTRY_TYPES
from django import forms
from django.forms.fields import EMPTY_VALUES
from django.forms.util import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime


class ImagesWidget(forms.widgets.Input):
    
    input_type = "hidden"
    
    def render(self, name, value, attrs=None):
        if isinstance(value, list):
            value = ",".join([str(v) for v in value])
        return super(ImagesWidget, self).render(name, value, attrs=None)
    

class ImagesField(forms.Field):
    
    widget = ImagesWidget
    
    def clean(self, value):        
        if self.required and value in EMPTY_VALUES:
            raise ValidationError(self.error_messages['required'])
        values = value.split(",")
        try:
            values = [int(v) for v in values if v]
        except ValueError:
            raise forms.ValidationError(u"Values must be integers.")
        return values
            

class EntryForm(forms.Form):

    title = forms.CharField(max_length=300,
                            required=True,
                            widget=forms.TextInput({'class': 'inline-label title span-18 last'}),
                            label=_(u"Title"),
                            )

    text = forms.CharField(required=True,
                           widget=forms.Textarea({'class': 'inline-label  span-18 last tall markitup'}),
                           label=_(u"Text"),
                           )

    images = ImagesField(required=False,
                         label=_(u"Images"),
                         )

    entry_type = forms.ChoiceField(ENTRY_TYPES, required=True, initial=TEXT_TYPE,
                                   widget=forms.Select({'class': 'large'}),
                                   label=_(u"Entry Type"),
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


def getFormData(entry):
    data = {}
    data['title'] = entry.title
    data['text'] = entry.text
    data['entry_type'] = entry.entry_type
    data['published'] = entry.published
    data['publication_date'] = entry.publication_timestamp and entry.publication_timestamp.date() 
    data['publication_time'] = entry.publication_timestamp and entry.publication_timestamp.time()
    data['images'] = [image.id for image in Image.objects.filter(entry=entry)]
    data['disable_comments'] = entry.disable_comments
    data['hide_comments'] = entry.hide_comments
    data['include_in_rss'] = entry.include_in_rss
    return data


def saveEntry(entry, data):
    entry.title = data.get('title')
    entry.text = data.get('text')
    entry.entry_type = data.get('entry_type', TEXT_TYPE)
    entry.published = data.get('published', False)
    publication_date = data.get('publication_date')
    publication_time = data.get('publication_time')
    now = datetime.datetime.now()
    if entry.published and not publication_date:
        publication_date = now.date()
    if entry.published and not publication_time:
        publication_time = now.time()
    if publication_date and publication_time:
        entry.publication_timestamp = datetime.datetime.combine(publication_date, publication_time)
    entry.disable_comments = data.get('disable_comments', False)
    entry.hide_comments = data.get('hide_comments', False)
    entry.include_in_rss = data.get('include_in_rss', False)
    entry.save()
    images = data.get("images", [])
    if images:
        for image_id in images:
            image = Image.objects.get(pk=int(image_id))
            if image.entry != entry:
                image.entry = entry
                image.save()
        
    return entry
