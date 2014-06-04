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
        return "%s - %s" % (self.scout_chief, self.event_happening)

    def clean(self):
        """
        Checks among fields go here

        raises ValidationError if not valid
        """

        subscriptions = ScoutChiefSubscription.objects.filter(
            scout_chief=self.scout_chief
        )
        n_subscriptions = subscriptions.count()

        if n_subscriptions >= self.MAX_SUBSCRIPTIONS:
            raise ValidationError('Non è possibile iscriversi a più di 3 eventi')

        #check no eventi sovrapposti
        if subscriptions.filter(event_happening__timeslot=self.event_happening.timeslot).count():
            raise ValidationError('Sei già iscritto ad un evento di questo turno')

        #TODO: check che ci siano posti liberi
        

    def save(self, *args, **kw):
        self.full_clean()
        super(ScoutChiefSubscription, self).save(*args, **kw)
