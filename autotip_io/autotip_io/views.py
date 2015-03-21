import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import GiveawaySubmission

@csrf_exempt
def giveaway_submission(request):
    address = request.POST['address']
    gs, created = GiveawaySubmission.objects.get_or_create(
        date_created=datetime.datetime.now(),
        address=address
    )
    return HttpResponse("OK")
