#-*- coding: utf-8 -*-

from django.db import models

from base import Unit, Person, ScoutChief, District, HeartBeat
import query

#--------------------------------------------------------------------------------

class EventTimeSlot(models.Model):

    name = models.CharField(max_length=32, unique=True, blank=True, null=True)
    dt_start = models.DateTimeField()
    dt_stop = models.DateTimeField()

    class Meta:

        db_table = "camp_eventtimeslots"
        ordering = ('dt_start',)
        verbose_name = "turno"
        verbose_name_plural = "turni"

    def __unicode__(self):
        return self.name or "%s alle %s" % (
            self.dt_start.strftime("%A %d/%m dalle %H:%M"), self.dt_stop.strftime("%H:%M")
        )

    def save(self, *args, **kw):
        if not self.name:
            self.name = None
        super(EventTimeSlot, self).save(*args, **kw)

#--------------------------------------------------------------------------------

class EventHappening(models.Model):
    """
    Through table for timeslot_set ManyToManyField
    """

    timeslot = models.ForeignKey(EventTimeSlot)
    event = models.ForeignKey("Event")

    seats_n_boys = models.IntegerField(blank=True, default=0)
    seats_n_chiefs = models.IntegerField(blank=True, default=0)

    class Meta:
        db_table = "camp_eventhappenings"
        verbose_name = "evento"
        verbose_name_plural = "eventi"

    def __getattr__(self, attr_name):

        if attr_name in Event._meta.get_all_field_names() + ['code']:
            rv = getattr(self.event, attr_name)
        elif attr_name in EventTimeSlot._meta.get_all_field_names():
            rv = getattr(self.timeslot, attr_name)
        else:
            rv = super(self.__class__, self).__getattribute__(attr_name)
        return rv

    @property
    def n_seats(self):
        return self.seats_n_boys + self.seats_n_chiefs

    @property
    def available_seats(self):
        return self.event.seats_tot - self.n_seats

#--------------------------------------------------------------------------------

class EventPerson(models.Model):
    """
    Through table for timeslot_set ManyToManyField
    """

    ROLE_ANIMATOR = "ANIMATOR"
    ROLE_RELATOR = "RELATOR"
    ROLE_MODERATOR = "MODERATOR"
    ROLE_REFERRER = "REFERRED"
    ROLE_CHOICES = (
        (ROLE_ANIMATOR, "animatore"),
        (ROLE_RELATOR, "relatore"),
        (ROLE_MODERATOR, "moderatore"),
        (ROLE_REFERRER, "referente"),
    )

    person = models.ForeignKey(Person)
    event_happening = models.ForeignKey(EventHappening)
    role = models.CharField(max_length=16,
        choices=ROLE_CHOICES, default=ROLE_ANIMATOR
    )
    contacts = models.CharField(max_length=512, blank=True,
        verbose_name="contatti",
        help_text="codifica dei contatti di una persona. Ad es: cell:328111111, mail:a@a.com"
    )

    class Meta:
        db_table = "camp_eventhappeningpeople"
        verbose_name = "riferimento evento"
        verbose_name_plural = "riferimenti evento"

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

    EVENT_LAB = 'LAB'
    EVENT_TAV = 'TAV'
    EVENT_KIND_CHOICES = (
        (EVENT_LAB, 'laboratorio'),
        (EVENT_TAV, 'tavola rotonda'),
    )

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    timeslot_set = models.ManyToManyField(EventTimeSlot, through=EventHappening)

    #--- code parts (i.e: LAB-A30123 or TAV-B20001 ---#
    kind = models.CharField(max_length=32, choices=EVENT_KIND_CHOICES, default=EVENT_LAB)
    district = models.ForeignKey(District)
    topic = models.ForeignKey(HeartBeat, verbose_name="strada di coraggio")
    num = models.IntegerField(verbose_name="codice numerico")

    @property
    def code(self):
        return "%s-%s%s%s" % (
            self.kind, self.district.code, self.topic.code, self.num
        )

    #--- constraints ---#
    seats_tot = models.IntegerField(blank=True)

    min_seats = models.IntegerField(blank=True, default=1)
    max_boys_seats = models.IntegerField(blank=True, default=30)
    max_chiefs_seats = models.IntegerField(blank=True, default=5)

    min_age = models.IntegerField(verbose_name="età minima", blank=True)
    max_age = models.IntegerField(verbose_name="età massima", blank=True)

    #--- states ---#

    STATE_ENABLED = "ENABLED"
    STATE_RESERVED = "RESERVED"
    STATE_DISABLED = "DISABLED"

    STATE_THREECHOICES = (
        (STATE_ENABLED, 'abilitato'),
        (STATE_RESERVED, 'riservato'),
        (STATE_DISABLED, 'disabilitato'),
    )

    STATE_TWOCHOICES = (
        (STATE_ENABLED, 'abilitato'),
        (STATE_DISABLED, 'disabilitato'),
    )

    state_handicap = models.CharField(max_length=16,
        choices=STATE_TWOCHOICES, default=STATE_ENABLED,
        verbose_name="accessibilità ai diversamente abili"
    )
    state_chief = models.CharField(max_length=16,
        choices=STATE_THREECHOICES, default=STATE_ENABLED,
        verbose_name="rivolto ai capi"
    )

    #--- activation states ---#

    ACTIVATION_CREATING = "CREATING"
    ACTIVATION_ACTIVE = "ACTIVE"
    ACTIVATION_DISMISSED = "DISMISSED"
    ACTIVATION_CHOICES = (
        (ACTIVATION_CREATING, "in creazione"),
        (ACTIVATION_ACTIVE, "attivo"),
        (ACTIVATION_DISMISSED, "dismesso"),
    )

    state_activation = models.CharField(max_length=16,
        choices=ACTIVATION_CHOICES, default=ACTIVATION_ACTIVE,
        verbose_name="stato di attivazione"
    )

    #--- subscription states ---#

    SUBSCRIPTION_OPEN = "OPEN"
    SUBSCRIPTION_CLOSED = "CLOSED"
    SUBSCRIPTION_CHOICES = (
        (SUBSCRIPTION_OPEN, "aperte"),
        (SUBSCRIPTION_CLOSED, "chiuse"),
    )
    state_subscription = models.CharField(max_length=16,
        choices=SUBSCRIPTION_CHOICES, default=SUBSCRIPTION_OPEN,
        verbose_name="stato di iscrizione"
    )

    #--- referrers ---#

    objects = query.EventQuerySet.as_manager()

    class Meta:

        db_table = "camp_events"
        verbose_name = "definizione evento"
        verbose_name_plural = "definizione eventi"
        #?TOASK unique_together = (
        #?TOASK     ('num_code', 'kind'),
        #?TOASK )

    def __unicode__(self):
        return self.name

