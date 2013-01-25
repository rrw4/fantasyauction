from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from player.models import Player

class League(models.Model):
    name = models.CharField(max_length=100, blank=True)
    users = models.ManyToManyField(User, blank=True)
    size = models.IntegerField(blank=True) #number of teams in the league
    salary_cap = models.IntegerField(blank=True) #base salary cap per roster
    roster_limit = models.IntegerField(blank=True) #max players per roster

    def __unicode__(self):
        return self.name

class Roster(models.Model):
    league = models.ForeignKey(League)
    user = models.ForeignKey(User)
    salary_cap = models.IntegerField(blank=True) #roster's salary cap - may include cap penalties
    total_salary = models.IntegerField(blank=True) #sum of roster's salaries
    total_players = models.IntegerField(blank=True) #number of players on the roster

    def get_players(self):
        roster_players = RosterPlayer.objects.filter(roster=self)
        return roster_players

    def update_roster_numbers(self):
        roster_players = RosterPlayer.objects.filter(roster=self)
        total_salary = 0
        total_players = 0
        for roster_player in roster_players:
            total_salary += roster_player.salary
            total_players += 1
        self.total_salary = total_salary
        self.total_players = total_players
        self.save()

    def add_player(self, player, salary):
        """ Adds a player to roster by creating a RosterPlayer with the specified salary """
        if player != None and salary != None:
            rosterplayer = RosterPlayer(roster=self, player=player, salary=salary)
            rosterplayer.save()

    def __unicode__(self):
        return self.league.name + ', ' + self.user.username

class RosterPlayer(models.Model):
    roster = models.ForeignKey(Roster)
    player = models.ForeignKey(Player)
    salary = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.roster.user.username + ' - ' + self.player.get_player_string()

@receiver(post_save, sender=RosterPlayer)
def update_roster(sender, **kwargs):
    rosterplayer = kwargs.get('instance')
    roster = rosterplayer.roster
    roster.update_roster_numbers()
