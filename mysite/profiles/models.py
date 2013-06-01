from django.db import models
from django.utils.translation import ugettext_lazy as _

from userena.models import UserenaLanguageBaseProfile
from userena.utils import user_model_label

import datetime

from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.db import models

import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        logger.error('user token created')

class Profile(UserenaLanguageBaseProfile):
    """ Default profile """
    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
    )
    
    MARITAL_CHOICES = (
        (1,_('married')),
        (2,_('single')),
    )

    CUP_SIZE_CHOICES = ( 
        (1,_('32A')),
        (2,_('34B')),
        (3,_('36C')),
        (4,_('38D')),
	(5,_('40E')),
    )

    FIGURE_CHOICES = (
        (1,_('slightly fat')),
        (2,_('strong')),
        (3,_('standard')),
        (4,_('slightly thin')),
    )

    IDENTIFICATION_CHOICES = (
        (1,_('Unauthorized')),
        (2,_('Processing')),
        (3,_('authorized')),
    )

    user = models.OneToOneField(user_model_label,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')

    gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
    birth_date = models.DateField(_('birth date'),default=datetime.date.today)
    about_me = models.TextField(_('about me'), blank=True)
    marital_status = models.PositiveSmallIntegerField(_('marital status'),
						      choices=MARITAL_CHOICES,
 						      blank=True,
						      null=True) 
    height = models.IntegerField(default=0,blank=True,null=True)
    cup_size = models.PositiveSmallIntegerField(_('cup size'),
                                                      choices=CUP_SIZE_CHOICES,
						      blank=True, 
                                                      null=True)
    figure = models.PositiveSmallIntegerField(_('figure'),
                                                      choices=FIGURE_CHOICES,
                                                      blank=True,
                                                      null=True)

    hobbie = models.CharField(max_length=50,blank=True) 
    income = models.PositiveIntegerField(blank=True,null=True)
    message_price = models.PositiveIntegerField(default=0)
    point = models.IntegerField(default=0)

    identification = models.PositiveSmallIntegerField(_('is identification'),
							choices=IDENTIFICATION_CHOICES,
							default=1)
    
    @property
    def age(self):
        if not self.birth_date: return False
        else:
            today = datetime.date.today()
            # Raised when birth date is February 29 and the current year is not a
            # leap year.
            try:
                birthday = self.birth_date.replace(year=today.year)
            except ValueError:
                day = today.day - 1 if today.day != 1 else today.day + 2
                birthday = self.birth_date.replace(year=today.year, day=day)
            if birthday > today: return today.year - self.birth_date.year - 1
            else: return today.year - self.birth_date.year

class Address(models.Model):
     """ address for profile"""
     profile = models.ForeignKey(Profile,related_name='address')
     location = models.PointField(srid=32140,null=True)
     city = models.CharField(max_length=200)
     zipcode = models.IntegerField()

     objects = models.GeoManager()
