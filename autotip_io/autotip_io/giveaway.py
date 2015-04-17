import datetime
import random
from .models import GiveawaySubmission
from moneywagon import get_current_price, Transaction
from pybitcointools import history, mktx, sign

def perform_giveaway(dry_run=True, giveaway_private_key=None):
    giveaway_address = '1K65TijR56S4CcwjXBnecYEKmTNrMag5uq'
    #giveaway_address = '1BUxsE6s6Kkpwn4ZQiYuu3zVAtVffJEyDP' # for testing

    tx = Transaction('btc')
    tx.add_input(giveaway_address, giveaway_private_key)
    giveaway_balance = tx.total_input_satoshis() / 1e8

    to_be_given_away = giveaway_balance * 0.02
    dollars_per_btc, source = get_current_price('btc', 'usd')

    print "%.8f BTC (%.2f USD) in donate address %.8f BTC (%.2f USD) will be given away" % (
        giveaway_balance, giveaway_balance * dollars_per_btc,
        to_be_given_away, to_be_given_away * dollars_per_btc
    )

    drawing_date = datetime.datetime.now()
    week_ago = drawing_date - datetime.timedelta(days=7)

    raw_submissions = list(GiveawaySubmission.objects.filter(
        date_created__gt=week_ago,
        date_created__lt=drawing_date,
        winner=False
    ))

    # for now, try to send to unique addresses instead of multiple entries to
    # the same address. This code should be removed when there are more unique
    # entries per drawing.
    all_submissions = []
    for sub in raw_submissions:
        if sub.address not in [x.address for x in all_submissions]:
            all_submissions.append(sub)

    submission_count = len(all_submissions) #.count()
    print submission_count, "submissions received"
    if submission_count == 0:
        return

    target_count = int(submission_count / 1.0)
    reward_amount = to_be_given_away / target_count

    print "%d submissions (half of all submissions) will be each awarded %.8f BTC (%.2f USD)" % (
        target_count,
        reward_amount, reward_amount * dollars_per_btc
    )

    payout_amount_satoshi = int(reward_amount * 1e8)

    # replace the last 3 digits in the amount with "887" so the extenstion
    # can know it has been awarded.
    payout_amount_satoshi_encoded = int("%s887" % str(payout_amount_satoshi)[:-3])

    print "satoshi award:", payout_amount_satoshi
    print "encoded reward:", payout_amount_satoshi_encoded

    # this is theamount each potential winner needs to have to hae tipped to be
    # eligible for a payout.
    min_tip_amount = 0.04 / dollars_per_btc

    total_awarded_satoshi = 0
    while len(tx.outs) < target_count:
        candidate = random.choice(all_submissions)
        if candidate.is_eligible(min_tip_amount):
            print "** Winner!", candidate
            tx.add_output(
                address=candidate.address,
                value=payout_amount_satoshi_encoded
            )
            candidate.winner = True
            candidate.save()
            total_awarded_satoshi += payout_amount_satoshi_encoded
        else:
            print "Rejected, Not eligible", candidate

    print "Total satoshis added to giveaway TX:", total_awarded_satoshi

    if not dry_run:
        print tx.get_hex()
        raw_input("Press enter to push TX, ctrl-c to cancel")
        print tx.push()
    else:
        GiveawaySubmission.objects.all().update(winner=False)
        print tx.get_hex()
