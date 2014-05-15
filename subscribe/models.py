from django.db import models

from base.models import ScoutChief, EventHappening

class ScoutChiefEventHappeningSubscription(models.Model):

    scout_chief = models.ForeignKey(ScoutChief)
    event_happening = models.ForeignKey(EventHappening)

    subscribed_on = models.DateTimeField(auto_now_add=True)
    unsubscribed_on = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.scout_chief, self.event)

    class Meta:

        db_table = "subscriptions"
        verbose_name = "iscrizione evento"
        verbose_name_plural = "iscrizioni eventi"
