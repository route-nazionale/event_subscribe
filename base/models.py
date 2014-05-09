from django.db import models

class ScoutGroup(models.Model):

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:

        verbose_name = "gruppo scout"
        verbose_name_plural = "gruppi scout"

#--------------------------------------------------------------------------------

class Chief(models.Model):

    code_membership = models.CharField(max_length=128, unique=True)
    scout_group = models.ForeignKey(ScoutGroup)

    def __unicode__(self):
        return "<%s> - %s" % (self.scout_group, self.code_membership)

    class Meta:

        verbose_name = "capo"
        verbose_name_plural = "capi"

#--------------------------------------------------------------------------------

class SubCamp(models.Model):

    name = models.CharField(max_length=128, unique=True)
    
    def __unicode__(self):
        return self.name

#--------------------------------------------------------------------------------

class Event(models.Model):

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

    def __unicode__(self):
        return self.name

    class Meta:

        verbose_name = "evento"
        verbose_name_plural = "eventi"
