# evaluate if necessary when using templates
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Content

@csrf_exempt
def index(request):

    if request.method == "POST":

        if 'url' in request.POST and 'short' in request.POST:
            url = request.POST['url']
            short = request.POST['short']
        else:
            return HttpResponse("POST not implemented without a querystring", status=501)

        # We check if the url was typed including 'http://', 'https://' or not
        if not url.startswith('http://') and not url.startswith('https://'):
            # if the url dont't include it, we add it to the start of the url
            url = 'https://' + url

        try:
            # upload content
            content = Content.objects.get(key=short)
            content.delete()
        except Content.DoesNotExist:
            pass

        print("URL: " + url)
        print("short: " + short)
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