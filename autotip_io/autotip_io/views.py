import datetime

from django.http import HttpResponse

from models import GiveawaySubmission

def giveaway_submission(request):
    #address = request.POST['address']
    #gs, created = GiveawaySubmission.objects.get_or_create(
    #    date_created=datetime.datetime.now(),
    #    address=address
    #)
    return HttpResponse("OK")
