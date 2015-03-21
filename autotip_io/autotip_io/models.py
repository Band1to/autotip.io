import datetime
from django.db import models

class GiveawaySubmission(models.Model):
    date_created = models.DateTimeField(default=datetime.datetime.now)
    address = models.TextField()
    winner = models.BooleanField(default=False)

def draw_winner(drawing_date):
    """
    For a given drawling date, select one submission out of the prior week
    randomly
    """
    week_ago = drawing_date - datetime.timedelta(days=7)

    random_submission = GiveawaySubmission.objects.filter(
        date_created__gt=week_ago,
        date_created__lt=drawing_date,
        winner=False
    ).order_by("?")[1]

    eligible = []
    for gs in all_submissions:
        if gs.is_eligible():
            eligible.append(gs)

    random.choice()

    return winner
