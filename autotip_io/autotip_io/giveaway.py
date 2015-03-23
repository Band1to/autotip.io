import datetime
import random
from .models import GiveawaySubmission
from moneywagon import AddressBalance
from pybitcointools import history, mktx, sign


def perform_giveaway(dry_run=True):
    giveaway_address = '1K65TijR56S4CcwjXBnecYEKmTNrMag5uq'
    giveaway_balance = AddressBalance().get('btc', giveaway_address)
    to_be_given_away = giveaway_balance / 2

    print giveaway_balance, "BTC in donate address", to_be_given_away, "will be given away"

    drawing_date = datetime.datetime.now()
    week_ago = drawing_date - datetime.timedelta(days=7)

    all_submissions = GiveawaySubmission.objects.filter(
        date_created__gt=week_ago,
        date_created__lt=drawing_date,
        winner=False
    )

    print all_submissions.count(), "submissions received"
    target_count = int(all_submissions.count() / 2.0)
    reward_amount = to_be_given_away / target_count

    print reward_amount, "will be awarded to", target_count, "(half of all submissions)"

    if dry_run:
        return

    ins = history(giveaway_address)

    winners = []
    while len(winners) < target_count:
        candidate = random.choice(all_submissions)
        if candidate.is_eligible():
            winners.append(candidate.address)
            candidate.winner = True
            candidate.save()

    tx = mktx(ins, outs)
    tx2 = sign(tx, 0, priv)
