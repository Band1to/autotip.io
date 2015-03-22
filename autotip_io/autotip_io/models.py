import datetime
import pytz
from moneywagon import HistoricalTransactions

from django.db import models

class Blog(models.Model):
    author = models.ForeignKey()
    content = models.TextField()

class GiveawaySubmission(models.Model):
    date_created = models.DateTimeField(default=datetime.datetime.now)
    address = models.TextField()
    winner = models.BooleanField(default=False)

    def __unicode__(self):
        win = " {WINNER}" if self.winner else ''
        return "{:%m/%d/%Y} [{}]{}".format(self.date_created, self.address, win)

    def amount_tipped_interval(self, start, end):
        """
        Consult the blockchain to see if they are actually tipping.
        """
        txs = HistoricalTransactions().get('btc', self.address)
        if not txs:
            return 0

        total = 0
        for tx in txs:
            if start.replace(tzinfo=pytz.UTC) < tx['date'] < end.replace(tzinfo=pytz.UTC):
                total += tx['amount']

        return total
