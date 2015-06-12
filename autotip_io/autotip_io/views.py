import datetime

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from models import GiveawaySubmission, Blog, Article

@csrf_exempt
def giveaway_submission(request):
    address = request.POST['address']
    gs, created = GiveawaySubmission.objects.get_or_create(
        date_created=datetime.date.today(),
        address=address
    )
    if created:
        return HttpResponse("OK")
    else:
        return HttpResponse("Duplicate for today.")

def home(request):
    return TemplateResponse(request, 'home.html', {
        "latest_blogs": Blog.objects.order_by("-date_created")[:3]
    })

def giveaway_rules(request):
    return TemplateResponse(request, 'giveaway_rules.html', {})

def chrome_extension_docs(request):
    return TemplateResponse(request, 'chrome_extension_usage.html', {})

def docs(request, doc_name):
    return TemplateResponse(request, '%s_docs.html' % doc_name, {})

def getting_started(request, guide_name):
    # 'audio', 'writers'
    return TemplateResponse(request, 'getting_started_%s.html' % guide_name, {})

def single_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    return TemplateResponse(request, 'single_article_or_blog.html', {'blog': blog})


def single_article(request, pk):
    article = Article.objects.get(pk=pk)
    return TemplateResponse(request, 'single_article_or_blog.html', {'article': article})
