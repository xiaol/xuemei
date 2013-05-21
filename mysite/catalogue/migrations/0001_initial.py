# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table(u'catalogue_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=16, decimal_places=8)),
        ))
        db.send_create_signal(u'catalogue', ['Transaction'])

        # Adding model 'Wallet'
        db.create_table(u'catalogue_wallet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('payment_counter', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('last_balance', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=16, decimal_places=8)),
        ))
        db.send_create_signal(u'catalogue', ['Wallet'])

        # Adding model 'WalletTransaction'
        db.create_table(u'catalogue_wallettransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('from_wallet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_transactions', to=orm['catalogue.Wallet'])),
            ('to_wallet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='received_transactions', null=True, to=orm['catalogue.Wallet'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=16, decimal_places=8)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['WalletTransaction'])

        # Adding model 'Payment'
        db.create_table(u'catalogue_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=16, decimal_places=8)),
            ('amount_paid', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=16, decimal_places=8)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('paid_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
        ))
        db.send_create_signal(u'catalogue', ['Payment'])

        # Adding M2M table for field transactions on 'Payment'
        db.create_table(u'catalogue_payment_transactions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payment', models.ForeignKey(orm[u'catalogue.payment'], null=False)),
            ('transaction', models.ForeignKey(orm[u'catalogue.transaction'], null=False))
        ))
        db.create_unique(u'catalogue_payment_transactions', ['payment_id', 'transaction_id'])

        # Adding model 'WalletStore'
        db.create_table(u'catalogue_walletstore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wallet_store', to=orm['catalogue.Wallet'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wallet_store', to=orm['catalogue.Product'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('received_amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'catalogue', ['WalletStore'])

        # Adding model 'Product'
        db.create_table(u'catalogue_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upc', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='variants', null=True, to=orm['catalogue.Product'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('product_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.ProductClass'], null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('cost_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Product'])

        # Adding model 'ProductClass'
        db.create_table(u'catalogue_productclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('requires_shipping', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('track_stock', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'catalogue', ['ProductClass'])

        # Adding M2M table for field options on 'ProductClass'
        db.create_table(u'catalogue_productclass_options', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productclass', models.ForeignKey(orm[u'catalogue.productclass'], null=False)),
            ('option', models.ForeignKey(orm[u'catalogue.option'], null=False))
        ))
        db.create_unique(u'catalogue_productclass_options', ['productclass_id', 'option_id'])

        # Adding model 'Option'
        db.create_table(u'catalogue_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Required', max_length=128)),
        ))
        db.send_create_signal(u'catalogue', ['Option'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table(u'catalogue_transaction')

        # Deleting model 'Wallet'
        db.delete_table(u'catalogue_wallet')

        # Deleting model 'WalletTransaction'
        db.delete_table(u'catalogue_wallettransaction')

        # Deleting model 'Payment'
        db.delete_table(u'catalogue_payment')

        # Removing M2M table for field transactions on 'Payment'
        db.delete_table('catalogue_payment_transactions')

        # Deleting model 'WalletStore'
        db.delete_table(u'catalogue_walletstore')

        # Deleting model 'Product'
        db.delete_table(u'catalogue_product')

        # Deleting model 'ProductClass'
        db.delete_table(u'catalogue_productclass')

        # Removing M2M table for field options on 'ProductClass'
        db.delete_table('catalogue_productclass_options')

        # Deleting model 'Option'
        db.delete_table(u'catalogue_option')


    models = {
        u'catalogue.option': {
            'Meta': {'object_name': 'Option'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Required'", 'max_length': '128'})
        },
        u'catalogue.payment': {
            'Meta': {'object_name': 'Payment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '16', 'decimal_places': '8'}),
            'amount_paid': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '16', 'decimal_places': '8'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Transaction']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'catalogue.product': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Product'},
            'cost_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variants'", 'null': 'True', 'to': u"orm['catalogue.Product']"}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.ProductClass']", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.productclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProductClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'track_stock': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'catalogue.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '16', 'decimal_places': '8'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'catalogue.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '16', 'decimal_places': '8'}),
            'payment_counter': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'catalogue.walletstore': {
            'Meta': {'object_name': 'WalletStore'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wallet_store'", 'to': u"orm['catalogue.Product']"}),
            'received_amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wallet_store'", 'to': u"orm['catalogue.Wallet']"})
        },
        u'catalogue.wallettransaction': {
            'Meta': {'object_name': 'WalletTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '16', 'decimal_places': '8'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'from_wallet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_transactions'", 'to': u"orm['catalogue.Wallet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_wallet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'received_transactions'", 'null': 'True', 'to': u"orm['catalogue.Wallet']"})
        }
    }

    complete_apps = ['catalogue']