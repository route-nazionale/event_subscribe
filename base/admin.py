from django.contrib import admin

from base.models import Chief, SubCamp, ScoutGroup, Event

class ChiefAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'scout_group', 'code_membership')
    list_filter = ('scout_group',)

class GenericNameAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'name', 'n_objs')

class EventAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 'name', 'dt_start', 'dt_stop', 'subcamp', 'n_seats', 'tot_seats'
    )
    list_editable = (
        'name', 'dt_start', 'dt_stop', 'subcamp', 'n_seats', 'tot_seats'
    )

admin.site.register(Chief, ChiefAdmin)
admin.site.register(SubCamp, GenericNameAdmin)
admin.site.register(ScoutGroup, GenericNameAdmin)
admin.site.register(Event, EventAdmin)


