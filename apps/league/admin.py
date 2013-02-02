from django.contrib import admin
from league.models import League, Season, Roster, RosterPlayer

admin.site.register(League)
admin.site.register(Season)
admin.site.register(Roster)
admin.site.register(RosterPlayer)
