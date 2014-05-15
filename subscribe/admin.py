from django.contrib import admin

from subscribe.models import ScoutChiefSubscription

class ScoutChiefSubscriptionAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'scout_chief', 'event', 'subscribed_on')
    list_display = ('__unicode__', 'subscribed_on',)
    #list_editable = ('scout_chief', 'event')

admin.site.register(ScoutChiefSubscription, ScoutChiefSubscriptionAdmin)
