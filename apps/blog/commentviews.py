from blog.forms import CommentForm
from blog.models import Entry, Comment
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import cjson
from django.template.loader import render_to_string


AUTHOR_NAME_COOKIE = "comment_author_name"
AUTHOR_EMAIL_COOKIE = "comment_author_email"
AUTHOR_URL_COOKIE = "comment_author_url"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30

def form(request, entry_id=None):
    if request.method != 'POST':
        raise Http404
    if not entry_id:
        raise Http404
    try:
        entry = Entry.objects.get(pk=entry_id, published=True)
    except Entry.DoesNotExist: 
        raise Http404

    data = {}
    if request.user.is_anonymous():
        data['author_name'] = request.COOKIES.get(AUTHOR_NAME_COOKIE, "").decode('utf-8')
        data['author_email'] = request.COOKIES.get(AUTHOR_EMAIL_COOKIE, "").decode('utf-8')
        data['author_url'] = request.COOKIES.get(AUTHOR_URL_COOKIE, "").decode('utf-8')
    for k in request.POST:
        data[k] = request.POST[k] 
    form = CommentForm(data)

    validate = 'validate' in request.POST
    
    return render_to_response("blog/comments/form.html",
                              {'form': form,
                               'validate': validate,
                               'entry_id': entry_id},
                               context_instance=RequestContext(request))
     

def add_comment(request, entry_id=None):
    if request.method != 'POST':
        raise Http404
    if not entry_id:
        raise Http404
    try:
        entry = Entry.objects.get(pk=entry_id, published=True)
    except Entry.DoesNotExist: 
        raise Http404

    data = {}
    
    form = CommentForm(request.POST)
    cookies = {}
    if form.is_valid():
        kw = form.cleaned_data
        kw['entry'] = entry
        try:
            reply_to = kw.pop('reply_to')
            try:
                kw['parent'] = Comment.objects.get(pk=reply_to, entry=entry)
            except Comment.DoesNotExist:
                pass
        except KeyError:
            pass
        comment = Comment(**kw)
        comment.save()
        if request.user.is_anonymous():
            cookies[AUTHOR_NAME_COOKIE] = form.cleaned_data['author_name']
            cookies[AUTHOR_EMAIL_COOKIE] = form.cleaned_data['author_email']
            cookies[AUTHOR_URL_COOKIE] = form.cleaned_data['author_url']
        data['comment'] = render_to_string("blog/comments/include/comment.html",
                                {'comment': comment},
                                context_instance=RequestContext(request)) 
    else:
        data['form'] = render_to_string("blog/comments/include/commentform.html",
                        {'form': form,
                         'entry_id': entry_id,
                         'validate': True},
                         context_instance=RequestContext(request))
    response = HttpResponse(cjson.encode(data))
    if cookies:
        for k, v in cookies.items():
            response.set_cookie(k, v.encode('utf-8'), COOKIE_MAX_AGE) 
    return response   
