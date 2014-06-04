from django.contrib import admin

from base.models import (
    ScoutChief, District, Unit, Event, 
    HeartBeat, EventHappening, EventTimeSlot
)

class ScoutChiefAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 'scout_unit', 'code',
        'name', 'surname', 'birthday'
    )
    list_filter = ('scout_unit', 'name', 'surname', 'birthday')

class DistrictAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'code', 'n_objs')

class UnitAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'n_objs')

class EventAdmin(admin.ModelAdmin):

    list_display = (
        'code', 'num', 'name', 'district', 'seats_tot'
    )
    list_editable = (
        'name', 'district', 'seats_tot'
    )

class EventHappeningAdmin(admin.ModelAdmin):

    list_display = (
        'event', 'timeslot',
        'seats_n_boys', 'seats_n_chiefs'
    )
    list_editable = (
        'seats_n_boys',
    )

class HeartBeatAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'code')

class EventTimeSlotAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'name', 'dt_start', 'dt_stop')

admin.site.register(ScoutChief, ScoutChiefAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventHappening, EventHappeningAdmin)
admin.site.register(HeartBeat, HeartBeatAdmin)
admin.site.register(EventTimeSlot, EventTimeSlotAdmin)
