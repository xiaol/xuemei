from django.db import models
from catalogue.abstract_models import *
import datetime
from userena.utils import user_model_label
from mysite import settings

from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

class Transaction(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    amount = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=Decimal("0.0"))

class Wallet(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField()
    
    payment_counter = models.IntegerField(default=1)
    last_balance = models.DecimalField(default=Decimal(0),
                                 max_digits=16,
                                 decimal_places=8)

class WalletTransaction(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    from_wallet = models.ForeignKey(
        'Wallet',
        related_name="sent_transactions")
    to_wallet = models.ForeignKey(
        'Wallet',
        null=True,
        related_name="received_transactions")
    amount = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=Decimal("0.0"))
    description = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        if self.from_wallet and self.to_wallet:
            return u"Wallet transaction "+unicode(self.amount)
        return u"Fee "+unicode(self.amount)

class Payment(models.Model):
    description = models.CharField(
        max_length=255,
        blank=True)
    amount = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=Decimal("0.0"))
    amount_paid = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=Decimal("0.0"))
    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField()
    paid_at = models.DateTimeField(null=True, default=None)
    transactions = models.ManyToManyField(Transaction)
    
    def is_paid(self, minconf=1):
        if self.paid_at:
            return True
        return self.amount_paid>=self.amount

class WalletStore(models.Model):
    wallet = ForeignKey(
	'Wallet',
	related_name='wallet_store')

    product = ForeignKey(
	'Product',
        related_name='wallet_store')

    amount = models.PositiveIntegerField()
    received_amount = models.PositiveIntegerField()

class Product(AbstractProduct):
    pass
 
class ProductClass(AbstractProductClass):
    pass

class Option(AbstractOption):
    pass
