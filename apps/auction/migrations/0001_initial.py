# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Auction'
        db.create_table('auction_auction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['league.League'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('expiration_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('high_bid_value', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('high_bidder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
        ))
        db.send_create_signal('auction', ['Auction'])

        # Adding model 'Bid'
        db.create_table('auction_bid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auction.Auction'])),
            ('bidder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('current_value', self.gf('django.db.models.fields.IntegerField')()),
            ('max_value', self.gf('django.db.models.fields.IntegerField')()),
            ('current_high_bid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('winning_bid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('auction', ['Bid'])


    def backwards(self, orm):
        # Deleting model 'Auction'
        db.delete_table('auction_auction')

        # Deleting model 'Bid'
        db.delete_table('auction_bid')


    models = {
        'auction.auction': {
            'Meta': {'object_name': 'Auction'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expiration_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'high_bid_value': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'high_bidder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['league.League']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player.Player']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        'auction.bid': {
            'Meta': {'object_name': 'Bid'},
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auction.Auction']"}),
            'bidder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'current_high_bid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_value': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'winning_bid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
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
        'player.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['auction']