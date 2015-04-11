import datetime
import random
from .models import GiveawaySubmission
from moneywagon import push_tx, get_current_price
from pybitcointools import history, mktx, sign

def perform_giveaway(dry_run=True, giveaway_private_key=None):
    giveaway_address = '1K65TijR56S4CcwjXBnecYEKmTNrMag5uq'
    #giveaway_address = '1BUxsE6s6Kkpwn4ZQiYuu3zVAtVffJEyDP' # for testing

    ins = history(giveaway_address)
    giveaway_balance = sum(x['value'] for x in ins) / 1e8

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
    print "5 cents of btc", min_tip_amount

    winners = []
    while len(winners) < target_count:
        candidate = random.choice(all_submissions)
        if candidate.is_eligible(min_tip_amount):
            print "** Winner!", candidate
            winners.append({
                'address': candidate.address,
                'value': payout_amount_satoshi_encoded
            })
            if not dry_run:
                candidate.winner = True
                candidate.save()
        else:
            print "Rejected, Not eligible", candidate

    total_awarded_satoshi = sum([x['value'] for x in winners])
    print "Total satoshis added to giveaway TX:", total_awarded_satoshi

    fee_satoshi = 10000
    change_satoshi = int((giveaway_balance * 1e8) - (total_awarded_satoshi + fee_satoshi))

    # we have to add our own change output since pybitcointools doesnt do this for you.
    tx = mktx(ins, winners + [{'address': giveaway_address, 'value': change_satoshi}])

    for i in xrange(len(ins)):
        print "Signing", i
        tx = sign(tx, i, giveaway_private_key)

    print tx

    if not dry_run:
        print push_tx('btc', tx)
