from django.db import models

from base.models import ScoutChief, Event, ScoutGroup

class ScoutChiefEventSubscribe(models.Model):

    scout_chief = models.ForeignKey(ScoutChief)
    event = models.ForeignKey(Event)

    subscribed_on = models.DateTimeField(auto_now_add=True)
    unsubscribed_on = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.scout_chief, self.event)

    class Meta:

        verbose_name = "iscrizione evento"
        verbose_name_plural = "iscrizioni eventi"
