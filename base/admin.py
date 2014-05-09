from django.contrib import admin

from base.models import Chief, SubCamp, ScoutGroup

class ChiefAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'scout_group', 'code_membership')
    list_filter = ('scout_group',)

class GenericNameAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'name', 'n_objs')

admin.site.register(Chief, ChiefAdmin)
admin.site.register(SubCamp, GenericNameAdmin)
admin.site.register(ScoutGroup, GenericNameAdmin)


