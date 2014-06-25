#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from base.models.event import *

class Command(BaseCommand):
    args = ''
    help = 'Populate event_happenings timeslots from camp_events'

    def handle(self, *args, **options):

        n_created = 0
        n_skipped = 0

        time_slots =  EventTimeSlot.objects.all()
        
        for event in Event.objects.all():
            for time_slot in time_slots:
                obj, created = EventHappening.objects.get_or_create(timeslot=time_slot, event=event)
                if created:
                    n_created += 1
                    #self.stdout.write(u"Created event %s in timeslot %s" % (event, time_slot))
                else:
                    n_skipped += 1

        self.stdout.write("\nCreated: %d, skipped: %d" % (n_created, n_skipped))
                

