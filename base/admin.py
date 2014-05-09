from django.contrib import admin

from base.models import ScoutChief, SubCamp, ScoutGroup, Event

class ScoutChiefAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'scout_group', 'code_membership')
    list_filter = ('scout_group',)

class GenericNameAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'name', 'n_objs')

class EventAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 'name', 'timeslot', 'subcamp', 'n_seats', 'tot_seats'
    )
    list_editable = (
        'name', 'timeslot', 'subcamp', 'n_seats', 'tot_seats'
    )

admin.site.register(ScoutChief, ScoutChiefAdmin)
admin.site.register(SubCamp, GenericNameAdmin)
admin.site.register(ScoutGroup, GenericNameAdmin)
admin.site.register(Event, EventAdmin)


