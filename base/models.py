from django.db import models

class ScoutGroup(models.Model):

    name = models.CharField(max_length=128, unique=True)

    class Meta:

        verbose_name = "gruppo scout"
        verbose_name_plural = "gruppi scout"

    def __unicode__(self):
        return self.name

    def n_chiefs(self):
        return self.chief_set.count()
    n_chiefs.short_description = "num. capi"

    n_objs = n_chiefs

#--------------------------------------------------------------------------------

class Chief(models.Model):

    code_membership = models.CharField(max_length=128, unique=True,
        verbose_name="codice censimento"
    )
    scout_group = models.ForeignKey(ScoutGroup)

    class Meta:

        verbose_name = "capo"
        verbose_name_plural = "capi"

    def __unicode__(self):
        return "<%s> - %s" % (self.scout_group, self.code_membership)

#--------------------------------------------------------------------------------

class SubCamp(models.Model):
    """
    Subcamp entity
    """

    name = models.CharField(max_length=128, unique=True)
    
    class Meta:

        verbose_name = "sottocampo"
        verbose_name_plural = "sottocampi"

    def __unicode__(self):
        return self.name

    def n_events(self):
        return self.event_set.count()
    n_events.short_description = "num. eventi"

    n_objs = n_events

#--------------------------------------------------------------------------------

class Event(models.Model):
    """
    Events can be laboratories or round tables, each one
    with their own specifications.

    They could be holded in different datetimes,
    by current requirements it seems that they will last
    for half-a-day but this model is planned to be versatile.

    The same thing happens for tot_seats which seems to be
    fixed (30 for a laboratory, 500 for a round table)
    """

    EVENT_KIND_CHOICES = (
        ('lab', 'laboratorio'),
        ('round-table', 'tavola rotonda'),
    )
    
    #?!? code = models.CharField(max_length=32, null=True, blank=True)

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    kind = models.CharField(max_length=32, choices=EVENT_KIND_CHOICES, default='lab')
    tot_seats = models.IntegerField(blank=True)
    n_seats = models.IntegerField(blank=True)

    is_handicap_compatible = models.BooleanField(default=True)
    subcamp = models.ForeignKey(SubCamp)

    dt_start = models.DateTimeField()
    dt_stop = models.DateTimeField()

    class Meta:

        verbose_name = "evento"
        verbose_name_plural = "eventi"

    def __unicode__(self):
        return self.name

