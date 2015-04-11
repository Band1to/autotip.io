import datetime
import pytz
from moneywagon import HistoricalTransactions

from django.db import models

class Blog(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(default=datetime.datetime.now)

class GiveawaySubmission(models.Model):
    date_created = models.DateTimeField(default=datetime.datetime.now)
    address = models.TextField()
    winner = models.BooleanField(default=False)

    def __unicode__(self):
        win = " {WINNER}" if self.winner else ''
        return "[{:%m/%d/%Y} {}]{}".format(self.date_created, self.address, win)

    def is_eligible(self, min_tip_amount):
        if self.winner:
            # no duplicate winners
            return False

        end = datetime.datetime.today()
        start = end - datetime.timedelta(days=7)
        tipped_btc, count = self.tipping_stats_interval(start, end)
        return tipped_btc > min_tip_amount and count >= 1


    def tipping_stats_interval(self, start=None, end=None):
        """
        Consult the blockchain to see if they are actually tipping.
        Returns how much tipped and how many tips made for the previous week.
        """
        if not start and not end:
            end = datetime.datetime.today()
            start = end - datetime.timedelta(days=7)

        txs = HistoricalTransactions().get('btc', self.address)
        if not txs:
            return 0

        count = 0
        total = 0
        for tx in txs:
            if start.replace(tzinfo=pytz.UTC) < tx['date'] < end.replace(tzinfo=pytz.UTC):
                if tx['amount'] < 0: # only count spends
                    total += tx['amount']
                    count += 1

        return abs(total), count
