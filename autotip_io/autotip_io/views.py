import datetime

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from models import GiveawaySubmission, Blog

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

def blog(request):
    return TemplateResponse(request, 'blog.html', {
        'blogs': Blog.objects.all(),
    })

def giveaway_rules(request):
    return TemplateResponse(request, 'giveaway_rules.html', {})

def chrome_extension_docs(request):
    return TemplateResponse(request, 'chrome_extension_usage.html', {})
