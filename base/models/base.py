#-*- coding: utf-8 -*-

from django.db import models

class Unit(models.Model):

    name = models.CharField(max_length=128, primary_key=True)

    class Meta:

        db_table = "scout_units"
        verbose_name = "gruppo scout"
        verbose_name_plural = "gruppi scout"

    def __unicode__(self):
        return self.name

    def n_chiefs(self):
        return self.scoutchief_set.count()
    n_chiefs.short_description = "num. capi"

    n_objs = n_chiefs

#--------------------------------------------------------------------------------

class ScoutChief(models.Model):

    code = models.CharField(max_length=128, unique=True,
        verbose_name="codice censimento"
    )
    scout_unit = models.ForeignKey(Unit)

    name = models.CharField(max_length=32, verbose_name="nome")
    surname = models.CharField(max_length=32, verbose_name="cognome")
    birthday = models.DateField(verbose_name="data di nascita");

    class Meta:

        db_table = "scout_chiefs"
        verbose_name = "capo scout"
        verbose_name_plural = "capi scout"

    def __unicode__(self):
        return "%s - %s %s" % (self.scout_unit, self.name, self.surname)

#--------------------------------------------------------------------------------

class Person(models.Model):
    """
    Generic person to be bound to one or more events.

    QUESTION: how do we get different people? For a chief
    a unique code is the membership code, but for a "guest"?
    who is he?
    """

    KIND_CHIEF = "CHIEF"
    KIND_GUEST = "GUEST"
    KIND_CHOICES = (
        (KIND_CHIEF, "capo"),
        (KIND_GUEST, "ospite")
    )

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128, blank=True,
        verbose_name="codice censimento"
    )
    city = models.CharField(max_length=128, blank=True)
    kind = models.CharField(max_length=16,
        choices=KIND_CHOICES, default=KIND_CHIEF
    )
    description = models.TextField(blank=True)

#--------------------------------------------------------------------------------

class District(models.Model):
    """
    District entity
    """

    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128, unique=True)

    class Meta:

        db_table = "camp_districts"
        verbose_name = "sottocampo"
        verbose_name_plural = "sottocampi"

    def __unicode__(self):
        return self.name

    def n_events(self):
        return self.event_set.count()
    n_events.short_description = "num. eventi"

    n_objs = n_events

#--------------------------------------------------------------------------------

class HeartBeat(models.Model):

    name = models.CharField(max_length=128, unique=True)
    code = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.name
