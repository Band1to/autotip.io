import random
from .models import GiveawaySubmission

def draw_winner(drawing_date):
    """
    For a given drawing date, select one submission out of the prior week
    randomly
    """
    week_ago = drawing_date - datetime.timedelta(days=7)

    all_submissions = GiveawaySubmission.objects.filter(
        date_created__gt=week_ago,
        date_created__lt=drawing_date,
        winner=False
    )

    while True:
        candidate = random.choice(all_submissions)
        if candidate.is_eligible():
            return candidate

def dry_run()
