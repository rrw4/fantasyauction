from django.contrib.auth.models import User
from django.db import models

from player.models import Player

class League(models.Model):
    name = models.CharField(max_length=100, blank=True)
    users = models.ManyToManyField(User, blank=True)
    size = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.name

class Roster(models.Model):
    league = models.ForeignKey(League)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.league.name + ', ' + self.user.username

class RosterPlayer(models.Model):
    roster = models.ForeignKey(Roster)
    player = models.ForeignKey(Player)

    def __unicode__(self):
        return self.roster.user.username + ' - ' + self.player.get_player_string()
