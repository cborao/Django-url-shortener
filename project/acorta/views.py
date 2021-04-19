# evaluate if necessary when using templates
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Content


@csrf_exempt
def index(request):

    if request.method == "POST":

        # We check if the POST request have a valid query string
        if 'url' in request.POST and 'short' in request.POST:
            url = request.POST['url']
            short = request.POST['short']
        else:
            return HttpResponse("POST not implemented without a query string", status=501)

        # We check if the url was introduced including 'http://', 'https://' or not
        if not url.startswith('http://') and not url.startswith('https://'):
            # if the url dont't include it, we add it to the start of the url
            url = 'https://' + url

        try:
            # if the shortened url have been stored in a previous POST, we
            # remove it and add the new content.
            content = Content.objects.get(key=short)
            content.delete()
        except Content.DoesNotExist:
            pass

        content = Content(key=short, url=url)
        content.save()

    content_list = Content.objects.all()
    context = {'content_list': content_list}
    return render(request, 'acorta/index.html', context)


@csrf_exempt
def get_content(request, shortened):

    try:
        content = Content.objects.get(key=shortened)
        context = {'content': content}
        return render(request, 'acorta/serve.html', context, status=301)

    except Content.DoesNotExist:
        return HttpResponse("/" + shortened + ": is not a valid resource", status=404)