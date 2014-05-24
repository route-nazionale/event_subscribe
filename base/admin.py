from django.contrib import admin

from base.models import ScoutChief, District, Unit, Event

class ScoutChiefAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'scout_unit', 'code')
    list_filter = ('scout_unit',)

class GenericNameAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'name', 'n_objs')

class EventAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 'name', 'district', 
        'seats_n_boys', 'seats_n_chiefs', 'seats_tot'
    )
    list_editable = (
        'name', 'district', 
        'seats_n_boys', 'seats_tot'
    )

admin.site.register(ScoutChief, ScoutChiefAdmin)
admin.site.register(District, GenericNameAdmin)
admin.site.register(Unit, GenericNameAdmin)
admin.site.register(Event, EventAdmin)


