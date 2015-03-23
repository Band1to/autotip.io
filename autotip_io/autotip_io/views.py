import datetime

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from models import GiveawaySubmission, Blog

@csrf_exempt
def giveaway_submission(request):
    address = request.POST['address']
    gs, created = GiveawaySubmission.objects.get_or_create(
        date_created=datetime.datetime.now(),
        address=address
    )
    return HttpResponse("OK")

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
