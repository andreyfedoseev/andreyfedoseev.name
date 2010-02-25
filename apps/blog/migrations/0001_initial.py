
from south.db import db
from django.db import models
from blog.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('blog_entry', (
            ('id', orm['blog.Entry:id']),
            ('blog', orm['blog.Entry:blog']),
            ('title', orm['blog.Entry:title']),
            ('text', orm['blog.Entry:text']),
            ('slug', orm['blog.Entry:slug']),
            ('published', orm['blog.Entry:published']),
            ('publication_timestamp', orm['blog.Entry:publication_timestamp']),
            ('meta_description', orm['blog.Entry:meta_description']),
            ('entry_type', orm['blog.Entry:entry_type']),
            ('include_in_rss', orm['blog.Entry:include_in_rss']),
            ('disable_comments', orm['blog.Entry:disable_comments']),
            ('hide_comments', orm['blog.Entry:hide_comments']),
            ('update_for', orm['blog.Entry:update_for']),
            ('cover', orm['blog.Entry:cover']),
        ))
        db.send_create_signal('blog', ['Entry'])
        
        # Adding model 'Image'
        db.create_table('blog_image', (
            ('id', orm['blog.Image:id']),
            ('entry', orm['blog.Image:entry']),
            ('image', orm['blog.Image:image']),
            ('order', orm['blog.Image:order']),
            ('caption', orm['blog.Image:caption']),
        ))
        db.send_create_signal('blog', ['Image'])
        
        # Adding model 'Blog'
        db.create_table('blog_blog', (
            ('id', orm['blog.Blog:id']),
            ('title', orm['blog.Blog:title']),
            ('site', orm['blog.Blog:site']),
        ))
        db.send_create_signal('blog', ['Blog'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('blog_entry')
        
        # Deleting model 'Image'
        db.delete_table('blog_image')
        
        # Deleting model 'Blog'
        db.delete_table('blog_blog')
        
    
    
    models = {
        'blog.blog': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'blog.entry': {
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Blog']"}),
            'cover': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'disable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'entry_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'}),
            'hide_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_in_rss': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'publication_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'update_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Entry']", 'null': 'True', 'blank': 'True'})
        },
        'blog.image': {
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Entry']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['blog']
