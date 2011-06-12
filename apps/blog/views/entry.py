

def entry(request, id, slug=None):
    entry = get_object_or_404(Entry, id=id, slug=slug)
    return render_to_response("blog/entry.html", {
                              'entry': entry,
                              }, context_instance=RequestContext(request))
