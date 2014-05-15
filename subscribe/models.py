#-*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

from base.models import ScoutChief, EventHappening

class ScoutChiefSubscription(models.Model):

    scout_chief = models.ForeignKey(ScoutChief)
    event_happening = models.ForeignKey(EventHappening)

    subscribed_on = models.DateTimeField(auto_now_add=True)
    unsubscribed_on = models.DateTimeField(null=True, blank=True)

    MAX_SUBSCRIPTIONS = 3

    class Meta:

        db_table = "subscriptions"
        verbose_name = "iscrizione evento"
        verbose_name_plural = "iscrizioni eventi"

    def __unicode__(self):
        return "%s - %s" % (self.scout_chief, self.event)

    def clean(self):
        """
        Checks among fields go here

        raises ValidationError if not valid
        """

        n_subscriptions = ScoutChief.object.filter(
            scout_chief=self.scout_chief
        ).count()

        if n_subscriptions >= self.MAX_SUBSCRIPTIONS:
            raise ValidationError('Non è possibile iscriversi a più di 3 eventi')

        #TODO: check no eventi sovrapposti
        #TODO: check che ci siano posti liberi
        

    def save(self, *args, **kw):
        self.full_clean()
        super(ScoutChiefSubscription, self).save(*args, **kw)
