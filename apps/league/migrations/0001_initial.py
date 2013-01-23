# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'League'
        db.create_table('league_league', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('salary_cap', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('roster_limit', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('league', ['League'])

        # Adding M2M table for field users on 'League'
        db.create_table('league_league_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('league', models.ForeignKey(orm['league.league'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('league_league_users', ['league_id', 'user_id'])

        # Adding model 'Roster'
        db.create_table('league_roster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['league.League'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('salary_cap', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('total_salary', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('total_players', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('league', ['Roster'])

        # Adding model 'RosterPlayer'
        db.create_table('league_rosterplayer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('roster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['league.Roster'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player'])),
            ('salary', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('league', ['RosterPlayer'])


    def backwards(self, orm):
        # Deleting model 'League'
        db.delete_table('league_league')

        # Removing M2M table for field users on 'League'
        db.delete_table('league_league_users')

        # Deleting model 'Roster'
        db.delete_table('league_roster')

        # Deleting model 'RosterPlayer'
        db.delete_table('league_rosterplayer')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'league.league': {
            'Meta': {'object_name': 'League'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'roster_limit': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'salary_cap': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'league.roster': {
            'Meta': {'object_name': 'Roster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['league.League']"}),
            'salary_cap': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'total_players': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'total_salary': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'league.rosterplayer': {
            'Meta': {'object_name': 'RosterPlayer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player.Player']"}),
            'roster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['league.Roster']"}),
            'salary': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'player.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['league']